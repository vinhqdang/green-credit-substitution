## 5. Results

### 5.1 Descriptive patterns

Table 1 reports the full 41-economy sample composition; firm counts range from 150 (Montenegro) to
3,075 (Egypt), and the raw, unconditional green-practice-adoption rate ranges more than three-fold
across economies, from 30.3% (Egypt) to 90.1% (Malta). Figure 1 maps this variation alongside SBFN
policy status: 8 of the 41 primary-sample economies had adopted an SBFN framework as of their
survey year (Georgia, Egypt, Jordan, Kyrgyz Republic, Mongolia, Morocco, Tunisia, and Türkiye) — 13 of
the full 47-economy sample once the five (of six) SBFN-member small-sample supplementary economies
are counted — and every European Union member state in the sample is, consistent with SBFN's mandate,
a non-adopter. At the firm level, bank credit access correlates positively with the green-adoption
index (r = 0.18) but is essentially uncorrelated with a firm's own perceived finance obstacle
(r = -0.02) — a first hint, well before any regression, that realized access to credit rather than
perceived financing difficulty is what tracks green behaviour, and the two are evidently not
interchangeable measures of the same underlying constraint.

Figure 2 previews the paper's central finding graphically before a single regression is estimated:
plotting each economy's green-adoption rate against its regulatory-quality score and fitting separate
lines for SBFN members and non-members produces two lines of very similar, modestly positive slope,
separated by a roughly 15-20 percentage-point vertical gap — SBFN-member economies show *systematically
lower* raw green-adoption rates at every level of regulatory quality, not a steeper relationship between
regulatory quality and adoption. That combination — a level difference with no slope difference — is
exactly the signature the regression evidence below confirms formally.

### 5.2 Baseline classical benchmark (Table 4)

Table 4 reports the pooled logistic baseline. Column M1 confirms H1 on its own terms: firms with a
bank credit line are significantly more likely to have adopted a green practice (b = 0.571, p <
0.001; average marginal effect = 12.95 percentage points, 95% CI [7.7, 18.2]) — holding a formal
credit line is associated with roughly the same increase in the probability of green adoption as
moving from a small to a large firm, and a somewhat larger increase than being an exporter. Column M2
adds SBFN status and its interaction with credit access: the SBFN main effect is large, negative, and
precisely estimated (b = -0.991, p < 0.001), while the credit x SBFN interaction is small and
statistically indistinguishable from zero (b = 0.049, p = 0.773). Column M3's fully saturated triple
interaction with regulatory quality tells the same story at greater length: every interaction term
involving credit access is small and insignificant, while regulatory quality's uninteracted
relationship with adoption is positive, if only marginally significant in this particular fully-
saturated specification (b = 0.278, p = 0.110).

As flagged in Section 4.3, this specification cannot include country fixed effects without
mechanically absorbing the very SBFN and regulatory-quality terms the hypotheses concern, so what
Table 4 shows is a genuine test of H2/H3, not a placeholder — and that test returns no interaction. The
question the remaining stages are built to answer is whether that null result reflects a real
absence of policy moderation, or an artefact of forcing a two-level question (does a country-level
policy variable reshape a firm-level financing relationship?) through a single-level model with
country-clustered standard errors computed over only 41 clusters, a setting in which such standard
errors are known to be unreliable (Cameron and Miller, 2015).

### 5.3 Bayesian hierarchical model (Table 5) — primary test of H2/H3

The hierarchical specification — country-varying random slopes on credit access, cross-level
interactions with SBFN status and standardized regulatory quality, four chains of 1,000 post-warmup
draws each, all r-hat <= 1.01 and ess_bulk between 797 and 2,270 — is built specifically to give H2
and H3 a fair hearing that the absorbed classical specification could not. It does not change the
conclusion. Table 5 reports the full posterior summary; three results stand out.

First, the firm-level credit effect (H1) survives unchanged in substance: posterior mean 0.33 (89%
equal-tailed interval [0.18, 0.49]), comfortably excluding zero. Second, both country-level
institutional variables retain clean, precisely estimated **main** effects on the baseline
adoption rate — SBFN membership net-negative (-0.57, 89% ETI [-1.00, -0.09]), regulatory quality
net-positive (0.34, 89% ETI [0.16, 0.53]) — reproducing, with proper hierarchical uncertainty
quantification rather than an absorbed or clustered approximation, exactly the level-shift pattern
Figure 2 shows visually. Third, and centrally for H2 and H3, neither cross-level interaction is
distinguishable from zero: credit x SBFN, 0.072 (89% ETI [-0.26, 0.40]); credit x regulatory quality
(standardized), 0.004 (89% ETI [-0.13, 0.14]) — a near-exact zero on the latter, not merely an
imprecise one.

