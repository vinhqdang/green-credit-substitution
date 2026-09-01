# Peer Review Report — Re-Review / Verification Pass (v2)

**Manuscript:** "Credible on Paper? Green Banking Policy, Access to Finance, and Institutional Capacity in the Greening of Firms Worldwide"
**Reviewed for:** *Economic Systems* (Elsevier) — Special Issue, "Governing the Green Transition as System Change: State Capacity, Policy Credibility, and Institutional Complementarities in Emerging and Transition Economies"
**Review mode:** `academic-paper-reviewer`, re-review (verification of round-1 fixes) + independent critique of newly-added material
**Prior review:** `output/review_cfp_fit_2026-09.md` (round 1, full panel)
**Basis:** current `latex/manuscript.tex` (recompiled with pdflatex + bibtex — see Finding V-1 below for what that compile actually revealed), `manuscript/*.md`, `PROGRESS.md`'s change log, `data/processed/table10_multiple_testing_correction.csv`, `src/compute_fdr_interactions.py`
**Constraint:** Read-only pass. No manuscript edits made as part of producing this report.

---

## Headline

Round 1's substantive findings were, on inspection, genuinely addressed rather than hedge-dressed — this is not a rubber-stamp verdict, see the item-by-item matrix below. But the round of fixes introduced one new, verifiable, and non-trivial defect: **inserting the new multiple-testing-correction table shifted the LaTeX auto-numbering of every table after it, and the new table's own rows hardcode the *old* table numbers as plain text rather than using cross-references — so the compiled PDF's Table 10 currently cites itself and its neighbors by the wrong numbers.** This also exposed a **pre-existing, unrelated numbering bug** in the original manuscript (predating this entire review cycle) that neither round-1 review nor the original authors caught. Full detail in Finding V-1; it is the most important thing in this report because it is not a judgment call — I recompiled the PDF and read the resolved page/table numbers directly out of the `.aux` file, so this is a verified defect, not a stylistic guess.

---

## Part A — Verification of Round-1 Findings

| # | Round-1 finding | Verdict | Evidence |
|---|---|---|---|
| 1 (CRITICAL) | Identification-strategy mismatch with CFP; staggered-DID gap left implicit | **PARTIALLY ADDRESSED — transparency fixed, substance unchanged (as disclosed)** | A genuine, well-argued paragraph was added (`latex/manuscript.tex` §4.1, the "A natural alternative..." paragraph) explaining why a staggered DID/event-study is infeasible with WBES's one-off Green Economy module fielding. This directly answers round 1's *specific* ask ("either mount it or explicitly justify why not"). It does not, and cannot, make the paper's identification strategy causal — it was never going to, given the disclosed data constraint — so the *underlying* special-issue-fit risk is reduced but not eliminated. See Part C for the updated verdict. |
| 2 | Broken cross-reference (Discussion cited Section 2 for content that lives nowhere) | **FULLY ADDRESSED** | The panel-infeasibility discussion now genuinely lives in §4.1 (`sec:methodology`), and the Conclusion's Limitation 1 cross-reference was corrected to point there (`\ref{sec:methodology}` instead of `\ref{sec:institutions}`). Verified by reading both ends of the reference. |
| 3 | Causal-sounding language on H1 | **FULLY ADDRESSED** | Abstract already read "associated" pre-fix and was left correctly hedged; the Discussion's opening sentence, which round 1 specifically flagged, now reads "is associated with an adoption probability roughly 13 percentage points higher... not a causally identified effect" (line 522). Highlights bullet changed from "raises" to "is associated with." Consistent across all three locations checked. |
| 4 | Causal forest "causal"/CATE overclaim | **FULLY ADDRESSED** | New sentence in §4.3 Stage 3 (line 144) explicitly states the identifying assumption is unconfoundedness given observables, "exactly the same assumption underlying the logit and hierarchical specifications," and that CATEs "should be read accordingly as doubly-robust conditional associations rather than causal effects identified off a natural experiment." This is a correct and appropriately blunt statement — no residual overclaim found in §5.4's causal-forest results prose either. |
| 5 | Multiple-testing exposure on the overdraft interaction | **FULLY ADDRESSED, methodologically sound — but see Finding V-1 for a production defect in its delivery** | The Benjamini-Hochberg correction is real, independently reproducible (I re-ran the arithmetic by hand for three of the thirteen rows and it matches `data/processed/table10_multiple_testing_correction.csv` exactly), and honestly reported: the headline result (nothing survives at any conventional FDR) is stated plainly rather than softened. The choice to restrict the correction family to credit-interaction terms (excluding the pure country-level SBFN×RegQuality term, and excluding Table 5/6's Bayesian and forest estimates) is defensible standard practice — it's a within-hypothesis-family correction (all these terms test H2/H3), not an across-unrelated-hypotheses one — though the manuscript could be a half-sentence more explicit that this is the family-definition choice being made, for a methodologically alert reviewer who might otherwise ask "why not correct across everything in the paper." Minor, not blocking. |
| 6 | "No interaction" conflated with "no institutional complementarity"; extensive-margin alternative unaddressed; self-report/stakeholder caveat missing | **FULLY ADDRESSED, and well-executed** | All three new Discussion paragraphs are present, substantively engage the actual concern (not just cosmetic hedging), and are honest about their own limits (e.g., the extensive-margin paragraph explicitly says the paper's design "does not do this" rather than claiming partial evidence it doesn't have). The SBFN/IFC theory-of-change framing is a genuine, well-placed addition that strengthens the paper's stakeholder relevance. |
| 7 | Firm-size heterogeneity under-theorized, introduced too late | **FULLY ADDRESSED** | New §3.4 (H4) gives it real theoretical grounding (fixed-cost logic, tied to Ullah 2025 already in the reference list) and is honest about its post-hoc status ("We did not set out to test this as a fourth ex-ante hypothesis... it emerged from the causal forest's feature-importance decomposition"). This is the correct way to retrofit an exploratory finding into a hypothesis structure — it does not pretend the analysis was pre-registered. See Finding V-2 for one precision nit in how it's cross-referenced. |
| 8 | Endogenous SBFN adoption / no sensitivity analysis; wild-cluster bootstrap on Stage 1; Oster's-delta-style check | **NOT ADDRESSED — correctly disclosed as out of scope, not silently dropped** | `PROGRESS.md` states plainly that these require the underlying WBES microdata, which is not in this repository (confirmed: `raw_data/` does not exist locally; `src/build_firm_dataset.py` reads from a path that isn't present). This is the right way to handle a finding you cannot fix rather than fabricating a result — I verified the microdata really is absent rather than taking the disclosure at face value. |

