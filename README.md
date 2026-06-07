# quote-before-code

[![version](https://img.shields.io/badge/version-v1.0.1-blue)](https://github.com/artttj/quote-before-code/releases) [![runs](https://img.shields.io/badge/runs-930-orange)](https://github.com/artttj/quote-before-code/blob/main/experiment/MASTER_SUMMARY.txt) [![p--value](https://img.shields.io/badge/p-1.9%C3%9710%E2%81%BB%C2%B3-green)](https://github.com/artttj/quote-before-code/blob/main/experiment/article_FINAL.md) [![license](https://img.shields.io/badge/license-MIT-gray)](https://github.com/artttj/quote-before-code/blob/main/LICENSE)

A Claude Code skill that forces a coding agent to find and quote a real convention from your repo before it writes any code. One rule runs it:

> **Do not write code until you have quoted one real convention from the repo.**

This repo is two things: the skill, and the controlled experiment that decided its exact shape. The numbers below are why the skill reads the way it does.

## The problem it fixes

When a task looks easy, an agent writes the generic version from memory and never opens your repo. So it reinvents a helper that already exists, raises the wrong exception type, ignores a validation order, and breaks call sites that depended on the local convention. The requirement was sitting in the code. The agent was too sure of itself to go look.

## What the experiment found

I started with the opposite skill: a careful-sounding principle that told the agent to verify its work and to ground itself in the codebase. Then I tested whether it did anything. The study is 12 conditions, about 930 mechanically graded runs, three model tiers.

- **Principle-style skills are inert.** "Verify before done" and "ground your work in the codebase" matched a bare control across every fair condition. On a weaker model the verbose skill was worse, because it pushed confident DONE declarations and suppressed honest hedging.
- **A promising redesign died under power.** Front-loading "research the codebase first" led the control at n=10 (60% vs 45% correct). Scaled to 40 runs per arm the win vanished completely: 0/40 versus control 0/39, Fisher p = 1.0. In all 40 runs the agent never once opened the code it needed, even though the module was importable and the instruction was in every prompt.
- **A procedure with a hard stop changed everything.** Swapping the principle for an executable step plus a blocking gate — "locate the package, read it, quote a real convention, and do not write code until you have" — took reuse of the existing code from **0% to 100%** and correctness on a latent-requirement task from **0/40 to 40/40** (p = 1.9 × 10⁻²³; pooled across tasks p = 7.8 × 10⁻¹⁹).
- **Either ingredient alone is enough.** Ablation: the same instruction buried in a long multi-phase skill scored 0%, a focused principle scored 50%, and either a concrete how-to or the hard stop alone scored 100%. Dilution was part of why the original failed.
- **The gate fixes discovery, not comprehension.** On the hardest task, the gate got the agent to read the right module 100% of the time but it still applied the rule correctly only 18% of the time. "Didn't look" and "looked but misapplied" are two different failures, and a hard stop only solves the first.

This lines up with the literature: intrinsic self-correction with no external signal does not reliably help and can hurt (Huang et al., ICLR 2024), and the gains in agentic coding come from scaffolding that makes the model fetch a real signal (SWE-agent, NeurIPS 2024). The skill is a prompt-level version of that scaffolding.

The takeaway, and the reason this skill exists: **write skills as an action plus a line the model cannot cross, not as a value.** "Ground your work" is noise. "Do not write code until you have quoted a real convention" is a behavior change you can measure at p below 10⁻¹⁸.

The full write-up is in [`experiment/article_FINAL.md`](experiment/article_FINAL.md). The condition-by-condition numbers are in [`experiment/MASTER_SUMMARY.txt`](experiment/MASTER_SUMMARY.txt).

## Install

```
/plugin marketplace add artttj/quote-before-code
/plugin install quote-before-code@quote-before-code
```

Or drop the skill in by hand:

```bash
git clone https://github.com/artttj/quote-before-code.git
mkdir -p ~/.claude/skills/quote-before-code
cp quote-before-code/plugins/quote-before-code/skills/quote-before-code/SKILL.md ~/.claude/skills/quote-before-code/
```

It triggers on its own when you change behavior in an existing codebase. Skip it for genuinely greenfield code with no surrounding repo to read.

## What's inside

```
plugins/quote-before-code/skills/quote-before-code/SKILL.md   the skill: the Iron Law, the procedure, the hard stop
experiment/
  article_FINAL.md        the write-up
  MASTER_SUMMARY.txt      every condition, with stats
  results_*.csv           the graded data per condition
  *_runs.json             raw run records
  harness/                arms, grader, reuse check, task loader
  tasks/                  the 10 graded tasks
  hostrepo/newsroom/      the host package agents were meant to reuse
  analysis.py             Wilson intervals, Fisher tests, bootstraps
```

## Reproduce

```bash
cd experiment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 analysis.py        # re-derive the stats from the committed run data
```

## License

MIT
