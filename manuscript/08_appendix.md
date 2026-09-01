## Appendix A. SBFN policy status and regulatory quality, full sample

Table A1 reports, for all 47 economy-years in the paper's primary and small-sample supplementary
check, the SBFN membership status coded for the analysis, the join year where applicable, the SBFN
Multi-Tiered Progress Framework stage in force nearest the survey year, and the exact year of the
Worldwide Governance Indicators observation used. Sourcing detail for every individual determination
(the specific SBFN Global Progress Report, country addendum, or accession announcement consulted) is
available in the replication files given the volume of citation detail involved; we summarize the
stage classification and provenance briefly here for economies coded as SBFN adopters. Mongolia and
Bangladesh, both founding 2012 members, had reached an "Advancing" implementation stage by their
respective 2019 and 2022 survey years; Morocco (member since 2014) had likewise reached "Advancing"
by 2019; Türkiye (2015) and Georgia (2017) sat at a "Developing" implementation stage by 2019; Jordan
(2016) and the Kyrgyz Republic (2018) remained at an initial "Commitment" stage by 2019; Egypt's
stage classification (2016 join year, 2020 survey) is reported as "Formulating," the nearest
available classification predating the survey by several months; Indonesia (2012) had progressed to
a "Consolidating" stage by its 2023 survey; Peru (2013), Philippines (2013), and India (2016) sat at
"Advancing" and "Developing" stages respectively by their 2022-2023 surveys; and Tunisia's exact
policy-stage classification at its 2020 survey year could not be pinned to a report dated close
enough to that year to be reported with confidence, and is marked as such rather than estimated. The
analogous 162-economy table for the global sample (Section 4.1) is summarized by region in Appendix C
and provided in full in the online supplementary material and the replication package.

## Appendix B. Bayesian model convergence diagnostics

Convergence diagnostics for every focal parameter of the hierarchical model reported in Table 5 are
included directly in that table (r_hat, ess_bulk, ess_tail columns): all r_hat values are at or below
1.01, and ess_bulk ranges from 797 (sbfn_member) to 2,270 (fin_has_credit_line:wgi_rq_z), comfortably
above the conventional minimum threshold of 400 effective samples per parameter for stable posterior
summaries at four chains. No divergent transitions were flagged during sampling (NUTS via the nutpie
sampler, target acceptance rate as configured by that sampler's defaults, four chains of 1,000
post-warmup draws each after 1,000 tuning iterations).

## Appendix C. Global-sample SBFN status, regional summary

Of the 162 global-sample economy-years, 61 are coded as SBFN members as of their survey year and 101
as non-members. Table C1 reports the regional distribution of the 61 members, drawn from the SBFN
data portal's regional classification; five of the 61 (Peru, Philippines, Timor-Leste, Bangladesh,
and Indonesia) carry the deeper per-country sourcing already reported in Appendix A, having been
determined during the primary sample's original research pass rather than from the portal roster
alone.

**Table C1. Global-sample SBFN members, by SBFN region.**

| Region | Member economy-years |
| --- | --- |
| Latin America and Caribbean | 17 |
| Africa | 12 |
| Europe and Central Asia | 11 |
| East Asia and Pacific | 11 |
| South Asia | 6 |
| Middle East and North Africa | 4 |
| **Total** | **61** |
