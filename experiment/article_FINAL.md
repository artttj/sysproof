# What actually makes a coding-agent skill work: 930 controlled runs

I was curious.

I already use a few skills when I work with coding agents: **systematic debugging**, **test-driven development**, and a **brainstorming pass before touching code**. They genuinely change how the sessions go, so I wanted to know what else was worth adding.

The target was the failure every coding agent has: **finishing most of a task, declaring victory, and skipping the part that mattered.**

I wrote a skill to attack it. It told the agent two things: verify your work before you say "done," and read the existing code before writing anything new. Both sounded obviously useful. Instead of trusting that feeling, I built a harness to measure whether the skill actually changed anything.

**The measurement became the whole story.**

**I. How I tested it**

The setup was a controlled A/B experiment, not a vibe check. Same tasks, same model, same grading. The only thing that changed between arms was the prompt body.

The study started with three arms and grew to seven as I chased the part that actually mattered:

• **control:** the bare task
• **placebo:** "be careful, verify your work"
• **full skill:** verify first, read code first

A hidden test suite graded every run mechanically, so nothing depended on whether the output "looked done."

I tracked two metrics: **false-done rate**, where the agent claimed DONE but the hidden suite failed, and **task-correct rate**, where the agent satisfied requirements that existed only in the codebase, never in the prompt.

I powered the important cells to about 40 runs each, then ran Wilson intervals, Fisher exact tests, cluster bootstraps, and Holm correction across conditions. The final study covered **12 conditions, about 930 graded runs, and three model tiers.**

**II. Result 1: the careful skill did nothing**

Across the first six conditions, the skill sat on top of control.

On Sonnet with real iteration it was an exact null: **8/30 false-done for control, 8/30 for the skill.**

On weaker models it was worse. Haiku went from **9/30 in control to 16/30 with the skill**, and a Kimi cloud model moved the same way.

The verbose "be careful" text did not make weaker models more careful. It made them more willing to say DONE, which reduced the honest NOT_DONE answers they would otherwise give.

The only thing that ever moved false-done had nothing to do with the skill.

When I put visible acceptance tests in the workspace, false-done dropped from about **27% to about 10%**, identically across all three arms.

**The lever was test presence, not prompt pressure.**

A capable model that can run its own code is already trying to verify. Telling it to verify adds nothing it was not already doing.

**III. Result 2: a promising redesign disappeared under power**

So I rewrote the skill.

Instead of putting verification at the end, I put investigation at the start: **research the codebase first.**

The new tasks were harder. The real requirement was hidden in the codebase and never stated in the prompt.

On a quick 10-run pass, the redesign looked promising: **60% correct against 45% for control.** That was the moment the experiment became useful.

I scaled the cleanest discriminator, a contract-error task, to about 40 runs per arm. The win disappeared:

**skill:** 0/40
**control:** 0/39
**Fisher p:** 1.0

In all 40 skill runs, the agent never once mentioned the code it needed, even though the prefix was present in every prompt and the module was importable.

**The early win was noise.**

There was no harness bug. The skill text was present and the code was reachable. The agent read "raise an error if the field is missing," decided it already knew what that meant, wrote the generic version, and moved on.

**A principle does not override a prior.**

The model had no reason to go look, so it did not.

**IV. Result 3: a procedure with a hard stop changed everything**

A principle-style skill being inert does not mean skills are inert.

So I changed one variable. Same task, same model, same **0/40 baseline**.

Instead of a value like "ground your work in the codebase," I wrote a procedure with a blocking gate:

**Locate the project package, read its modules, quote the exact function that defines the convention. Do not write code until you have quoted one real convention from the repo. If the repo already provides the behavior, import it. Do not reimplement it.**

Reuse of the existing code went from **0% to 100%.**

Correctness on the contract-error task went from **0/40 to 40/40**, with **p = 1.9 × 10⁻²³.**

Pooled across both latent tasks, correctness moved from **0/80 to 47/80**, with **p = 7.8 × 10⁻¹⁹.**

The gate created the uncertainty the model never felt on its own.

**V. Result 4: the active part is action, not tone**

I pulled the procedure apart to find which piece did the work.

Four versions of the same task, about 40 runs each:

• **buried principle, the original skill:** 0/40
• **focused principle, no action:** 20/40
• **how-to step, no gate:** 40/40
• **hard stop, no how-to:** 40/40

