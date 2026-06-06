# What actually makes a coding-agent skill work: 930 controlled runs

I was curious. I already lean on a handful of skills when I work with a coding agent, like systematic debugging, test-driven development, and the brainstorming pass before I touch code, and they genuinely change how the sessions go. So I wanted to know what else I could add. If a debugging skill makes the agent better at debugging, what kind of skill makes it better at the thing every agent is worst at: finishing 80% of a task, declaring victory, and skipping the part that mattered?

I wrote one to find out. It told the agent two things: verify your work before you say "done," and read the existing code before you write anything new. Both felt obviously right. Then instead of trusting that feeling, I built a harness to measure whether it did anything. The measurement is the whole story.

## How I tested it

A controlled A/B, run like an experiment rather than a vibe check. Same tasks, same model. It started as three arms, the bare task (control), a "be careful, verify your work" placebo, and the full skill, and grew to seven as I chased the active ingredient. The full set is in Methods at the end. The only thing that differed between arms was the prompt body. A hidden test suite graded every run mechanically, so nothing depended on my judgment of "looks done."

Two metrics across the study. First, false-done rate: the agent claimed DONE but the hidden suite failed. Later, task-correct rate on requirements that only existed in the codebase, not the prompt. I powered each cell to about 40 runs so a result would mean something, and I used real statistics throughout: Wilson intervals, Fisher exact tests, cluster bootstraps, Holm correction across conditions. The final study is 12 conditions, around 930 graded runs, three model tiers.

## Result 1: the careful skill is inert

Across the first six conditions the skill sat on top of control. On Sonnet with real iteration it was an exact null, 8/30 versus 8/30 false-done. On weaker models it was worse: Haiku went 9/30 control to 16/30 with the skill, and a Kimi cloud model moved the same direction. The verbose "be careful" text pushed those models into confident DONE declarations and suppressed the honest NOT_DONE hedging they would otherwise produce.

The one thing that ever moved false-done was unrelated to the skill. When I placed visible acceptance tests in the workspace, the rate dropped from about 27% to 10%, identically across all three arms. The lever was test presence, not the prompt. A capable model that can run its own code is already verifying. Telling it to verify adds nothing it was not doing.

## Result 2: a promising redesign that died under power

So I rewrote the skill to front-load investigation instead of back-loading verification: research the codebase first. New metric, harder tasks where the real requirement was latent in the code and never stated in the prompt.

On a quick run of 10 per arm it finally led, 60% correct versus 45% for control. This is the moment the experiment earned its keep. I scaled the cleanest discriminator, a contract-error task, to 40 runs per arm, and the win vanished completely. Skill 0/40, control 0/39, Fisher p = 1.0. In all 40 skill runs the agent never once mentioned the code it needed, even though the prefix was in every prompt and the module was importable. The probability of 0/40 if the true effect had been as large as the n=10 run implied was about 6 in 10 million. The early signal was noise.

There was no bug. The skill text was present, the code was reachable, and the agent read "raise an error if the field is missing," decided it already knew the answer, wrote the generic version, and moved on. A principle does not override a prior. The model had no reason to go look, so it did not.

## Result 3: a procedure with a hard stop changes everything

A principle-style skill being inert is not the same as skills being inert. So I changed exactly one variable. Same task, same model, same 0/40 baseline. Instead of a value ("ground your work in the codebase"), I wrote a procedure with a blocking gate:

> Locate the project package, read its modules, quote the exact function that defines the convention. Do not write code until you have quoted one real convention from the repo. If the repo already provides the behavior, import it. Do not reimplement it.

Reuse of the existing code went from 0% to 100%. Correctness on the contract-error task went from 0/40 to 40/40, p = 1.9 × 10⁻²³. Pooled across both latent tasks, 0/80 to 47/80, p = 7.8 × 10⁻¹⁹. The gate created the uncertainty the model never felt on its own.

## Result 4: what the active ingredient actually is

I pulled the procedure apart to find which piece did the work. Four versions of the same task at about 40 runs each:

- Buried principle (the original skill): 0/40
- Focused principle, no action: 20/40 (50%)
- How-to step, no gate: 40/40 (100%)
- Hard stop, no how-to: 40/40 (100%)

Either a concrete how-to *or* a blocking gate independently takes discovery to 100%. You do not need both. The focused principle reaching 50% was its own finding: the original skill scored 0 partly because the grounding instruction was diluted inside a long multi-phase document. A tight principle beat a bloated one. A concrete action beat both, every time. Ranking: buried principle 0%, focused principle 50%, any concrete action 100%.

