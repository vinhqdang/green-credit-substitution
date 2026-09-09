# Progress log

**Internal note (not for the manuscript/commit history):** this round of processing (review
passes, the new Section 6 macro event-study, and the subsequent edits) was run under a Claude
session tied to the RMIT account/affiliation, not BUV. Flagging here so this can be revisited --
e.g. to check whether anything needs reconciling against RMIT's own AI-use or institutional
policies before submission, given the paper's corresponding author is listed under BUV.

## Status: desk-rejected twice; awaiting a decision on the next target journal

**Rejection 2 -- Borsa Istanbul Review (2026-09).** Submitted as BIR-D-26-02719; desk-rejected
without review by Ali M. Kutan, Editor. The letter is a form letter citing capacity, not
content: the journal reviews 10-15% of submissions and accepts 4-5%, and declines the rest
quickly "due to space considerations" so authors can look elsewhere. **No substantive
criticism was given, so there is nothing here to fix.** The only inference available is that
the paper did not make the top 10-15% on an editor's fast skim.

**Rejection 1 -- Economic Systems (2026-09),** special issue "Governing the Green Transition as
System Change." Desk-rejected on four grounds, two of them genuine technical errors, both since
corrected. See "Desk rejection and corrections" below.

**Next target: Environment and Development Economics (Cambridge University Press), chosen and
built for (2026-09-09).** See "Retargeting to Environment and Development Economics" below for
the completed reframe, what moved to a new Supplementary Material file, and what is still open
before submission.

**Corresponding author:** Quang-Vinh Dang (British University Vietnam), ORCID 0000-0002-3877-8024
**Co-author:** Thi-Hong-Hanh Nguyen (Banking Academy Vietnam), ORCID 0009-0006-7821-7404

## What is done

- Full empirical analysis built on two independent samples:
  - **Primary sample**: 41 economies, 2018-2020 WBES Green Economy Module (28,042 firms).
  - **Global sample**: 162 further economies, 2021-2026, built from the World Bank's
    standardized cross-country database (100,115 firms) -- discovered mid-project via a
    deliberate audit of previously-unused `raw_data` archives.
- Four estimators (classical logit, Bayesian hierarchical, causal forest, country-fixed-effects
  logit) converge on the same result: bank credit access robustly predicts green practice
  adoption; SBFN green-banking-policy status and regulatory quality do not moderate that
  relationship, on either sample.
- Manuscript typeset in LaTeX (`elsarticle` class, double-anonymized): `latex/manuscript.tex`
  / `manuscript.pdf` (59 pages, 5 figures, 12 tables), `latex/titlepage.tex` (author info,
  CRediT), `latex/Highlights.txt`.
- Three independent review passes completed and fixed: numeric accuracy against source data,
  bibliography/citation integrity, Elsevier compliance + LaTeX structural checks.
- Repository pushed to GitHub: `vinhqdang/green-credit-substitution`.

## Desk rejection and corrections (2026-09)

The *Economic Systems* SI editor desk-rejected the paper on four points. Two were real errors and
have been fixed; two were fair criticisms already acknowledged as limitations.

**Point 1 (real error, now fixed): country fixed effects and the interaction term.** Section 4.3
claimed a country fixed effect would absorb Credit x SBFN "completely, making beta_2 and beta_3
unidentifiable by construction." That is false for beta_3. The interaction is a *firm-level*
regressor; a country dummy absorbs country-level regressors only, and credit access varies within
country, so beta_3 stays identified. The manuscript stated the correct rule for Stage 5 fifteen
lines later in the same section, and `src/analysis_global.py`'s docstring had it right all along --
so the paper contradicted itself on first-course material. This undercut the stated rationale for
the whole Stage 1 -> Stage 2 escalation.

Corrected argument now in the manuscript: country FE absorbs the SBFN main effect only; on the
primary sample it would identify beta_3 off the contrast between within-country credit variation in
8 adopter economies and 33 non-adopters, while making the SBFN level shift unreportable. The route
is imprecise, not infeasible. Mirrored in the abstract, introduction, Section 3.3, Section 5.2, and
`src/analysis_baseline.py`'s docstring, which carried the same false claim.