We read this as an honest and, we think, informative finding rather than a disappointing one: giving
the moderation hypothesis a hierarchical model built for precisely this two-level question still
returns no interaction, while sharpening (relative to the pooled baseline) the confidence with which
we can state that SBFN status and regulatory quality shift the *level* of green adoption directly.

### 5.4 Causal forest / heterogeneous treatment effects (Table 6)

Table 6 reports the Causal Forest DML estimates, which impose no linear-interaction functional form
and let the treatment effect vary flexibly across firm and country covariates. The overall average
treatment effect of credit access is 0.073 (95% CI [-0.040, 0.186]) — directionally consistent with,
though smaller in magnitude and less precisely estimated than, the logit average marginal effect of
0.130 in Section 5.2, reflecting the more conservative variance properties of a doubly-robust,
cross-fitted nonparametric estimator relative to a parametric logit on the same data. Critically,
the conditional average treatment effects triangulate with Section 5.3 rather than contradicting it:
the estimated effect is 0.072 for firms in non-SBFN economies versus 0.076 for firms in SBFN
economies, and 0.075 / 0.070 / 0.075 across the low/middle/high regulatory-quality terciles
respectively — three different institutional cuts, three essentially flat effects. Two entirely
independent estimators, one parametric and hierarchical, one nonparametric and forest-based, agree
on the absence of institutional moderation.

The forest's feature-importance decomposition adds a genuinely new result rather than only
confirming the null: of the four candidate effect-modifiers, firm size (log sales) accounts for
75.6% of the model's explained heterogeneity, versus 19.9% for regulatory quality, 2.6% for SBFN
status, and 1.9% for exporter status. Whatever heterogeneity exists in how strongly credit access
predicts green adoption is, on this evidence, primarily a firm-level rather than a
country-institutional phenomenon. Collapsing this into the Enterprise Surveys' own coarse size
strata (Table 6b), however, does not reveal a clean monotonic gradient: the estimated effect is 0.080
for small firms, 0.075 for medium firms, and 0.057 for large firms (all with wide, overlapping
confidence intervals spanning zero), which if anything runs opposite to a simple "larger firms
better absorb a green investment's fixed costs" story rather than confirming it. Read alongside the
75.6% importance share for the continuous size measure, we take this as evidence that the
heterogeneity the forest is detecting is more granular or non-monotonic across the firm-size
distribution than a three-category collapse can reveal, rather than evidence for any particular
direction of a size gradient — a qualification we report explicitly rather than paper over with a
tidier-sounding but unsupported claim. This redirects, rather than closes, the paper's
institutional-moderation question, and we return to it in Section 6.

### 5.5 Small-sample supplementary check: waste-minimization adoption (Table 7)

Before turning to the global-sample replication that is this paper's second major test (Section
5.7), Table 7 reports a smaller supplementary check using waste-minimization adoption — an outcome
not captured in the standardized cross-country database underlying the global sample, and so a
genuinely independent (if small-sample) data point — available in four economies whose Green Economy
modules asked this item under directly comparable wording: India 2022, Indonesia 2023, Peru 2023,
and Timor-Leste 2021. Three of these four are themselves SBFN members at various progression stages,
so this sample cannot re-test the SBFN-adoption contrast; what it can test is whether the
credit-to-green channel documented in Sections 5.2-5.4 is a peculiarity of the ECA-MENA sample or
generalizes elsewhere. It generalizes: pooled across the four economies, having an overdraft
facility is associated with significantly higher odds of waste-minimization adoption (b = 0.422,
p < 0.001, N = 9,038, 4 countries). The direction of the core finance-green relationship replicates
on a different continent, a different half-decade, and a narrower outcome definition than the one
anchoring Sections 5.2-5.4 — a preview, on four economies, of the much larger replication in
Section 5.7.

### 5.6 Additional robustness (Table 8)

Table 8 subjects the primary-sample finding to four further checks, all retaining sector fixed
effects, firm controls, and country-clustered standard errors (no country fixed effects, for the
reason given in Section 4.3). First, replacing the binary outcome with the continuous seven-item
green-adoption index and estimating by OLS reproduces the same pattern to the decimal: credit access
positive and significant (b = 0.053, p < 0.001), SBFN main effect negative and significant
(b = -0.092, p < 0.001), interaction indistinguishable from zero (b = 0.006, p = 0.739).

