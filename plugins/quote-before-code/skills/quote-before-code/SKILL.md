---
name: quote-before-code
description: Use when adding or changing behavior in an existing codebase, so the agent reuses what is already there and follows local conventions instead of writing a plausible-but-wrong version from general knowledge. Forces it to find and quote a real convention before writing code. Skip for greenfield code with no surrounding repo.
---

# quote-before-code

When a task looks easy, the model writes the generic version from memory and never
opens the repo - so it reinvents helpers that already exist, picks the wrong exception
type, ignores a validation order, and breaks call sites. A controlled experiment
(~930 graded runs) showed a generic "ground your work in the codebase" *principle*
changed nothing: 0/40 reuse, identical to no skill. An *executable procedure with a
hard stop* took reuse from 0% to 100% on the same tasks. This skill is that procedure.

## The Iron Law

```
DO NOT WRITE CODE UNTIL YOU HAVE QUOTED ONE REAL CONVENTION FROM THE REPO.
```

If the repo already provides the behavior, import it. Do not reimplement it.

## The Procedure

Do this BEFORE writing any implementation. Both steps below independently moved
behavior to 100% in testing; do both.

1. **Find it.** Locate the project's source and read the modules closest to the task.
   `grep -rn` for the relevant symbol (the exception class, the helper, the validator,
   the type) across the source tree — that works in any language. If the entrypoint is
   unclear, start from the manifest (`package.json`, `pyproject.toml`, `go.mod`,
   `Cargo.toml`) to find where the package lives, then read the files nearest the task.

2. **Quote it.** In your reasoning, name the exact file and function/class that
   defines the convention you will follow: the exception type raised, the helper to
   reuse, the validation/ordering rule, the naming pattern, the return shape.

3. **Follow it.** Write the smallest patch that imports or matches what you quoted.

## The Hard Stop

You may not write the solution until step 2 is done. If you cannot quote a real
convention from the repo, you have not looked hard enough - keep reading. "I already
know how to do this" is the exact thought this skill exists to interrupt: the repo's
convention beats your general knowledge every time they disagree.

## What this does and does not fix

- **Fixes "didn't look":** the hard stop forces discovery. This is the whole win.
- **Does NOT fix "looked but misapplied":** finding the right module does not
  guarantee you apply its rule correctly (e.g. an ordering invariant). After quoting
  the convention, re-read it and check your patch against it specifically.

## When to use

Any change to an existing codebase where the correct behavior may depend on local
conventions. **Skip** for genuinely greenfield code with no surrounding repo to read.

## Keep it sharp

This works because it is short and concrete. Do not bury the procedure inside a long
multi-phase process - in testing, the same instruction buried in a big skill scored
0%, focused scored 50%, and as a standalone hard-gated procedure scored 100%.
