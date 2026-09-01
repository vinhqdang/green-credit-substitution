# Peer Review Report — Third Pass (v3)

**Manuscript:** "Credible on Paper? Green Banking Policy, Access to Finance, and Institutional Capacity in the Greening of Firms Worldwide"
**Reviewed for:** *Economic Systems* (Elsevier) — Special Issue, "Governing the Green Transition as System Change"
**Review mode:** `academic-paper-reviewer`, re-review (verification) + independent critique of the major new Section 6 addition
**Prior reviews:** `output/review_cfp_fit_2026-09.md` (round 1), `output/review_cfp_fit_2026-09_v2.md` (round 2)
**Basis:** `latex/manuscript.tex` recompiled fresh for this review (pdflatex + bibtex, 3 passes) and cross-checked against the resolved `manuscript.aux`, not against the change log I was given
**Constraint:** Read-only pass. No manuscript edits made as part of producing this report.

---

## Headline

Round 2's table-numbering fix holds under the new Section 6 addition — verified directly, not assumed. The code/file-language cleanup from the two ad hoc passes is genuinely clean across the whole manuscript, not just the spots explicitly mentioned in the change log. The new Section 6 is sound, honestly reported applied econometrics with one real completeness gap (only one control-group specification reported) and, more importantly, **one specific terminology imprecision that recurs in two places (Discussion and Conclusion): the paper calls Section 6's finding a null on "institutional moderation," but Section 6 tests a main effect (does adoption move a country outcome), not a moderation effect (does adoption change a firm-level slope) — the same distinction the paper itself is otherwise careful about.** This is fixable in about two sentences and does not undermine the underlying analysis, but it is exactly the kind of imprecision a sharp reviewer would flag, and it currently sits in the two most-read parts of the paper.

---

## Part A — Verification (not assumed from the change log)

### A1. Table-numbering fix: holds. Verified via `manuscript.aux`, not via memory of round 2.

I deleted all LaTeX auxiliary files and recompiled from scratch (pdflatex → bibtex → pdflatex ×2). Resolved numbers: `tab:baseline`=3, `tab:multilevel`=4, `tab:causalforest`=5, `tab:sizecate`=6, `tab:extension`=7, `tab:fdr`=8, `tab:robustness`=9, `tab:global`=10, `tab:macrodid`=**11** (the new Table 11, correctly the last main-body table); `fig:macroevent`=**6** (correctly the last main-body figure); `sec:macrodid`=**6**, `sec:discussion`=**7**, `sec:conclusion`=**8**. A full sweep of the source for hardcoded `Table N` / `Section N` / `Figure N` mentions not using `\ref{}` returned zero hits. The new Section 6 material did not reopen the numbering bug round 2 found — it was added entirely through `\ref{}`, correctly.

### A2. Code/file-language sweep: clean, independently re-verified.

I ran my own sweep (not the one described in the change log) across `latex/manuscript.tex` and every `manuscript/*.md` file for `.csv`/`.py`/`.txt`, `github`, `script`, `fetched`, `API key`, `endpoint`, `pandas`/`numpy`/`dataframe`, `import`, and similar markers. Every hit resolved to one of two categories: (a) a substring false positive (`script` inside `manuscript`), or (b) the Data Availability statement and AI-disclosure paragraph, where naming a GitHub repository and replication code is the expected convention, not a leak of implementation detail into the science. No residual file paths, API-key-style details, or code-flavored verbs remain in the body text. The two ad hoc passes described in the change log actually worked; I am not taking that on faith.

### A3. Compile health: clean.

75 pages (up one from the 74 reported in the change log — consistent with ordinary reflow from the two small text edits since, not a sign of anything wrong). No undefined references, no LaTeX errors, no overfull-hbox warnings beyond the pre-existing ones already noted in round 2 (long tables, none newly introduced by Section 6 beyond the already-fixed Table 11).

---

## Part B — Section 6 on its own merits (new critique, not in either prior round)

