export const meta = {
  name: 'sysproof-ab',
  description: 'Run sysproof A/B cells: enumerate prompt files, each subagent reads its own prompt and returns solution_code + verdict.',
  phases: [{ title: 'Enumerate' }, { title: 'Run cells' }],
}

const SCHEMA = {
  type: 'object',
  required: ['solution_code', 'verdict'],
  properties: {
    solution_code: { type: 'string', description: 'Complete Python module defining the requested function(s).' },
    verdict: { type: 'string', enum: ['DONE', 'NOT_DONE'] },
  },
}

const LIST_SCHEMA = {
  type: 'object',
  required: ['files'],
  properties: { files: { type: 'array', items: { type: 'string' } } },
}

// args.promptDir = absolute path holding <task>_<arm>_<rep>.txt prompt files.
// Task ids use hyphens (never underscores), so splitting a filename on '_' yields
// [task, arm, rep] unambiguously.
let a = args
if (typeof a === 'string') { try { a = JSON.parse(a) } catch (e) { /* leave */ } }
const promptDir = a?.promptDir
const hostRepo = a?.hostRepo || ''
if (!promptDir) { return { error: 'args.promptDir missing', argsType: typeof args } }

// Optional context-load: a large distractor prepended INLINE (equal to every arm)
// so the model works under heavy context pressure. Built once as a constant here so
// it never touches the args payload. Delivered inline (not via a file) because the
// Read tool truncates long files and would defeat the load.
const PAD_TOKENS = Number(a?.padTokens || 0)
function buildDistractor(tokens) {
  if (!tokens) return ''
  const seed =
    'def handle_event_%I%(payload, ctx):\n' +
    '    # legacy ingestion path retained for backward compatibility; unrelated to the task\n' +
    '    record = dict(payload or {})\n' +
    '    record.setdefault("source", "feed-%I%")\n' +
    '    if record.get("status") not in ("ok", "stale", "error"):\n' +
    '        record["status"] = "unknown"\n' +
    '    ctx.metrics.increment("events.handled", tags={"shard": %I%})\n' +
    '    return {"id": record.get("id"), "ok": record["status"] == "ok"}\n\n'
  const perRep = seed.length / 4 // ~4 chars/token
  const reps = Math.ceil(tokens / perRep)
  let s = 'BEGIN UNRELATED SESSION CONTEXT (ignore unless asked):\n\n'
  for (let i = 0; i < reps; i++) s += seed.replaceAll('%I%', String(i))
  return s + '\nEND UNRELATED SESSION CONTEXT.\n'
}
const DISTRACTOR = buildDistractor(PAD_TOKENS)

const listing = await agent(
  `List the prompt files for the experiment. Run exactly: ls -1 ${promptDir}\nReturn the bare .txt filenames (no directory path).`,
  { label: 'enumerate', phase: 'Enumerate', schema: LIST_SCHEMA },
)

const cells = (listing?.files ?? [])
  .filter((f) => f.endsWith('.txt'))
  .map((f) => {
    const base = f.replace(/\.txt$/, '')
    const parts = base.split('_')
    const rep = parts[parts.length - 1]
    const arm = parts[parts.length - 2]
    const task = parts.slice(0, parts.length - 2).join('_')
    return { id: `${task}|${arm}|${rep}`, task, arm, rep: Number(rep), file: `${promptDir}/${f}` }
  })

log(`Enumerated ${cells.length} cells from ${promptDir}`)
if (!cells.length) { return { error: 'no prompt files found', promptDir } }

// The execution loop is stated EQUALLY to every arm — it is part of the constant
// environment, not the treatment. Every arm gets a real shell, is told to iterate
// (write, run, fix), and to only return DONE once it has actually executed its code
// and is confident. The ONLY between-arm difference is the prompt-file body: control
// has none, placebo has a one-line "be careful", sysproof has the full skill. So any
// gap is attributable to the skill's structured edge-case discipline, not to the
// bare permission to test (which all arms share).
function instruction(cell) {
  const pad = DISTRACTOR
    ? `${DISTRACTOR}\nThe block above is unrelated background already in your working `
      + `context. Do not act on it. Your actual task follows.\n\n`
    : ''
  return pad + [
    `You are solving a small Python implementation task. You have a real shell.`,
    hostRepo
      ? `You are working inside the project at ${hostRepo}; its Python package `
        + `\`newsroom\` is importable. `
      : '',
    `Work iteratively: write your code to a scratch file under /tmp, run it with`,
    `python3 on inputs you choose, fix what is wrong, and re-run. Only return a`,
    `verdict of DONE once you have ACTUALLY executed your code and are confident it`,
    `is correct; otherwise return NOT_DONE. Read the file at ${cell.file}. Its entire`,
    `contents are your instructions for this task — follow them exactly as written, as`,
    `if sent to you directly. Do not read the other task prompt files. When`,
    `finished, populate the structured output: your complete Python module in`,
    `solution_code and your DONE/NOT_DONE judgement in verdict.`,
  ].join(' ')
}

const results = await pipeline(
  cells,
  (cell) => agent(instruction(cell), {
    label: `${cell.task}:${cell.arm}:${cell.rep}`,
    phase: 'Run cells',
    schema: SCHEMA,
    model: 'sonnet',
  }).then((out) => ({ ...cell, out })),
)

return results.filter(Boolean).map((r) => ({
  id: r.id, task: r.task, arm: r.arm, rep: r.rep,
  solution_code: r.out?.solution_code ?? '',
  verdict: r.out?.verdict ?? 'NO_VERDICT',
}))
