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