### B1 (MAJOR): "institutional moderation" is the wrong word for what Section 6 tests, and this recurs in the two places readers are most likely to take away the paper's headline claim

Section 6 tests whether SBFN adoption shifts a **country's aggregate environmental trajectory** — a main effect of the policy itself. This is a different hypothesis from H2/H3, which ask whether SBFN adoption **moderates the firm-level credit-to-green slope**. The paper is careful about this distinction inside Section 6.2 itself ("does not support treating SBFN adoption as a country-level lever that visibly improves aggregate environmental outcomes" — correctly a main-effect framing) and in the Introduction's sixth contribution point ("does not support a beneficial institutional effect" — also correctly framed). But in exactly the two places most likely to be read as the paper's final word — the new Discussion paragraph introducing Section 6, and the Conclusion's "Fifth" result — the text says:

> "...is, we think, the single hardest-to-dismiss piece of evidence in the paper that **the null on institutional moderation** is a real feature of how SBFN adoption relates to environmental outcomes..." (Discussion)

> "...likewise finds no clean evidence that SBFN adoption improves aggregate environmental outcomes---the single strongest piece of evidence in the paper that **the null on institutional moderation** is a real feature of how this policy relates to outcomes..." (Conclusion)

A reader who has just absorbed five sections of H2/H3 moderation-testing will reasonably parse "the null on institutional moderation" in these two sentences as "Section 6 also found no moderation effect" — which is not what Section 6 tested. This is not a fatal flaw in the underlying econometrics; it is a terminology slip in exactly the two sentences a skimming guest editor is most likely to read closely (the paragraph introducing a new section, and a numbered results list in the Conclusion). **Fix:** replace "the null on institutional moderation" with "the null on a beneficial institutional effect" (or equivalent) in both spots; the surrounding argument does not need to change, only these two phrases.

### B2 (MINOR/MAJOR, methodological completeness): only one control-group specification is reported

