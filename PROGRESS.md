# Progress log

## Status: manuscript complete, submission pending fee-waiver decision

**Target journal:** Economic Systems (Elsevier), special issue "Governing the Green
Transition as System Change: State Capacity, Policy Credibility, and Institutional
Complementarities in Emerging and Transition Economies."

**Corresponding author:** Quang-Vinh Dang (British University Vietnam)
**Co-author:** Thi-Hong-Hanh Nguyen (Banking Academy Vietnam)

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

## Pending

- **Waiting on reply from the managing editor (Jan-Egbert Sturm, sturm@kof.ethz.ch) regarding
  a waiver of the €80 submission fee** (available per the journal's guide for authors when
  all authors are based in a low-income or lower-middle-income country).
- Repository should be set to **private** before formal submission (to preserve
  double-anonymized review — the Data Availability statement already reflects this), then
  back to public upon acceptance. Not yet done — requires manual action on GitHub
  (Settings -> Danger Zone -> Change visibility), not doable via CLI in this environment.
- CRediT authorship statement on the title page was filled in with a plausible split by
  Claude at the corresponding author's request — worth a final human check before submission.
- Suggested reviewer names/institutional emails (requested by the guide) still need to be
  supplied by the authors.

## Next steps once the fee-waiver reply arrives

1. If waived: proceed to submission via Elsevier's Editorial Manager for Economic Systems.
2. If not waived: confirm payment method, then submit.
3. Set the GitHub repo to private beforehand; flip back to public after acceptance and update
   the Data Availability statement with the real link at that point.
