## 6. Supplementary evidence: a country-level staggered event-study on macro environmental outcomes

Sections 5.2-5.8 establish this paper's central finding using firm-level cross-sectional data, for the
data-availability reasons given in Section 4: the WBES Green Economy module cannot support a staggered
difference-in-differences or event-study design around each economy's own SBFN adoption date, because
it has not been fielded as a repeated panel instrument. That constraint applies to the firm-level
finance-to-green-investment channel specifically; it does not apply to a different, complementary
question that the same SBFN adoption-timing variation can answer directly: does a country's aggregate
environmental trajectory shift around its own SBFN adoption date? This section builds and reports that
test, using an entirely independent data source and unit of analysis, precisely because it is the
identification strategy this literature -- and this special issue in particular -- asks for, and because
a genuine answer, however it comes out, is more useful than leaving the question unaddressed.

### 6.1 Data and design

We assemble a country-year panel spanning every World Bank member economy with a non-aggregate ISO3
code (217 economies), 2000-2024. Treatment timing is each economy's SBFN join year, drawn from the same
SBFN data portal membership roster used to construct the global sample (Section 4) and cross-checked
against the global-sample SBFN coding used in Section 5.7 (zero disagreements across 61 overlapping
economies); economies that have never joined SBFN, as of
the roster's most recent update, serve as the never-treated comparison group. This yields 68
ever-treated economies (join years 2012-2024, the same real staggered-adoption variation described in
Section 2) and 149 never-treated economies. Outcome data come from the World Bank's World Development
Indicators, retrieved via the World Bank DataBank API: renewable energy consumption (% of total final energy
consumption, `EG.FEC.RNEW.ZS`) and CO2 emissions per capita (AR5 GWP-consistent series,
`EN.GHG.CO2.PC.CE.AR5`), both available for the large majority of economies from 2000 through at least
2021-2024. We additionally draw on GDP per capita (constant 2015 US$, `NY.GDP.PCAP.KD`) as a covariate, to
net out the obvious confound that SBFN-adopting economies are disproportionately still-industrializing,
faster-growing economies whose emissions profiles are shaped by their development stage independently
of any banking-sector policy.

We estimate the effect of SBFN adoption on each outcome using the Callaway and Sant'Anna (2021)
staggered-adoption difference-in-differences estimator, which recovers group-time average treatment
effects for each adoption cohort separately and aggregates them into an overall average treatment
effect on the treated (ATT) and an event-study profile, using only never-treated economies as the
comparison group. We report this estimator, rather than a standard two-way-fixed-effects (TWFE)
regression, because TWFE is now well known to produce badly biased estimates under staggered treatment
timing when already-treated units are implicitly used as controls for later-treated units
(Goodman-Bacon, 2021); we report a naive TWFE specification alongside the Callaway-Sant'Anna estimates
specifically to illustrate the size of that bias in our own data, rather than as a candidate preferred
estimate. For each outcome we report both an unconditional specification and a doubly-robust
specification conditioning on log GDP per capita.

### 6.2 Results

Table 11 reports the overall ATT for both outcomes under three specifications; Figure 6 plots the full
event-study profile (doubly-robust, GDP-per-capita-controlled specification) for both outcomes.

**Table 11. Country-level staggered event-study: overall average treatment effect of SBFN adoption on
macro environmental outcomes.** Callaway-Sant'Anna estimator, never-treated comparison group, 999
bootstrap iterations; naive TWFE reported for comparison only. Full country-year panel, 2000-2024.

| Outcome | Specification | ATT | SE | 95% CI |
| --- | --- | --- | --- | --- |
| Renewable energy % | Callaway-Sant'Anna, no covariates | -1.192 | 0.802 | [-2.763, 0.380] |
| Renewable energy % | Callaway-Sant'Anna, doubly-robust, log GDP p.c. | 0.674 | 0.916 | [-1.122, 2.470] |
| Renewable energy % | Naive TWFE (post dummy, country+year FE) | -4.672\*\*\* | 1.127 | [-6.882, -2.463] |
| CO2 per capita | Callaway-Sant'Anna, no covariates | 0.631\*\*\* | 0.179 | [0.280, 0.982] |
| CO2 per capita | Callaway-Sant'Anna, doubly-robust, log GDP p.c. | 0.349\*\* | 0.156 | [0.044, 0.655] |
| CO2 per capita | Naive TWFE (post dummy, country+year FE) | 0.901\*\*\* | 0.204 | [0.500, 1.302] |

*** 95% CI excludes zero; ** 95% CI excludes zero, narrower margin. Underlying data and code in the
replication package.

Two results, read together, do not support treating SBFN adoption as a country-level lever that
visibly improves aggregate environmental outcomes -- which is itself informative, since this is the
identification strategy best suited to answer that specific question directly. First, renewable energy
share shows no effect distinguishable from zero in either specification, and the doubly-robust
event-study profile (Figure 6, left panel) is flat and precisely estimated on both sides of the
adoption date: a clean null, not an underpowered one.

Second, CO2 emissions per capita shows a positive (i.e., the "wrong-signed" direction if SBFN adoption
reduced emissions) and statistically significant association with adoption in every specification, but
three features of the result argue against reading it causally. It shrinks by roughly 45% (0.631 to
0.349) once we condition on log GDP per capita, indicating that a substantial share of the raw
association is attributable to exactly the development-stage confound we set out to net out. The
doubly-robust event-study profile (Figure 6, right panel) shows a small, mostly flat pre-period with
only two marginally significant leads, followed by a post-period effect that grows smoothly and
monotonically from near zero at adoption to its largest magnitude nine to twelve years out -- a
continuing-divergence pattern more consistent with SBFN-adopting economies already sitting on a
different, faster-rising emissions trajectory than non-adopters (which a single covariate cannot fully
absorb) than with a discrete policy-caused jump at the adoption date. And the naive TWFE estimate
(0.901) is itself more than double the doubly-robust Callaway-Sant'Anna estimate (0.349), the same
direction of bias documented in the staggered-DID literature and a useful internal illustration of why
we lead with the more robust estimator throughout this section.

We are deliberately not spinning this into either a "green banking policy backfires" or a "green
banking policy works" claim. The honest reading is that a macro-level design -- built using exactly the
identification strategy (staggered adoption timing, a proper Callaway-Sant'Anna estimator, never-treated
controls) this special issue's own methodological expectations call for -- also does not produce clean
evidence that SBFN adoption changes a country's aggregate environmental trajectory for the better, and
the one statistically significant result we do find is more parsimoniously explained by which economies
self-select into SBFN membership than by what the policy itself does once adopted. This is, we think, a
genuinely different and complementary piece of evidence to Sections 5.2-5.7's firm-level results, not a
restatement of them: different data source, different unit of analysis, different outcome constructs,
and, for the first time in this paper, an identification strategy that exploits exogenous variation in
adoption *timing* rather than relying on cross-sectional comparison across adopters and non-adopters.
That it converges on the same substantive conclusion -- no clean evidence of a beneficial institutional
effect -- from a design built specifically to meet a bar the paper's firm-level evidence cannot meet,
strengthens rather than substitutes for the paper's central finding.