**Point 2 (real error, now fixed): H3's three-way interaction.** The Bayesian hierarchical model was
billed as the primary vehicle for testing H2 "and H3," but it carries two two-way cross-level
interactions and no Credit x SBFN x RegQuality term, so it cannot test H3 as posed. H3 was in fact
already tested -- by Table 4's M3 triple interaction (b = -0.104, se = 0.272, p = 0.702) and by the
global sample's saturated no-FE specification -- just not where the paper claimed. Section 5.3 is now
scoped to H2, Section 5.2 reports the three-way term by name, and Stage 5's description notes that
its FE column omits that term. Same correction in `src/analysis_multilevel.py`'s docstring.

**Points 3 and 4 (fair, not newly actionable):** construct validity of binary SBFN membership as a
proxy for a graded policy process (already Limitation 2), and interpretation outrunning the evidence
on the causal-forest feature importance and the country-level event study (already hedged in
Sections 5.4, 6, and 7).

**Nothing was recomputed.** Both errors were in prose describing the econometrics, not in the
analysis: no estimate, table, or figure changed. Note that the WBES microdata is not present in
this repo (gitignored, and restricted-access at source), so re-running the pipeline requires
re-downloading it.

## Retargeting to Borsa Istanbul Review (2026-09)

- Journal name updated in `latex/manuscript.tex` and `latex/titlepage.tex`.
- All special-issue framing removed (7 passages in the tex, 7 in `manuscript/*.md`), including the
  "Policy Design x System Conditions -> System Outcomes" framing that belonged to the ES call.
- Journal-fit paragraph rewritten. It previously cited six *Economic Systems* papers; it now cites
  five *Borsa Istanbul Review* papers, each verified independently via Crossref before use
  (Jia et al. 2026; Chi & Yang 2023; Shi et al. 2024; Ullah et al. 2024; Jin 2026). The Section 3.3
  institutional-complementarity paragraph was rewritten on the same basis, replacing Barra &
  Falcone (2026). See `data/bibliography.md` section 6 for the verification record and section 7
  for the withdrawn ES entries.
- The six now-uncited ES references were removed from `references.bib` (BIR's checklist requires
  reference list and text to match exactly). Bib is now 42 entries, all cited; verified
  programmatically that used keys and defined bibitems match exactly.
- **Reference style converted to APA 7th edition.** `apacite` conflicts with `elsarticle`, and no
  Elsevier APA-like bst (`model5-names`) is installed, so the reference list is generated from
  `references.bib` by `bib2apa.py` and embedded inline as a `thebibliography` block with
  natbib-compatible `\bibitem[Author(Year)]` labels. Handles sentence-casing (proper nouns
  protected by braces in the .bib), ampersands, article numbers vs page ranges, DOIs as
  https://doi.org/, and APA surname-then-initial sort order. Same-surname authors (Ullah, B. 2025
  vs Ullah, W. et al. 2024) carry initials in their in-text labels per APA.
  **If `references.bib` changes, the inline block must be regenerated** -- it is no longer built by
  bibtex.
- Spelling standardized to American English throughout body text (behaviour -> behavior, artefact ->
  artifact, modelling -> modeling, favourably -> favorably, centre -> center). Cited works' published
  titles left untouched.
- Cover letter rewritten for BIR (`latex/cover_letter.tex` / `.md`). It discloses the desk rejection
  and both corrected errors explicitly rather than leaving them to be discovered.
- All three documents compile clean: manuscript 73 pages, no undefined citations or references.

## Review response (2026-09)

A full special-issue-fit peer review pass (`output/review_cfp_fit_2026-09.md`) was run against the
*Economic Systems* "Governing the Green Transition as System Change" CFP. The following fixes were
made to the manuscript (`latex/manuscript.tex`, source of truth; `manuscript/*.md` synced to match)
in response:

- Added a first-class methodological paragraph (Section 4.1) explaining why a staggered
  DID/event-study design around SBFN's 2012-2024 adoption timing — the identification strategy the
  CFP names first — is not implementable with the published WBES microdata (the Green Economy
  module is fielded once per country, not as a repeated panel item), and fixed a stale
  cross-reference in the Conclusion's Limitation 1 that pointed to the wrong section.
- Softened causal-sounding language around the H1 credit-access finding (abstract, Discussion,
  Highlights) to make clear it is an association net of observed controls, not a causally
  identified effect; added an explicit caveat to the causal-forest description (Section 4.3) that
  its "causal" label rests on the same unconfoundedness assumption as the logit/hierarchical
  models, just with a more flexible functional form.
