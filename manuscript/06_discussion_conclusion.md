## 6. Discussion

Put in plain economic terms, the paper's central finding is this: a firm holding a bank credit line
is roughly 13 percentage points more likely to have adopted a green production practice than an
otherwise identical firm without one — comparable in magnitude to the gap between a small firm and a
large one — and that gap is essentially the same size whether the firm sits in an SBFN
sustainable-finance policy adopter or a non-adopter, and essentially the same size whether the
country's regulatory quality sits in the bottom, middle, or top third of the sample. Firms in
SBFN-adopting economies are, on average, some 15-20 percentage points *less* likely to have adopted a
green practice at all — a level gap, not a slope gap, and one that shows up whether we look at a
naive pooled logit, a hierarchical model built specifically to detect a moderation effect the pooled
model might obscure, or a causal forest that imposes no interaction functional form whatsoever.
Three methodologically distinct estimators, none of them nested in or dependent on the others' 
assumptions, converge on the same qualitative picture.

This is worth dwelling on precisely because it complicates rather than confirms the implicit
premise of much of the existing green-credit-policy literature, which is disproportionately built on
evidence from China's unusually mature, unusually well-resourced green credit guidelines (Li, Feng,
Li, and Zhou, 2023; Huang, Gao, and Jia, 2023; Dai et al., 2025). Our sample includes economies at
every stage of the SBFN's own progression framework — from Jordan and the Kyrgyz Republic's initial
"Commitment" stage to Mongolia's "Advancing" implementation a full seven years after founding
membership — and across that entire range, we find no evidence that formal policy adoption changes
how a firm's credit access translates into green investment behaviour. Section 5.4's most novel
result gives one plausible redirection of the question, though not a tidy answer to it: the
heterogeneity that *does* exist in the credit-green relationship is overwhelmingly a firm-size
phenomenon (75.6% of explained variance) rather than a country-institutional one (regulatory quality
19.9%, SBFN status a mere 2.6%) — yet, as Section 5.4 reports honestly, collapsing this into the
Surveys' own coarse Small/Medium/Large strata does not recover a clean gradient in either direction
(point estimates of 0.080, 0.075, and 0.057 respectively, with heavily overlapping confidence
intervals), so we cannot yet say whether it is small or large firms for whom the credit-green channel
runs stronger, only that firm scale — in some more granular or non-monotonic form than a three-category
split reveals — is where the forest locates most of the effect heterogeneity a country-level policy
variable does not. What this does support is a reorientation of where policy attention belongs: if the
operative constraint sits at the level of which individual firms can absorb a green investment's fixed
costs once financed, rather than at the level of whether a supervisory guideline nudges banks to lend
more broadly, then a country-level supervisory mandate operating on the extensive margin of bank
lending decisions may be aimed at the wrong margin regardless of its own institutional credibility —
a question future work with a finer-grained firm-size or capacity measure is better placed to resolve
than the coarse categories available here.

The one interaction that does clear a conventional significance threshold — a *negative*
credit x SBFN effect when finance access is measured through overdraft facilities rather than
term credit lines (Section 5.6) — is, we think, more consistent with this redirection than with a
simple failure of green banking policy. Overdrafts finance working capital, not the kind of
multi-year capital expenditure our outcome variable measures; if SBFN-guided lending is
disproportionately channelled through the term-loan instruments better suited to financing a solar
installation or an energy-efficiency retrofit, exactly the pattern we find — a null-to-positive
effect on credit lines, a negative one on overdrafts — is what a supervisor successfully steering
credit toward long-horizon green investment, rather than short-horizon working capital, would
produce. We flag this as suggestive rather than established, since it is a single significant
coefficient among the many interaction tests reported across Tables 4-8, and our data cannot
directly verify the underlying loan-tenor mechanism.