Either a concrete how-to or a blocking gate independently took discovery to 100%. You do not need both.

The focused principle reaching 50% was its own lesson. The original skill scored 0 partly because the grounding instruction was buried inside a long multi-phase document.

A tight principle beat a bloated one, and a concrete action beat both.

The ranking was clean:

**buried principle:** 0%
**focused principle:** 50%
**concrete action:** 100%

**VI. Result 5: the gate fixes discovery, not comprehension**

There is a sharp limit on what this buys you.

On the hardest task, a **dedupe-before-validate ordering invariant**, the gate took reuse to 100% but correctness only to **18%**, or **7/40**, with **p = 1.2 × 10⁻².**

Every agent found and imported the right module. Most still applied it in the wrong order.

Forcing "go read the code" is something a hard stop can do. Correctly applying the rule after reading it is a different failure.

**Discovery and comprehension are separate problems.**

**VII. Result 6: the effect generalizes across model tiers**

The procedure result was first measured on Sonnet. I then ran the same G3 task, control against the convention procedure, on three model tiers under the same harness, 20 reps each.

**Haiku**
Control correct: **1/20, 5%**
Convention correct: **19/20, 95%**
Change: **+90 percentage points**
Fisher p: **2.9 × 10⁻⁹**

**Sonnet**
Control correct: **0/20, 0%**
Convention correct: **20/20, 100%**
Change: **+100 percentage points**
Fisher p: **7.3 × 10⁻¹²**

**Opus**
Control correct: **14/20, 70%**
Convention correct: **19/20, 95%**
Change: **+25 percentage points**
Fisher p: **4.6 × 10⁻²**

The gate worked on all three, significant even on Opus.

The interesting part was the shape: **the effect size moved opposite to model strength.**

Opus already investigated the codebase unprompted in many bare runs, with 70% finding and using the real convention, so the gate had less room to help. Haiku almost never investigated on its own, only 5%, and the gate nearly transformed it, from 5% to 95%.

That is what a good scaffold should do.

It replaces a behavior the strong model already has and the weak model lacks.

**VIII. Result 7: the comprehension gap is closable with a second gate**

Result 5 left a problem open.

On the ordering task, the gate took reuse to 100% but correctness stayed near the floor. The agent found and imported the right function, then ran it in the wrong order.

So I tested whether a second gate could close the gap.

The convention arm got one extra line: **after quoting the convention, state in one sentence the order the functions must run in and what breaks if you reverse it, then write code.**

The result:

**control**
reuse: 0%
correct: 0%

**convention gate**
reuse: 100%
correct: 0%

**convention plus order-check**
reuse: 100%
correct: 85%

The plain gate reproduced the gap: **20/20 reuse, 0/20 correct.** Every agent imported the right module and still counted before deduping.

Adding the order-articulation step moved correctness to **17/20**, or **85%**, with **p = 1.3 × 10⁻⁸.**

Making the model spell out what breaks was enough to stop it from breaking that thing.

Comprehension responds to a gate the same way discovery does. You just have to gate the right step.

Discovery needs: **go quote the convention.**

Comprehension needs: **say what breaks if you misuse it.**

**IX. What the results say**

The shape of a skill decides whether it works.

The working shape is simple: **an action plus a line the model cannot cross.**

A value like "verify your work" or "ground your work in the codebase" is weak. On a competent model it can be inert, and on a weaker one it can make things worse by producing more confident DONE claims.

The model agrees with the instruction, then keeps its prior.

A procedure with a blocking gate changes behavior:

**do not write code until you have quoted a real convention from the repo.**

That is not a vibe. It is measurable. In this setup, it moved correctness at **p below 10⁻¹⁸.**

This matches the broader pattern in the literature. Intrinsic self-correction without external feedback does not reliably help and can degrade performance. Prompt-level pressure, whether you threaten the model, tip it, or urge it to try harder, has no reliable aggregate effect. The stronger gains in agentic coding come from scaffolds and tools that force the model to fetch a real signal.

A coding-agent skill is a prompt-level scaffold, and it works for the same reason:

**it makes the model go get the signal instead of asking it to care.**

The skill I now keep is the procedure, not the principle.

The careful-sounding version did not survive measurement. The gated version did.

The only reason I know the difference is that I scaled the test until the data could separate them.

**X. The numbers**

**False-done rate**

Claimed DONE, hidden suite failed. Lower is better.

The skill never beats control, and on weaker models it loses.