**No round-1 finding was rubber-stamped.** Item 1 is marked partial specifically because "the paper now explains its limitation better" and "the paper's identification strategy is stronger" are different claims, and only the first is true — this distinction matters for Part C.

---

## Part B — New Findings on the Added Material

### Finding V-1 (CRITICAL — verified, not a judgment call): Table-numbering cascade introduced by the new Table 10, compounding a pre-existing bug

I recompiled `latex/manuscript.tex` (pdflatex + bibtex, 3 passes) and read the resolved table numbers directly from `manuscript.aux`. The actual compiled sequence is:

| Label | Compiled number | What it is |
|---|---|---|
| `tab:vardef` | Table 1 | Variable definitions |
| `tab:composition` | Table 2 | Sample composition |
| `tab:baseline` | **Table 3** | Baseline classical logit |
| `tab:multilevel` | Table 4 | Bayesian hierarchical |
| `tab:causalforest` | Table 5 | Causal forest ATE/CATE/importances |
| `tab:sizecate` | Table 6 | Causal forest CATEs by size |
| `tab:extension` | Table 7 | Small-sample supplementary check |
| `tab:fdr` (**new**) | **Table 8** | Multiple-testing correction |
| `tab:robustness` | **Table 9** (was 8) | Additional robustness checks |
| `tab:global` | **Table 10** (was 9) | Global-sample regressions |

Two distinct problems follow from this:

1. **Pre-existing, not introduced by this round's fixes:** `tab:baseline` compiles to **Table 3**, but the manuscript hardcodes literal "Table 4" twice — once in §4.3's Stage 5 description ("comparability with the primary sample's Table 4," line 148) and once in §5.7 ("the direct global-sample analogue of Table 4's primary-sample baseline," line 456). I checked this against the pre-review-cycle commit (`git show 5039e0a:latex/manuscript.tex`) and confirmed both hardcoded "Table 4" mentions were already present before this review cycle began, at the equivalent lines — this is not something introduced by the recent fixes, and it was missed by the round-1 review too. It appears the manuscript's own intended numbering scheme (visible in the `data/processed/table4_baseline_regressions.csv`-style filenames, which imply composition=1, baseline=4, multilevel=5, causalforest=6, extension=7, robustness=8, global=9) assumes a Table 2 and Table 3 exist between composition and baseline that are simply **not present in the LaTeX body** — `data/processed/table2_summary_stats.csv` exists in the repository but there is no corresponding "Table 2: summary statistics" table anywhere in `manuscript.tex`. Either a table was dropped during typesetting, or `tab:vardef` was intended to occupy that Table 2/3 slot but was placed out of sequence. This is worth the authors' attention independent of anything in this review cycle.