## Result 5: the gate fixes discovery, not comprehension

One clean boundary on what this buys you. On the hardest task, a dedupe-before-validate ordering invariant, the gate took reuse to 100% but correctness only to 18%, 7/40, p = 1.2 × 10⁻². Every agent found and imported the right module. Most still applied it wrong. Forcing "go read the code" is something a hard stop can do. "Correctly apply the ordering rule you just read" is a separate failure the gate does not touch. Discovery and comprehension are two different problems.

## Result 6: it generalizes across model tiers, and the weaker the model the more it helps

The procedure result above was measured on Sonnet. To check it was not a one-model artifact, I ran the same G3 task, control versus the convention procedure, on three tiers under the identical harness, 20 reps each.

| model | control correct | convention correct | Δ | Fisher p |
|---|---|---|---|---|
| Haiku | 1/20 (5%) | 19/20 (95%) | +90pp | 2.9 × 10⁻⁹ |
| Sonnet | 0/20 (0%) | 20/20 (100%) | +100pp | 7.3 × 10⁻¹² |
| Opus | 14/20 (70%) | 19/20 (95%) | +25pp | 4.6 × 10⁻² |

The gate works on all three, significant even on Opus. The interesting part is the shape: the effect size runs *opposite* to model strength. Opus already investigates the codebase unprompted, with 70% of bare Opus runs finding and using the real convention, so the gate has little headroom. Haiku almost never investigates on its own (5%), so the gate nearly transforms it, 5 to 95. A mechanical gate buys the most exactly where the model is weakest. That is the right shape for a scaffold: it stands in for a behavior the strong model already has and the weak model lacks.

## Result 7: the comprehension gap is closable with a second gate

Result 5 left a problem open. On the ordering task the gate took reuse to 100% but correctness stayed near the floor: the agent found and imported the right function and still ran it in the wrong order. So I tested whether a second gate closes it. The convention arm got one extra line. After quoting the convention, state in one sentence the order the functions must run in and what breaks if you reverse it, then write code.

| arm | reuse | correct |
|---|---|---|
| control | 0% | 0% |
| convention (gate) | 100% | 0% |
| convention + order-check | 100% | 85% |

The plain gate reproduced the gap: 20/20 reuse, 0/20 correct, every agent imported the right module and still counted before deduping. Adding the order-articulation step took correctness to 17/20, 85%, p = 1.3 × 10⁻⁸. Making the model spell out what breaks was enough to stop it from breaking that thing. Comprehension responds to a gate the same way discovery does. You just have to gate the right step. Discovery needs "go quote the convention." Comprehension needs "say what breaks if you misuse it."

## What the results say

The shape of a skill decides everything, and the shape that works is an action plus a line the model cannot cross.

A value, like "verify your work" or "ground your work in the codebase," is inert on a competent model and can be harmful on a weak one. The model agrees and keeps its prior. A procedure with a blocking gate, like "do not write code until you have quoted a real convention from the repo," is a behavior change you can measure at p below 10⁻¹⁸.

This is the same thing the literature already reports, reproduced in the medium most of us now actually work in. Intrinsic self-correction with no external signal does not reliably help and sometimes hurts (Huang et al., ICLR 2024). Prompt-level pressure on the model, whether threatening it, tipping it, or urging it, has no reliable aggregate effect either (Meincke et al., Prompting Science Report 3, Wharton 2025). The gains in agentic coding come from scaffolding and tools that force the model to fetch a real signal, not from telling it to try harder (SWE-agent, NeurIPS 2024). A skill is just a prompt-level version of that scaffolding, and it works for the same reason: it makes the model go get the signal instead of asking it to care.

The skill I now keep is the procedure, not the principle. It survived 40 runs. The careful-sounding version did not, and the only reason I know that is that I scaled the test until the data could tell them apart.

## The numbers

False-done rate (claimed DONE, hidden suite failed). Lower is better. The skill never beats control, and on weaker models it loses.

| Condition | Model | control | placebo | skill |
|---|---|---|---|---|
| natural + exec | Haiku | 9/30 | 11/30 | 16/30 |
| natural + real iterate | Sonnet | 8/30 | 6/30 | 8/30 |
| steelman, tests in workspace | Sonnet | 3/30 | 3/30 | 3/30 |
| reasoning-only cloud | Kimi-K2 | 9/30 | 12/30 | 13/30 |
| 80k-token distractor | Sonnet | 6/30 | 6/30 | 7/30 |