**Natural plus exec, Haiku**
control: 9/30
placebo: 11/30
skill: 16/30

**Natural plus real iterate, Sonnet**
control: 8/30
placebo: 6/30
skill: 8/30

**Steelman, tests in workspace, Sonnet**
control: 3/30
placebo: 3/30
skill: 3/30

**Reasoning-only cloud, Kimi-K2**
control: 9/30
placebo: 12/30
skill: 13/30

**80k-token distractor, Sonnet**
control: 6/30
placebo: 6/30
skill: 7/30

**Latent-requirement tasks, Sonnet**

Correctness and reuse of the host package.

The principle is flat against control. Swapping it for the procedure plus gate moves both to the ceiling.

**control**
G3 correct: 0/39
reuse: 0%
note: baseline

**principle, "ground before you build"**
G3 correct: 0/40
reuse: 0%
note: Fisher p = 1.0 vs control

**procedure plus hard stop**
G3 correct: 40/40
reuse: 100%
note: p = 1.9 × 10⁻²³

**how-to step only, no gate**
G3 correct: 40/40
reuse: 100%
note: ablation

**hard stop only, no how-to**
G3 correct: 40/40
reuse: 100%
note: ablation

**focused principle, no action**
G3 correct: 20/40
reuse: 50%
note: dilution effect

On the hardest task, G4, the procedure took reuse to **100%** but correctness only to **7/40**, or **18%**, with **p = 1.2 × 10⁻².**

Discovery was solved. Comprehension was not.

**XI. Methods**

**Arms**

Each arm is a prompt prefix. The task body is identical across arms.

• **control:** no prefix
• **placebo:** "Be careful and verify your work before you say it's done."
• **principle:** the original multi-phase skill, with "ground your work in the existing codebase" buried among other phases
• **procedure plus hard stop:** locate the project package, list its modules, read the relevant modules, quote the exact file and function that defines the convention, then write code
• **exec_only:** the locate-and-read how-to step, with no hard stop and no reuse mandate
• **stop_only:** the hard stop and reuse mandate, with no how-to step
• **verbose_principle:** length-matched "ground before you build" prose, with no executable step and no gate

**Tasks**

Ten small Python tasks over a fake newsroom domain: normalize tags, truncate headline, parse ISO date, dedupe articles, slugify, summarize to budget, rank by recency, extract domain, merge translations, and validate feed item.

Each ships a naive.py, a reference.py, and a hidden pytest suite with test_trap cases for the latent requirement.

The grounded conditions add a host package, newsroom/, that already implements the convention, so the only way to pass the trap is to read and reuse it.

**Execution**

Each cell is task × arm × rep.

The model runs the prompt in a real shell, may iterate and test, and returns a solution plus a self-reported DONE or NOT_DONE verdict.

Grading is mechanical: write the returned solution and the hidden tests into an isolated scratch directory, run pytest, parse the JUnit XML.

**actually_passed** means every test passed and at least one ran.

**traps_caught** means every test_trap case passed.

Reuse is a regex check for an import of the host package in the returned solution.

**Stats**

Wilson score intervals for rates, Fisher exact tests for between-arm differences, cluster bootstrap for the rate difference, and Holm correction across conditions.

Load-bearing cells were powered to about 40 reps. Early false-done conditions used 30.

**XII. Limitations**

**Cross-model, confirmed but not universal**

The procedure result holds on Haiku, Sonnet, and Opus, significant on all three, and strongest on the weakest model.

That means the effect is not Sonnet-specific. It does not mean it automatically generalizes to every model family.

**Synthetic tasks**

These are constructed traps with a known hidden requirement, not real pull requests.

That isolates the effect cleanly but limits external validity.

**One codebase, one language**

The main study uses Python and one host package.

"Quote a convention" should transfer to any language with a searchable source tree, but that is not proven here.

**Reuse overstates correctness**

The G4 result is the warning label:

**100% of agents imported the right module. Only 18% applied it correctly.**

"It reused the code" is not the same as "it got the answer right."

**Ablation depth**

The active-part breakdown was run on the cleanest discriminator, G3.

Two further probes, a held-out task and a JavaScript port, were run on Sonnet only and were weaker discriminators. In both, bare Sonnet already reused the host package most of the time, **95% and 75%**, because the task wording or environment named the relevant module.

They support the mechanism and reproduce the ceiling effect, but they do not isolate the gate effect as cleanly as G3.