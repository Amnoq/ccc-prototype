# Ledger item 2 — independent verification report

Date: 2026-10-09 (checked 00:15–00:35 UTC).
Item: `zeta-23-lean formalization compiles sorry-free with standard axioms only`,
outcome_class `computationally_verified`, p_ai_2 = 0.75 (Claude, shown arm), result pending.
Prior status: "self-reported pass, build unreproduced, unscored."
Delegation: 2026-10-08 the router withdrew from the prediction loop; the machine
runs verification end-to-end; his word remains final over any rendered outcome.

## What was checked

Repo: `github.com/anthropics/formal-math` (public; `anthropics/zeta-23-lean` redirects here).
Main HEAD at check time: `e1a4e6508154ea59f030480661590a9fe3018011` (2026-10-06T04:00:29Z).
The `zeta23/` subtree was last touched by `2bafb8c88f` (2026-08-28, "Merge pull request
#24"); every later commit touches only `3sum-apsp/` (new dir, added 2026-10-06),
`.github/` CI config, or LICENSE. So the current `zeta23/` tree is the tree CI
verified — see below.

### 1. Independent static audit of the current sources (this run)

- `sorry` tokens: 28 total across `zeta23/`. 25 are the deliberate placeholder proofs
  in the trusted challenge statement files (`Challenge.lean`, `Challenge/XiPrime.lean`)
  — documented as deliberate in `Challenge.lean:26` ("the `sorry`s below are deliberate
  (this is the challenge side)"). The remaining 3 are inside `--` comments in
  `Zeta23/FromPNTPlus/StrongPNTPrefix.lean` ("sorry-free prefix, truncated before …")
  and `Mertens.lean` ("the sorry'd E₁Λ.bounded … is not ported; no sorry enters").
  Zero `sorry` in compiled code under `Zeta23/` or `Solution/`. Zero `admit` anywhere.
- `axiom` declarations: the only code-adjacent hits are `axiom qc : ℚ` /
  `axiom hqc : qc = 2*qc` inside the `/- … -/` docstring of the
  `additive_combination` tactic file (`Zeta23/FromPNTPlus/Tactic/AdditiveCombination.lean:183-184`)
  — inert doc text, not compiled. Zero project axioms in compiled code. Matches the
  repo's own AUDIT.md count.
- `comparator.json` permits exactly `[propext, Quot.sound, Classical.choice]`
  (Lean's three standard axioms); `comparator-xiprime.json` the same. 17 headline
  theorems listed (`two_thirds_on_critical_line`, `five_sixths_distinct`,
  `montgomery_taylor_*`, Dirichlet variants, each + `_cumulative`).
- Toolchain pins: `leanprover/lean4:v4.33.0-rc2`, Mathlib `51e6992efd06126df61a496bebf8f49482a4e129`.

### 2. Third-party-infrastructure machine build (GitHub Actions, public logs)

Workflow `Lean projects` (`.github/workflows/lean-projects.yml`), run `33213372463`
(2026-08-28, push of `2bafb8c88f` — the last commit touching `zeta23/`):
job `verify (zeta23)` = SUCCESS. Per the workflow definition that job:
1. installs elan from the repo's own `lean-toolchain`,
2. fetches the Mathlib prebuilt cache for the pinned rev (pushes to main build from scratch),
3. runs `lake build` and fails on any `sorry` outside the trusted Challenge statement files,
4. runs the Palomar comparator (`leanprover/comparator` at pinned commit
   `575674928e2…`, toolchain-matched `lean4export`, the **independent nanoda kernel**,
   landrun sandbox): every declared comparator configuration must be accepted
   ("Your solution is okay!").

The repo's own `zeta23/AUDIT.md` records the same run's results: `lake build`
8890 jobs, no errors, no sorry warnings; `#print axioms` on all comparator
statements → exactly `[propext, Classical.choice, Quot.sound]`; no `sorryAx`.

Later main commits (dependabot CI bump `fbdc36bbf1`; `3sum-apsp` addition
`e1a4e65081`, CI-verified green itself) do not touch `zeta23/`, so this
verification covers the current tree.

The one failing run visible today (`37821853938`, 2026-10-08) is a **fork's**
PR (`creelie/formal-math`, "Merge pull request #1 from anthropics/main"),
failing in 11 seconds — unrelated to base-repo main, which is green.

## Epistemic label

NOT a local independent reproduction: this environment has no Lean toolchain
installed and git egress is proxy-blocked (403 on CONNECT), so `lake update` /
a from-scratch local `lake build` could not be run here. What this is:
**(a)** an independent static audit of the actual sources (not the author's claims),
plus **(b)** a machine build on third-party infrastructure (GitHub Actions) with
an independent proof kernel (nanoda via the comparator), on the exact pinned tree,
with public logs anyone can re-inspect. That is one full tier above the prior
"self-reported pass": the author's laptop is no longer the only machine that ran it.

Remaining gold-standard step (not done): a `lake build` in our own
Lean-capable environment. Blocked here by git egress; feasible wherever the
toolchain can be installed.

## Recommendation for the render

The predicted class — compiles sorry-free with standard axioms only — is now
supported by two machine paths (independent static audit; third-party CI with
independent kernel). A defensible machine render is `result = 1` with the caveat
above recorded verbatim. The render itself is the main agent's call; per the
2026-10-08 delegation his word remains final and overrides on request.