Latent-requirement tasks, Sonnet (correctness, and reuse of the host package). The principle is flat against control. Swapping it for the procedure-plus-gate moves both to the ceiling.

| Arm | G3 correct | reuse | note |
|---|---|---|---|
| control | 0/39 | 0% | baseline |
| principle ("ground before you build") | 0/40 | 0% | Fisher p = 1.0 vs control |
| **procedure + hard stop** | **40/40** | **100%** | p = 1.9 × 10⁻²³ |
| how-to step only (no gate) | 40/40 | 100% | ablation |
| hard stop only (no how-to) | 40/40 | 100% | ablation |
| focused principle (no action) | 20/40 | 50% | dilution effect |

On the hardest task (G4, a dedupe-before-validate ordering invariant) the procedure took reuse to 100% but correctness only to 7/40 (18%, p = 1.2 × 10⁻²). Discovery solved, comprehension not yet.

## Methods

**Arms (seven).** Each is a prompt prefix. The body of the task is identical across arms.

- **control**: no prefix.
- **placebo**: "Be careful and verify your work before you say it's done."
- **principle** (the original skill): a multi-phase document whose grounding instruction is "ground your work in the existing codebase," among other phases.
- **procedure + hard stop** (the winner): "Locate the project's package and list its modules… read the module(s) most related to this task… QUOTE the exact file + function that defines the relevant convention… HARD STOP: do not write your solution until you have quoted one existing convention; if the repo already provides the behavior, import it, do not reimplement it."
- **exec_only**: the locate-and-read how-to step, with no hard stop and no reuse mandate.
- **stop_only**: the hard stop and reuse mandate, with no how-to step.
- **verbose_principle**: a length-matched paragraph of "ground before you build" prose, no executable step, no gate. Controls for "just more, more forceful words."

**Tasks.** Ten small Python tasks over a fake newsroom domain (normalize tags, truncate headline, parse ISO date, dedupe articles, slugify, summarize-to-budget, rank by recency, extract domain, merge translations, validate feed item). Each ships a `naive.py` (the plausible wrong version), a `reference.py`, and a hidden `pytest` suite with `test_trap*` cases for the latent requirement. The grounded conditions add a host package (`newsroom/`) that already implements the convention, so the only way to pass the trap is to read and reuse it.

**Execution.** Each cell is (task × arm × rep). The model under test runs the prompt in a real shell, is told it may iterate and test, and returns a solution plus a self-reported DONE/NOT_DONE verdict. Grading is mechanical: write the returned solution and the hidden test into an isolated scratch dir, run `pytest`, parse the JUnit XML. `actually_passed` means every test passed and at least one ran. `traps_caught` means every `test_trap*` passed. Reuse is a regex check for an `import` of the host package in the returned solution.

**Stats.** Wilson score intervals for rates, Fisher exact tests for between-arm differences, cluster bootstrap for the rate difference, Holm correction across conditions. Cells powered to about 40 reps where a condition was load-bearing, 30 reps on the early false-done conditions.

## Limitations

- **Cross-model: confirmed, not assumed (Result 6).** The procedure result holds on Haiku, Sonnet, and Opus, significant on all three. It is strongest on the weakest model. So the effect is not Sonnet-specific, though all four tiers are still one model family.
- **Synthetic tasks.** These are constructed traps with a known latent requirement, not real pull requests. They isolate the effect cleanly at the cost of external validity.
- **One codebase, one language.** Python, one host package. "Quote a convention" should generalize to any language with a greppable source tree, but that is untested here.
- **Reuse overstates correctness.** The G4 result is the proof: 100% of agents imported the right module and only 18% applied it correctly. "It reused the code" is not "it got the answer right."
- **Ablation depth.** The active-ingredient breakdown was run on the cleanest discriminator (G3). Two further probes, a held-out task and a JavaScript port, were run on Sonnet only and are weaker discriminators. In both, bare Sonnet already reused the host package most of the time (95% and 75%), because the task wording or the environment named the relevant module. They confirm the mechanism is language-agnostic and reproduce the ceiling (a strong model with an obviously-relevant package often needs no gate), but they do not isolate the gate effect the way G3 does.