2. **Introduced by this round's fix:** the new Table 10 (`tab:fdr`) was inserted physically *before* `tab:robustness` in the source, which pushed `tab:robustness` from Table 8 → Table 9 and `tab:global` from Table 9 → Table 10. The new table's own row labels, however, hardcode the *old* numbers as plain text rather than `\ref{}` cross-references: rows read "Table~8 (b1) Overdraft," "Table~9 M2 (country FE)," "Table~4 M3," etc. (lines 407, 414–426). Given the actual compiled numbering above, every one of these is now wrong: the overdraft row should read "Table 9," not "Table 8" (which, after the shift, is the FDR table's own number — the table would be citing itself); the country-FE rows should read "Table 10," not "Table 9"; and the M3 rows inherit the pre-existing "should be Table 3, not Table 4" problem from item 1.

Net effect: **Table 10 as it currently stands misidentifies its own source tables**, which is exactly the kind of production error a copyeditor or the guest editors' own production team would flag, and which undermines confidence in a table whose entire point is to be a careful, trustworthy accounting exercise. This is straightforward to fix (replace every hardcoded number with the corresponding `\ref{tab:baseline}`, `\ref{tab:robustness}`, `\ref{tab:global}`) and does not require any new analysis — but it needs to happen before this manuscript goes anywhere near a copyeditor, let alone a submission portal.

*(I did not fix this while producing this review, per the read-only constraint on this pass; recommend applying the `\ref{}` fix as an immediate, low-risk follow-up.)*

### Finding V-2 (MINOR): imprecise cross-reference for H4's empirical support

The Introduction's new fifth contribution point states "we show (Section~\ref{sec:h4}) that the effect heterogeneity that does exist is concentrated at the level of firm size" — but `sec:h4` is §3.4, which *states* H4 as a hypothesis; the actual empirical demonstration is in §5.4 (`sec:causalforest`). Suggest citing both (`Sections~\ref{sec:h4} and~\ref{sec:causalforest}`) or citing `sec:causalforest` alone, since "we show" implies the empirical section.

### Finding V-3 (MINOR, pre-existing, resurfaced): "four stages" vs. five described stages

§4.3's empirical-strategy intro still reads "in four stages of increasing methodological sophistication," immediately followed by Stage 1 through **Stage 5**. This predates the current fix round (confirmed against the pre-review commit) and was not caught by round 1 either. Trivial copy-edit (change "four" to "five"), flagged here only because a genuine verification pass should not let a real, easy-to-fix inconsistency go unmentioned twice in a row.

### Finding V-4 (MINOR): a slight tonal seam in the Discussion's closing paragraph

The new "no interaction ≠ no complementarity" paragraph (§6) is carefully hedged — "we hold it as the best current account rather than as a claim the paper has definitively ruled the other two out." Two paragraphs later, the Discussion's closing paragraph states its conclusion ("our results sit closer to a state-capacity-is-necessary-but-firm-level-frictions-bind-independently story...") without echoing that hedge. Not a contradiction — the closing paragraph is consistent with "preferred reading" — but a reader moving through the section in order could reasonably feel the hedge was quietly dropped rather than carried through. A one-clause callback ("our best current reading remains that...") would tie the two together more visibly. Cosmetic, not substantive.

### Finding V-5 (Observation, not a defect): H4's exploratory framing is genuine, not hedge-dressing

Explicitly checked, since the review brief asked: §3.4's framing ("We did not set out to test this as a fourth ex-ante hypothesis... it emerged from the causal forest's feature-importance decomposition, which we report honestly here as an auxiliary, exploratory hypothesis... rather than one we pre-specified") is an accurate description of the paper's own analytical history as reconstructable from the rest of the manuscript (the size-heterogeneity finding is discussed nowhere in the original hypothesis section, only in the causal-forest results). This is honest retrofitting, not rebranding an unchanged causal claim as tentative. No issue.

### Finding V-6 (Observation): the FDR fix is real work, not theater

The correction is independently reproducible from public information in the manuscript itself (I hand-verified the BH adjustment for the smallest three raw p-values), the script is included and legible, and — most importantly — the paper reports the *unfavorable* conclusion (nothing survives) rather than picking a looser FDR threshold that would let the overdraft finding through. This is exactly the kind of fix that could have been faked with a friendlier-looking number; it wasn't.

---

## Part C — Updated Special Issue Fit Verdict

**Verdict: still marginal fit — narrower and better-disclosed than round 1, but the core CFP risk is structurally unchanged, and cannot be closed further without the underlying microdata.**

What changed since round 1: the paper no longer leaves its identification-strategy gap to be discovered by a guest editor or reviewer — it now states, in its own methodology section, exactly why a staggered DID/event-study (the design class the CFP names first) is not implementable with this data, and the cover letter draft (`latex/cover_letter.md`) makes the same case directly to the guest editors up front. This is a meaningful reduction in *screening* risk: an editor applying the CFP's language literally will now find the paper's own accounting of the gap rather than having to infer it, and transparency of this kind is generally rewarded rather than punished at the desk-screening stage.

What did not change, and could not have changed without new data: the paper's actual identification strategy is still four estimators sharing one identifying assumption (unconfoundedness given observables), not a design from the CFP's named list. Round 1's Devil's Advocate CRITICAL finding was never "the paper hides this" — re-reading it now, the finding was "the paper's design doesn't match the CFP's stated bar," which remains true regardless of how well the paper now discloses it. Better disclosure is the right response to a data constraint that cannot be engineered away, and it is what a responsible author should do — but it changes the paper's *presentation* risk, not its *substantive* risk, against a CFP that says explicitly it screens on identification strategy rather than on candor about identification strategy.

I would not revise the verdict upward from round 1's "marginal fit, real risk of failing initial editorial screening on identification grounds" to anything stronger than: **marginal fit, materially better-argued case for why the paper's approach is the best available answer to the CFP's own question given real data constraints, but still resting on the guest editors accepting that argument rather than on the paper meeting the letter of the CFP's methods list.** Whether that argument succeeds is now genuinely in the guest editors' hands in a way it wasn't before (previously they might have rejected on an unexplained gap; now they have to engage with an explained one) — this is progress, but it is a change in what the editors are being asked to accept, not a resolution of the underlying tension.

---

## Part D — Revised Editorial Decision

**General journal standard (non-special-issue):** Minor revision. Nothing found in this pass changes the underlying empirical work's soundness; Finding V-1 is a typesetting/production defect, not a scientific one, and is trivially fixable.

**This special issue specifically:** Unchanged from round 1's practical recommendation — submit with the current cover letter framing, understanding that the special-issue screen is a genuine coin-flip-adjacent risk the authors have done what they reasonably can to influence, not eliminate. The Devil's Advocate CRITICAL finding from round 1 is **adjudicated as validated-and-mitigated-but-not-resolved**: it does not block submission (the authors cannot be asked to run a design their data cannot support), but it should not be represented internally as "fixed" — `PROGRESS.md`'s "Review response" section currently describes the identification-strategy item correctly as a disclosure/framing fix, which is accurate and should stay framed that way rather than being upgraded to "addressed" in any future status summary.

**Before this manuscript is copyedited or submitted:** Finding V-1 (table numbering) must be corrected — replace every hardcoded "Table N" in `latex/manuscript.tex` with the matching `\ref{tab:...}`, recompile, and re-check the `.aux` file the way this review did, since that is the only reliable way to confirm the fix rather than re-guess at source order. Findings V-2 through V-4 are optional polish.

---

## Summary Table

| Dimension | Round 1 | Round 2 (this pass) |
|---|---|---|
| Identification-strategy transparency | Missing / implicit | Explicit, well-argued, honestly bounded |
| Causal-language hygiene (H1, causal forest) | Overclaimed in places | Consistently corrected, verified in three locations |
| Multiple-testing accounting | Absent | Present, independently reproducible, reports the unfavorable result |
| Firm-size mechanism (H4) framing | Under-theorized, late, ambiguous provenance | Grounded, explicitly exploratory, honest about post-hoc status |
| Discussion nuance (no-interaction vs. no-complementarity; extensive margin; self-report) | Absent | Present and substantively engaged |
| **New: table-numbering correctness** | N/A | **Broken — self-inflicted by this round's own new table, compounding a pre-existing bug** |
| Special issue fit | Marginal, real screening risk | Marginal, same structural risk, materially better-argued case for it |
| Editorial decision (general) | Minor-to-Major | Minor (contingent on Finding V-1) |