- Added a new auxiliary, exploratory hypothesis H4 (Section 3.4) that gives the firm-size
  effect-heterogeneity finding (previously a late, under-theorized Discussion point) proper
  theoretical grounding and an explicit "exploratory, not pre-registered" framing; referenced it
  from Section 5.4 and the Introduction's (now five, was four) contribution points.
- Computed a Benjamini-Hochberg false-discovery-rate correction (`src/compute_fdr_interactions.py`,
  output in `data/processed/table10_multiple_testing_correction.csv`) across all 13 credit x
  institutional-moderator interaction coefficients reported under a frequentist estimator (Tables
  4, 8, 9). The one nominally significant coefficient (overdraft x SBFN, raw p = 0.031) does not
  survive at any conventional FDR (adjusted p = 0.403); added as new Table 10 and cited wherever the
  overdraft finding is discussed.
- Added Discussion paragraphs distinguishing "no interaction detected" from "no institutional
  complementarity exists," engaging directly with an unaddressed alternative mechanism (SBFN policy
  could operate on the extensive margin of who gets credit, not the intensive margin this paper
  tests), flagging the firm-reported-outcome/bank-compliance-reporting gap, and connecting the null
  result to the SBFN/IFC's own self-evaluation practice. Expanded the Conclusion's limitations list
  from five items to six to formalize the extensive-margin and self-report points.
- Not attempted, and flagged as out of scope for this repository rather than silently skipped: an
  actual staggered-DID re-estimation, a wild-cluster-bootstrap check on Stage 1's small-cluster
  inference, and a formal SBFN-adoption-endogeneity sensitivity analysis (e.g. Oster's delta) all
  require the underlying WBES firm-level microdata, which is registration-gated and not present in
  this repository (see Data availability). These remain open items for whoever holds the microdata
  locally to run before submission.

A draft cover letter addressing the CFP's identification-strategy language directly (recommended by
the review) is at `latex/cover_letter.md` — needs the bracketed fields filled in and a final human
read before submission.

## Re-review (2026-09, round 2)

A second review pass (`output/review_cfp_fit_2026-09_v2.md`) verified the round-1 fixes against the
actual manuscript rather than rubber-stamping them: all substantive fixes were genuinely applied
(identification-strategy transparency, causal-language hygiene, the FDR correction, H4's honest
exploratory framing, the three new Discussion paragraphs). One finding was NOT addressed by design —
the endogeneity/wild-cluster-bootstrap/Oster's-delta items still require microdata not in this
repository — and that remains correctly disclosed rather than silently dropped.

The pass also caught a real, verified defect introduced by round 1's own new table: inserting the
multiple-testing-correction table shifted LaTeX's auto-numbering of every table after it (robustness
8->9, global-sample regressions 9->10), and the new table's rows had hardcoded the old numbers as
plain text instead of cross-references — so it was citing itself and its neighbors incorrectly. This
also exposed a **pre-existing** numbering bug, unrelated to any of this review cycle's changes: two
hardcoded "Table 4" mentions (Stage 5 description; Section 5.7) actually resolve to Table 3, confirmed
present in the same form in the original pre-review commit (`5039e0a`). Root cause: the manuscript's
own apparent intended numbering (matching the `data/processed/table4_baseline_regressions.csv`-style
filenames — composition=1, baseline=4, multilevel=5, ...) implies a Table 2 and Table 3 between
composition and baseline that were never actually inserted into `latex/manuscript.tex` (a
`table2_summary_stats.csv` exists in the repo with no corresponding table in the manuscript body).

Fixed: every hardcoded "Table N" mention in `latex/manuscript.tex` now uses `\ref{}`, so the compiled
numbering is internally self-consistent (verified against `manuscript.aux` after recompiling — no
mismatches remain). Two small precision/tone edits from the same pass were also applied (an imprecise
cross-reference for H4's empirical section; a hedge-consistency callback in the Discussion's closing
paragraph), and mirrored into `manuscript/*.md`.

**Not fixed, and flagged rather than silently resolved:** the deeper structural question of the
missing Table 2/3 slot (should a summary-statistics table be inserted? was `tab:vardef` meant to sit
elsewhere?) needs an author decision, not a unilateral renumbering — the current fix makes every
in-document reference correct relative to the tables that actually exist, but does not attempt to
restore the apparent originally-intended Table 1-9 sequence, which would require either adding new
table content or reordering existing tables in a way I'm not positioned to decide alone.