The Callaway-Sant'Anna implementation used supports both `never_treated` and `not_yet_treated` control groups; the paper reports only the former. This is a defensible default (it is the more conservative choice, and the paper's covariate-adjustment logic — netting out the development-stage confound — applies to it cleanly), but a methodology-focused reviewer will likely ask why the alternative wasn't shown as a robustness check, particularly given the paper's own house style elsewhere is to report multiple specifications side by side precisely to pre-empt this question (Table 4's M1-M3, Table 8's five robustness checks, Table 9's with/without-FE columns). Section 6 breaks that pattern by reporting only one control-group choice. **Fix, if feasible:** add the `not_yet_treated` specification as a third column in Table 11, or note explicitly in 6.1 why it was not pursued (e.g., insufficient not-yet-treated mass in the earliest cohorts).

### B3 (MINOR, writing craft): the "we are not spinning this" rhetorical pattern is now doing double duty across the paper and starting to read as a tic

Phrases functionally identical to "we are deliberately not spinning this into either X or Y" now appear at least three times across the paper in slightly different words (the overdraft-interaction discussion in Section 5.6/Discussion, the "no interaction ≠ no complementarity" paragraph, and Section 6.2's explicit statement). Each instance is individually well-motivated and I would not cut any one of them in isolation — but three uses of the same rhetorical move within one paper starts to read as protesting rather than reporting, to a reviewer reading start to finish rather than section by section. This is a polish item, not a substance item: consider varying the phrasing, or trusting the reader to draw the "don't overclaim" conclusion once it has been modeled clearly the first time.

### B4 (Observation, not a defect): the core econometric choices in Section 6 are sound

The never-treated comparison group, the doubly-robust log-GDP-per-capita specification, the explicit naive-TWFE comparison to illustrate (not to adopt) the known staggered-timing bias, and — most importantly — the honest reporting of the CO2 result as *shrinking* substantially and *not* being read causally, are all defensible and, I think, actually well-executed applied microeconometrics. I specifically checked whether the renewables null is doing more argumentative work than it can bear ("does the null on renewables really support 'converges with firm-level findings'"): it does, but only for the narrower, correctly-scoped claim ("no clean evidence of a beneficial main effect on this outcome"), not for the broader "no institutional moderation" claim flagged in B1. Once B1 is fixed, I do not think the renewables result is overclaimed.

---

## Part C — Fresh Special Issue Fit verdict

**Verdict: upgraded from round 2's "marginal fit, same structural risk, better-argued case" to good fit, contingent on the B1 fix.**

The reasoning for the upgrade: round 1's CRITICAL finding was that the paper's identification strategy did not match any of the CFP's named design classes. That is no longer true. Section 6 is a genuine staggered-adoption Callaway-Sant'Anna event-study, on the exact SBFN policy-timing variation the rest of the paper is about, using an independent public data source, with a properly-specified never-treated comparison group and an explicit illustration of why the naive alternative (TWFE) would be wrong. A guest editor applying the CFP's own stated bar — "we welcome... staggered DID/event studies... submissions must... empirically test institutional or systemic mechanisms" — now has an actual instance of the named design to point to, not an argument for why one isn't needed.

The one thing that keeps this from being an unqualified "good fit, no caveats" verdict is B1: as currently worded, the paper's own Discussion and Conclusion risk letting a reader conflate "Section 6 found no main effect" with "Section 6 replicates the H2/H3 moderation null," which is a stronger and less accurate claim than the data supports. This is a two-sentence fix, not a design flaw, and I would not want it to be mistaken for a reason to discount the underlying analysis — but it should be fixed before submission, precisely because it sits in the two places a guest editor doing an initial screen is most likely to read closely.

---

## Part D — Coherence and length

At 75 pages (double-spaced, line-numbered review manuscript), the paper is long even by generous review-stage standards, but I do not think it reads as an unfocused accumulation of every possible check. The organizing logic — the same underlying question (does state capacity/policy credibility condition a financial-institutional effect?) tested at two levels of analysis (firm, then country) and, within the firm level, across four estimators of increasing methodological sophistication — is legible and consistently signposted (the paper repeatedly tells the reader why each new stage exists, e.g. "we report this specification... precisely to make that limitation visible"). Section 6 in particular does not feel bolted on: it directly answers a limitation the paper itself raised in Section 4.1, and its placement (a distinct Section 6, not a buried Results subsection) correctly signals that it is a different kind of test rather than one more firm-level robustness row.

That said, length is a real Journal-Fit consideration independent of coherence. Table 8's five-row robustness battery and the appendix's full 47-economy and 162-region sourcing tables are candidates for tighter online-supplementary treatment if the guest editors or a later-round reviewer push back on manuscript length; I would not pre-emptively cut them now; I would have the author be ready to.

---

## Summary Table

| Dimension | Round 2 | Round 3 (this pass) |
|---|---|---|
| Table-numbering self-consistency | Fixed | Re-verified holds under the Section 6 addition (checked `manuscript.aux` fresh, not assumed) |
| Code/file-language leakage | Two spots fixed | Independently re-swept, confirmed clean paper-wide |
| Identification-strategy gap (round-1 CRITICAL) | Better disclosed, not resolved | **Resolved**: Section 6 supplies an actual staggered-adoption design on the CFP-relevant variation |
| New finding: "institutional moderation" vs. main-effect terminology | N/A (section didn't exist) | **MAJOR, two-sentence fix, recurs in Discussion + Conclusion** |
| New finding: single control-group specification | N/A | MINOR/MAJOR completeness gap, addressable with a robustness column |
| New finding: repeated "not spinning this" rhetoric | N/A | MINOR polish |
| Special Issue Fit | Marginal, better-argued | **Good fit, contingent on the B1 fix** |
| Editorial decision (general) | Minor (contingent on table-numbering fix) | Minor (contingent on the B1 terminology fix; everything else is polish) |