Read against this special issue's organizing themes of state capacity and policy credibility, our
results sit closer to a state-capacity-is-necessary-but-firm-level-frictions-bind-independently
story than to a straightforward institutional-complementarity one in which stronger regulatory
quality unlocks a latent policy effect that would otherwise lie dormant. Regulatory quality
matters — it raises the general baseline propensity to adopt green practices regardless of a firm's
own financing arrangement — but it does not appear to be the missing ingredient that would let a
green banking guideline reshape the credit-to-green channel specifically. This suggests, tentatively,
that the binding constraint on green credit policy's effectiveness in our sample is less about
whether the supervising jurisdiction has the state capacity to make the guideline credible, and more
about whether firms below a certain scale can absorb a green investment's fixed costs at all once
credit is available — a question about firm-level absorptive capacity that sits one level down from
the state-capacity question the SBFN framework itself is designed to address.

## 7. Conclusion

This paper set out to test whether the wave of green banking policy adoption coordinated through the
Sustainable Banking and Finance Network changes the relationship between firm-level access to
finance and green investment behaviour, and whether any such moderation depends on the regulatory
capacity available to make the underlying policy credible. Using harmonized World Bank Enterprise
Survey data spanning 41 economies' full 2018-2020 Green Economy Module rollout plus five further
economies as an out-of-region check, and applying a deliberately escalating sequence of
estimators — a classical benchmark chosen to expose its own limitation, a Bayesian hierarchical model
built to give the moderation hypothesis a fair test, and a causal forest imposing no functional-form
assumption at all — we find three consistent results. First, access to bank credit is robustly
associated with a firm's green practice adoption, a relationship that survives every specification,
subsample, and alternative-outcome check in the paper and replicates in five further economies
outside the primary sample. Second, neither SBFN policy adoption nor regulatory quality moderates
that relationship in any of the three estimators, though both shift the general level of green
adoption directly and substantially. Third, where genuine effect heterogeneity does exist, it is
concentrated at the level of firm size rather than country institutions.

For policy, the implication is not that green banking guidelines are ineffective, but that our
evidence does not support treating them as an effective lever specifically for widening the gap in
green investment between financed and unfinanced firms — the margin most green-credit-policy
literature implicitly assumes they operate on. If our tentative loan-tenor interpretation of the
overdraft-interaction finding is correct, policymakers designing or refining SBFN-style frameworks
may find more traction focusing supervisory attention on the term-lending instruments that actually
finance green capital expenditure, and on complementary measures — technical assistance, matching
grants, or credit guarantees — that address smaller firms' absorptive-capacity constraints directly,
rather than assuming that a bank-level supervisory mandate alone will reach firms regardless of
scale.

We close with four limitations that bound how far these conclusions travel. First, our design is a
single cross-section per country: it cannot rule out reverse causality (firms already predisposed to
green investment may find it easier to obtain credit) or unobserved, time-invariant country
characteristics correlated with both SBFN adoption and the baseline propensity to adopt green
practices, and our identification rests on firm-level variation in credit access interacting with a
plausibly firm-exogenous country-level policy indicator, not a natural experiment. Second, SBFN
membership is a binary proxy for what the network's own multi-tiered progression framework treats as
a genuinely graded process (Section 2); a natural extension would model policy stage — Commitment
through Consolidating — as an ordinal or continuous treatment rather than collapsing it to
membership status, which our binary coding necessarily does. Third, the six-economy extension sample
cannot re-test the SBFN contrast itself, since five of its six economies are SBFN members, and it
combines non-identical outcome items across countries by construction of the WBES's own shortened,
randomized module design in later survey waves — a genuine data-availability constraint rather than
a methodological choice. Fourth, the Worldwide Governance Indicators' regulatory-quality measure is
a broad, economy-wide governance indicator rather than a banking-supervision-specific capacity
measure; a supervisor-specific index, were one available consistently across this country set, would
sharpen the institutional-complementarity test considerably. We leave each of these to future work.

## Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work the author(s) used Claude (Anthropic) to assist with data
extraction and cleaning from World Bank Enterprise Surveys microdata, construction of the analysis
datasets and merge with country-level SBFN and Worldwide Governance Indicators data, execution of
the statistical and machine-learning analyses reported in Section 5, generation of Figures 1-2, and
drafting of portions of the manuscript text. After using this tool, the author(s) reviewed and
edited the content as needed and take full responsibility for the content of the published article.