Second, replacing bank credit access with two alternative finance measures produces one genuine
point of nuance worth reporting rather than smoothing over. Using overdraft-facility access instead
of a credit line/loan, the main overdraft effect remains positive and significant (b = 0.274,
p = 0.011), the SBFN main effect remains negative and significant (b = -0.905, p < 0.001) — but the
overdraft x SBFN interaction is now negative and significant (b = -0.346, p = 0.031), the one
interaction term in the entire paper that clears a conventional significance threshold, and it runs
opposite to the direction H2 predicts. Using the reverse-coded perceived finance-obstacle measure in
place of realized access, by contrast, both the main effect and its SBFN interaction are precisely
zero (b = -0.010, p = 0.827; interaction b = -0.012, p = 0.849) — consistent with the descriptive
correlation noted in Section 5.1. We read the overdraft result as suggestive rather than
conclusive given it is one significant coefficient among more than a dozen interaction tests across
the paper, but it is at least directionally consistent with a substantive story worth flagging for
future work: if SBFN-guided lending is channelled preferentially through the term loans and credit
lines that finance long-horizon capital expenditure, rather than through short-term overdraft
facilities, we might expect exactly this pattern — a null-to-positive interaction on credit lines and
a negative one on overdrafts — though our data cannot directly test whether SBFN-guided credit is
disproportionately term-structured.

Third, splitting the sample into manufacturing (N = 13,340) and services (N = 9,538) subsamples
shows the credit-access main effect, the SBFN main effect, and the null credit x SBFN interaction all
replicate within each sector separately (manufacturing: credit b = 0.480, p < 0.001, interaction
b = -0.040, p = 0.826; services: credit b = 0.448, p < 0.001, interaction b = 0.195, p = 0.426) —
the paper's central null is not an artefact of pooling two structurally different production
technologies.

### 5.7 Global-sample replication with country fixed effects (Table 9)

The preceding six subsections establish the paper's central finding on the primary sample. We now
subject that finding to what we consider the most demanding test available to us: complete
re-estimation on an independently assembled, 162-economy global sample (Section 4.1), using a
different outcome variable (CO2-emissions monitoring rather than the seven-item composite), different
survey years (2021-2026 rather than 2018-2020), and, for the first time in the paper, a
country-fixed-effects specification that this much larger set of clusters can support. Figure 3 maps
the combined reach of the two samples together: 166 distinct economies, spanning every region and,
through the global sample specifically, extending for the first time in this literature into
high-income economies with no SBFN involvement at all.

Table 9 reports two specifications. Column M1, without country fixed effects, is the direct
global-sample analogue of Table 4's primary-sample baseline: credit access remains positive and
significant (b = 0.198, p = 0.039, N = 89,797, 159 countries), while the SBFN main effect
(b = -0.171, p = 0.353), the credit x SBFN interaction (b = 0.278, p = 0.430), and every
regulatory-quality interaction are statistically indistinguishable from zero. Column M2 imposes
country fixed effects, absorbing the SBFN and regulatory-quality main effects by construction (they
are collinear with the fixed effect, since both are constant within a given country-year) while
leaving their firm-level interactions with credit access fully identified, because credit access
itself varies within country. This is a sharper test than anything the primary sample's single
2018-2020 wave can support, and it returns the same answer with even more precision: credit access is
strongly significant (b = 0.249, p < 0.001), while the credit x SBFN interaction (b = 0.506,
p = 0.205) and the credit x regulatory-quality interaction (b = -0.044, p = 0.346) remain null.

We regard this as the paper's most important robustness result. It is not a re-analysis of the same
data under a different label: it is a different outcome construct, a different set of economies
(only a handful of which overlap with the primary sample), a different half-decade, and an
econometric specification — country fixed effects — that is only available at all because this
second sample has enough clusters to support it. That the qualitative conclusion is identical across
both samples and across the full set of four estimators reported in this paper (classical logit,
Bayesian hierarchical, causal forest, and now country-fixed-effects logit) is, we think, considerably
stronger evidence for the paper's central claim than either sample could offer alone.

### 5.8 Results summary across all specifications (Figures 4-5)

Sections 5.2-5.7 report ten tables spanning four estimators and two independent samples. Figure 4
consolidates every coefficient bearing on H1-H3 into a single view. Panel A shows the credit-access
effect (H1): every point estimate is positive and every confidence interval excludes zero, in both
samples and all four estimators. Panels B and C show the credit x SBFN and credit x regulatory-quality
interactions (H2, H3): every single confidence interval, across both samples and every estimator,
straddles zero. Figure 5 shows the same non-result from a completely different angle — the causal
forest's conditional average treatment effects broken out by SBFN status, regulatory-quality tercile,
and firm-size category all overlap both each other and the overall average treatment effect. No
subgroup split, by any variable examined in this paper, recovers a distinguishable effect.