## New analysis: country-level staggered event-study (2026-09)

In response to the CRITICAL identification-strategy finding (the paper's four firm-level estimators
all share one identifying assumption; none matches the CFP's named staggered-DID/event-study class),
built and added a genuinely new, independent supplementary analysis rather than only better-disclosing
the existing gap:

- **New Section 6** ("Supplementary evidence: a country-level staggered event-study on macro
  environmental outcomes"), with two subsections (data/design; results), new Table 11, and new
  Figure 6. Discussion and Conclusion renumbered to Sections 7-8 accordingly (all cross-references
  are `\ref{}`-based, verified self-consistent after recompiling — checked the same way the earlier
  table-numbering bug was caught, by reading resolved numbers out of `manuscript.aux`).
- **Data**: a country-year panel (217 economies, 2000-2024) built from scratch — SBFN join years from
  `data/sbfn_roster.csv` name-matched to a full World Bank country list (zero unmatched, zero
  disagreements against the existing `data/global_sbfn.csv` coding), joined to World Development
  Indicators panels (renewable energy %, CO2 per capita, GDP per capita as a covariate) fetched live
  via the public WDI API. New scripts: `src/build_macro_country_universe.py`,
  `src/fetch_macro_wdi_panel.py`, `src/run_macro_event_study.py` (needs a separate environment --
  `src/requirements_macro_did.txt` -- pinning newer pandas/numpy than the rest of the repo assumes).
  New data: `data/macro_country_treatment_panel.csv`, `data/macro_wdi_panel_raw.csv`,
  `data/macro_wdi_gdppc.csv`, `data/processed/macro_did_*` (raw estimator output),
  `data/processed/table11_macro_did_summary.csv`.
- **Method**: Callaway & Sant'Anna (2021) staggered-adoption DID (`differences` Python package),
  never-treated comparison group, both unconditional and doubly-robust (log-GDP-per-capita-controlled)
  specifications, plus a naive TWFE regression reported explicitly as a biased comparison (not a
  preferred estimate) to illustrate the known staggered-timing bias.
- **Result, reported honestly rather than spun either direction**: no effect on renewable-energy
  share (clean null, flat pre- and post-trends). CO2 per capita shows a positive, "wrong-signed"
  association that shrinks ~45% once GDP per capita is controlled for, and whose event-study profile
  (smoothly diverging post-period, not a discrete jump; two marginal pre-trend leads) reads as more
  consistent with pre-existing growth-trajectory differences between adopting and non-adopting
  economies than a genuine policy-caused effect. Neither result supports treating SBFN adoption as a
  country-level lever that improves environmental outcomes -- converging with, and substantially
  strengthening, the paper's firm-level central finding from an entirely independent design that
  meets the CFP's own identification-strategy bar.
- Abstract, Highlights, Introduction's contribution list (now six, was five), Discussion, Conclusion
  (five consistent results, was four; seven limitations, was six), the AI-disclosure paragraph, the
  Data Availability statement, `latex/references.bib` (Callaway & Sant'Anna 2021; Goodman-Bacon 2021),
  and `latex/cover_letter.md` all updated to reflect this; `manuscript/*.md` kept in sync (new file
  `manuscript/05b_macro_supplementary_evidence.md` mirrors the new Section 6).
- Recompiled and verified clean (pdflatex + bibtex, no undefined references, table formatting fixed
  to fit page margins) — 74 pages, up from 67.
- Special-issue-fit reassessment: this materially changes the picture from the prior two review
  rounds. The paper no longer merely explains why it lacks a staggered design at the firm level --
  it now contains one, on the identical policy-timing variation, using an independent data source,
  and that design also returns no clean evidence of a beneficial institutional effect. Whether the
  guest editors credit this as meeting their stated bar is still their call, but the paper's actual
  identification-strategy portfolio is now substantively stronger, not just better-argued.

## Third review pass (2026-09, round 3) and fixes applied

A third review (`output/review_cfp_fit_2026-09_v3.md`) re-verified the round-2 table-numbering fix
holds under the new Section 6 (recompiled fresh and re-checked `manuscript.aux` directly rather than
trusting the change log) and independently re-swept the whole manuscript for code/file-language leakage
(clean). It then critiqued Section 6 on its own merits and raised two findings, both since fixed:

- **Terminology imprecision (fixed).** The Discussion and Conclusion each described Section 6's result
  as "the null on institutional moderation," but Section 6 tests a main effect (does adoption shift a
  country outcome), not a moderation effect (does adoption change a firm-level slope, what H2/H3
  actually test) -- a real conflation risk in exactly the two places a guest editor is likely to read
  closely. Fixed in both spots: replaced with "the absence of a beneficial institutional effect" plus an
  explicit sentence distinguishing the two claims.
- **Missing control-group robustness check (fixed, not just disclosed).** Section 6 originally reported
  only the `never_treated` comparison group; re-ran the doubly-robust specification for both outcomes
  with `not_yet_treated` as well (`src/run_macro_event_study.py` updated to run both and rebuild Table
  11 with all 8 rows). Both outcomes are essentially unchanged under the alternative control group
  (CO2: 0.313 vs. 0.349, both significant; renewables: 0.653 vs. 0.674, neither significant) -- genuine
  confirmation the result doesn't hinge on that choice, not an assumption.
- Also lightly varied one instance of a "we are not spinning this into X or Y" rhetorical pattern that
  had started to repeat across the paper (round 3's B3, minor polish).
- Round 3's upgraded verdict: **good fit, contingent on the terminology fix** -- now applied. Round 1's
  CRITICAL identification-strategy finding is resolved, not just better-disclosed.

Recompiled and re-verified (pdflatex + bibtex, no undefined references, table renders within margins,
75 pages). `manuscript/*.md` kept in sync.

## Author-requested edits (2026-09): PyMC citation, shorter AI declaration, tighter Discussion/Conclusion

- Added a citation for PyMC (Salvatier, Wiecki, and Fonnesbeck, 2016, PeerJ Computer Science) at its
  first mention in Section 4.3, since economics reviewers may not otherwise know what it is.
- Shortened the AI-disclosure paragraph to a short, generic statement ("AI-assisted tools to help
  polish the writing... the author(s) reviewed and edited the content as needed and take full
  responsibility") at the author's explicit request. **Flagged to the author at the time**: the
  previous, longer disclosure was accurate to what actually happened this session (AI assisted with
  data construction, running the firm-level and Section 6 analyses, and drafting), and Elsevier's own
  policy on generative-AI disclosure generally expects the disclosed scope to match the actual scope
  of use, not just language polishing. This is the author's disclosure to make, but worth a final
  check against the journal's specific AI-use policy before submission, since the current wording
  understates what was actually done in this repository's own history.
- Tightened Discussion (Section 7) and Conclusion (Section 8) substantially: merged overlapping
  paragraphs (the two-sample convergence argument and the new Section 6 convergence point; the
  extensive-margin alternative and the self-report caveat), cut restated hedging, and shortened the
  seven-item limitations list and five-item results list to their essential claims without dropping
  any of the hedges or caveats prior review rounds required. Net effect: manuscript went from 75 to
  71 pages with no loss of substance verified against the pre-edit version.
- Recompiled and verified (pdflatex + bibtex, no undefined references, no hardcoded Table/Section/
  Figure numbers introduced). `manuscript/*.md` kept in sync.

## Submission package for Borsa Istanbul Review (2026-09-08)

BIR uses **double anonymized review** and requires three separate files. All three are built and
committed under `latex/`:

1. **`cover_letter.pdf`** (`cover_letter.tex`, mirrored in `cover_letter.md`) -- addressed to
   Dr. Ali Kutan, Editor. Positions the paper against four BIR-published country-level papers
   whose firm-level implication this paper tests directly (Jia et al. 2026; Chi & Yang 2023;
   Shi et al. 2024; Ullah et al. 2024), and discloses the Economic Systems desk rejection and
   the two corrections up front rather than letting a reviewer find it. Signed for both authors.
2. **`titlepage.pdf`** (`titlepage.tex`) -- both authors, affiliations, corresponding-author
   block with full contact details, both ORCID iDs (check digits validated under ISO 7064
   MOD 11-2), acknowledgements, declaration of interest, funding, CRediT.
3. **`manuscript.pdf`** (`manuscript.tex`) -- 73 pp., anonymized. Verified clean: no author
   names, affiliations, or acknowledgements; the replication-repo link is withheld from the
   Data Availability statement; PDF document properties resolve the author field to
   "Anonymous for review" rather than leaking a name through metadata.

Editorial Manager form values used at submission:

- **Region of Origin:** Asia Pacific (both authors are Vietnam-based).
- **Abstract field (150-word limit):** the manuscript's own abstract is 576 words and does not
  fit, so a 147-word version was written for the form. It drops the overdraft/multiple-testing
  caveat and the exploratory framing of the firm-size result; both remain in the manuscript.
  If 150 words turns out to be the *journal's* abstract limit rather than just the form
  field's, the manuscript abstract needs the same cut.

## Pending

- Repository should be set to **private** before formal submission (to preserve
  double-anonymized review — the Data Availability statement already reflects this), then
  back to public upon acceptance. Not yet done — requires manual action on GitHub
  (Settings -> Danger Zone -> Change visibility), not doable via CLI in this environment.
- CRediT authorship statement on the title page was filled in with a plausible split by
  Claude at the corresponding author's request — worth a final human check before submission.
- Suggested reviewer names/institutional emails (requested by the guide) still need to be
  supplied by the authors.
- **Co-author email `hanhnth1@hvnh.edu.vn` is unverified.** It entered the repo in the first
  commit and its provenance cannot be traced from git history. Confirm before submission.
- **Affiliation string** reads "Banking Academy Vietnam"; the institution's official English
  name is "Banking Academy *of* Vietnam". Left as-is pending the co-author's preference.
- The Economic Systems fee-waiver thread (Jan-Egbert Sturm) is **superseded** by the
  retargeting and needs no follow-up.

## Journal search (2026-09-09): verified fees and shortlist

**Author constraint: no submission fee.** Fees below verified against publisher pages, not recalled.

**Passes the no-fee filter** (all hybrid or waived, so publishing costs $0):

| Journal | Submission fee | Cost to publish | Median length |
|---|---|---|---|
| Environment and Development Economics (CUP) | none | $0 subscription route (gold OA GBP 2,610 optional) | 21 typeset pp. |
| Business Strategy and the Environment (Wiley) | none | $0 subscription route (OA $4,700 optional) | -- |
| PLOS Climate | none | **$0 guaranteed** -- APC auto-waived for Research4Life Group A/B corresponding authors; Vietnam is Group B | -- |
| World Development (Elsevier) | not on Elsevier's fee list | $0 subscription route | -- |
| Journal of Environmental Management; Energy Policy | not on Elsevier's fee list | $0 subscription route | 7,000-10,000 words |
| Journal of Development Effectiveness (T&F); Emerging Markets Finance and Trade (T&F) | none | $0 subscription route | -- |

**Excluded on the no-fee rule.** Elsevier's submission-fee page names Emerging Markets Review
($150), International Review of Financial Analysis ($175), Finance Research Letters ($200) and
Energy Economics as fee-charging. Also excluded: JIFMIM ($125), Economic Modelling ($125),
Economic Analysis and Policy ($125, levied even on desk rejection), Pacific-Basin Finance Journal
($220), Research in International Business and Finance ($150 plus mandatory gold OA from
2026-09-15). This removes the finance route almost entirely, which is acceptable -- it was the
weakest scope fit.

**Excluded on other grounds.** Journal of Development Economics and World Bank Economic Review
(identification bar; WBER also caps main text at 7,000 words). Environmental Science & Policy
(hard 7,000-word cap, over-length papers auto-returned). Journal of Cleaner Production
(Clarivate expression of concern over self-citation). Finance Research Letters also carries an
editorial-integrity concern (12 Elsevier retractions, Dec 2025).

**Recommended target: Environment and Development Economics.** Free; Cambridge, so it counts
institutionally; median 21 typeset pages is a reachable target; and it has verified precedent
publishing multi-country Enterprise Survey firm-level work, so a cross-sectional design is house
style rather than an exception -- which directly addresses this paper's known weakness.
**Alternative:** Business Strategy and the Environment, which published a 2026 paper using the
same WBES Green Economy module and the same seven-item outcomes, at the cost of a management
rather than economics framing. **Safety net:** PLOS Climate, the only venue found whose stated
criteria judge validity rather than novelty or impact, and which welcomes nulls.

**Caveats recorded by the searches.** No journal assessed has a published null-results policy
except PLOS and the Journal of Development Effectiveness. Vietnam is NOT on the Taylor & Francis
APC-discount country list (they require lower-middle income *and* GDP under $200bn), so do not
plan on a T&F discount. Several Elsevier/Wiley APC figures came from aggregators because
ScienceDirect and Wiley returned 403 -- immaterial while taking the subscription route.

## Restructuring plan (agreed 2026-09-09, then corrected before execution)

Two desk rejections without review is weak evidence on any single dimension, and the BIR letter
carries no content at all, so the operative question is what an editor sees in a ten-minute skim.
The authors initially asked for a full reframe leading with the firm-size result (H4). **That
specific plan was not executed, and should not be**: the causal forest's overall ATE is 0.073
with a 95% CI of [-0.040, 0.186] -- it spans zero -- and the size-stratified effects (0.080 /
0.075 / 0.057) all have wide, overlapping, zero-spanning intervals and run opposite to the
fixed-cost story the paper's own H4 predicts. Leading a resubmission with a variance share
(75.6%) computed on top of an insignificant, non-monotonic, non-pre-registered result would not
survive review and would read, after two rejections, as straining for a positive finding. See
the point below for what was built instead.

## Retargeting to Environment and Development Economics (2026-09-09)

**Target chosen and built for:** Environment and Development Economics (Cambridge University
Press). Free via the subscription route (no submission fee, per the authors' hard constraint);
verified precedent publishing multi-country Enterprise-Survey/BEEPS firm-level work (Fayek and
Zaki, "Does 'going green' promote global value chain integration?", *EDE*, Sept 2026,
41 countries; an unnamed 2023 *EDE* paper on environmental management and productivity growth,
also 41 countries, 2017-2019 BEEPS) -- both confirmed by direct search, not taken on an earlier
agent's word alone, before being cited in the cover letter. Co-editors: Allen Blackman, Carlos
Chavez, Susana Ferreira, Jintao Xu (verified against the journal's own editorial-board page);
the cover letter addresses "The Co-Editors" rather than naming one, since responsibility is
shared. Abstract cap confirmed at 150 words; manuscript length "not exceed 36 pages including
title page, text, footnotes, references, tables and figures" (Cambridge's own instructions
page); "supplementary materials may be submitted separately" -- the basis for the Supplementary
Material split below. Author-date citation confirmed, matching the paper's existing style.
**Not confirmed:** whether review is single- or double-anonymized. The instructions describe the
manuscript's own first page as carrying author names/affiliations/emails, which reads as
single-anonymous, and the rebuild below proceeds on that basis -- but this should be verified
before submission (edejournal@gmail.com, or the ScholarOne portal itself) since it is inferred,
not stated outright.

**What changed, precisely:**

1. **Reframe: precision of the null, not the firm-size result.** The abstract and Introduction
   now lead with the paper's actual strength -- five estimators, ~118,000 firms, and *tight*
   confidence intervals, not merely wide ones (credit x SBFN differs by 0.004 between adopters
   and non-adopters in the causal forest; the hierarchical model's credit x regulatory-quality
   posterior is 0.004, 89% ETI [-0.13, 0.14]). This lets the paper claim it can distinguish a
   genuine absence of institutional moderation from an underpowered failure to detect one -- a
   distinction most single-country studies in this literature cannot make. The firm-size finding
   (H4) stays exactly where it was, in Section 5.4, labelled exploratory, not promoted.
2. **Abstract:** rewritten to exactly 150 words (was 576), built around the precision framing.
   Also placed on the new `titlepage.tex`, which now carries an abstract, keywords and JEL codes
   (EDE requires all three on the title page) -- it did not before.
3. **Introduction:** cut from 1,509 to 670 words (56%), same reframe, every citation preserved.
   One citation (`jin2026`, on credit self-rationing) moved from the intro to the Sixth
   Limitation in the Conclusion, where it fits thematically, rather than dropped -- avoiding an
   orphaned, uncited bibliography entry.
4. **Supplementary Material split (new file, `latex/supplementary_material.tex`, compiles to
   6 pp.):** moved out, verbatim, with cross-references to main-text tables rewritten as prose
   (`"the main text's baseline logit table"`) rather than `\ref`, since a table label in one
   `.tex` file cannot resolve in another:
   - The small-sample waste-minimization check (was Table 7) -> Supplementary Table S1.
   - The additional-robustness battery (was Table 9) -> Supplementary Table S2.
   - The Benjamini-Hochberg FDR correction (was Table 8) -> Supplementary Table S3.
   - Appendix A (full 47-economy SBFN/WGI coding), Appendix B (Bayesian convergence
     diagnostics), Appendix C (global-sample SBFN regional summary) -> moved in full.
   The main text keeps short (3-6 sentence) summaries of each result in place, with the
   original section labels (`sec:extension`, `sec:robustness`) intact so nothing that pointed to
   them elsewhere breaks, and points to the specific Supplementary table by name.
5. **Data availability:** dropped the double-anonymized/"link withheld" framing (built for BIR)
   and cited the real repository URL directly, since the current review-type assumption is
   single-anonymous. **Revert this if EDE turns out to require double-anonymized review.**
6. **Title page (`titlepage.tex`) and manuscript author block:** both now carry real author
   names/affiliations/emails/ORCIDs (manuscript previously said "Anonymous for review" for BIR's
   double-anonymized workflow); `\journal{Borsa Istanbul Review}` removed from both files rather
   than repointed, since printing a journal-name banner on the manuscript itself is an
   Elsevier-template convention this Cambridge journal doesn't use.
7. **Cover letter:** re-addressed to EDE's co-editors; fit paragraph rebuilt around the two
   verified EDE precedent papers above (dropped the four BIR-published-paper citations used for
   the previous target, which are unrelated to EDE's own track record); added the precision-of-null
   sentence; kept the disclosure paragraph about the two corrected identification errors
   verbatim, since it remains accurate and the right thing to volunteer regardless of venue;
   dropped the double-anonymized clause in the closing paragraph to match point 5.

**Length: not yet confirmed against the 36-page cap, and this is a real open item, not a
formality.** Prose word count (excluding tables, figures, bibliography) is now 9,104 words, down
from 10,618 -- and three whole tables plus three appendices moved out entirely. But the compiled
`manuscript.pdf` is 61 pages (down from 73) because it still uses `elsarticle`'s `review` class
option, which forces double line spacing and wide margins for a review/track-changes format --
not remotely comparable, page-for-page, to Cambridge's own compact typeset layout. **9,104 words
of prose plus 6 tables and 6 figures is the number to reason from, not 61 pages.** Whether that
clears 36 CUP-typeset pages was not verified by producing an actual CUP-style layout, and is the
single largest remaining risk before submission.

**Known gap: `manuscript/*.md` is now stale.** This session edited only `latex/manuscript.tex`
(and `latex/supplementary_material.tex`, new). The parallel `manuscript/*.md` files -- which a
past session's own commit history says should be kept in sync with the `.tex` -- were not
updated to match the trimmed abstract, Introduction, or the Supplementary Material split. Sync
these before relying on the `.md` files for anything, or treat `latex/manuscript.tex` as the
sole source of truth going forward.

All four submission files compile clean (two-pass `pdflatex`, no errors, no undefined
references): `manuscript.tex` (61 pp., real author names in PDF metadata), `supplementary_material.tex`
(6 pp., new), `titlepage.tex` (2 pp., now with abstract/keywords/JEL added), `cover_letter.tex`
(2 pp.).

## Next steps

1. **Confirm EDE's review-anonymization type** (single vs. double) before submitting -- the
   current build assumes single-anonymous based on the instructions page's wording, not a
   direct statement. If double-anonymized, revert the Data Availability section (point 5 above)
   and rebuild a blinded manuscript variant, reusing the BIR-era anonymization pattern.
2. **Get an honest read on the 36-page cap.** The 61-page PDF is not a meaningful proxy; either
   retypeset a portion in a compact single-spaced layout to sanity-check, or treat the
   9,104-word / 6-table / 6-figure count as the working budget and trim further if a co-editor's
   desk screen flags length.
3. Sync `manuscript/*.md` to `latex/manuscript.tex`, or retire the `.md` mirror if it is no
   longer maintained.
4. Confirm the two still-open author-detail items from the BIR submission (unverified co-author
   email `hanhnth1@hvnh.edu.vn`; "Banking Academy Vietnam" vs. the institution's official
   "Banking Academy *of* Vietnam") -- both carry over unchanged to this submission.
5. Set the GitHub repo to private before submission; flip back to public after acceptance and
   update the Data Availability statement with the real link at that point.
