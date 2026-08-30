## 4. Data and methodology

### 4.1 Data sources and sample construction

The paper's firm-level data come from the World Bank Enterprise Surveys (WBES), a standardized, stratified-random-sample survey of formal-sector, non-agricultural, non-extractive private firms with at least five employees, conducted by the World Bank's Enterprise Analysis Unit. Our primary analysis sample is the World Bank's own harmonized cross-country file combining the 41 Europe and Central Asia (ECA) and Middle East and North Africa (MENA) economies surveyed under a single, identical questionnaire between 2018 and 2020, the survey wave in which the Bank's Green Economy module — a battery of questions on emissions monitoring, energy-consumption targets, and the adoption of specific climate-friendly production measures — was fielded in full to every respondent. This yields 28,042 firm-level observations across 41 economies (Table 1). We supplement this primary sample with 15,556 additional firm observations from six further economies (Bangladesh 2022, India 2022, Indonesia 2023, Peru 2023, Philippines 2023, Timor-Leste 2021) in which a shortened, partially randomized version of the Green Economy module was fielded; because the exact item wording and randomized sub-module assignment differ across these six economies, we do not pool them into the main harmonized outcome variable, and instead use them as an out-of-region external-validity check on a narrower, honestly-matched pair of indicators (CO2-emissions monitoring, available in five of the six; waste-minimization adoption, available in five of the six, with different specific economies covered by each), reported separately in Section 5.5.

Country-level data are drawn from two sources. SBFN policy-adoption status, join year, and progression-framework stage as of each economy's survey year are compiled from the Sustainable Banking and Finance Network's Global Progress Reports (2018, 2019, 2021, 2023-2024), country-level Progress Report addenda, and the network's live country-profile data portal, cross-checked against IFC press releases announcing individual member accessions; economies that joined SBFN only after their WBES survey year are coded as non-adopters as of that year (Section 2). Regulatory capacity is measured with the World Bank's Worldwide Governance Indicators (WGI) Regulatory Quality estimate, matched to each economy's exact survey year via the World Bank DataBank API.

### 4.2 Variable construction

**Outcome.** Our primary dependent variable, *green practice adoption*, is a binary indicator equal to one if a firm reports having adopted at least one of seven Green Economy module practices over the preceding three years: more climate-friendly on-site energy generation, an energy-management system, waste-minimization or recycling measures, air-pollution control measures, other pollution-control measures, any energy-efficiency measure, or the use of on-site renewable energy. We also construct a continuous *green adoption index*, the mean of the same seven binary items, for robustness.

**Treatment.** *Bank credit access* is a binary indicator equal to one if the firm reports holding a line of credit or loan from a formal financial institution at the time of the survey.

**Country-level moderators.** *SBFN member* is a binary indicator equal to one if the economy had adopted a national SBFN sustainable-finance policy framework as of the survey year. *Regulatory quality* is the WGI Regulatory Quality estimate for the survey year (continuous, standardized to mean zero, unit standard deviation within the estimation sample for the hierarchical and machine-learning specifications).

**Controls.** Firm size (small/medium/large, per the Enterprise Surveys' own sampling strata), broad sector (manufacturing, services, construction), log sales, an exporter dummy (any direct or indirect export share), and a foreign-ownership dummy (any private foreign ownership share).

Table 2 lists every variable used in the analysis together with its exact WBES question code and source, in the interest of full transparency about variable construction given the multi-source nature of the merge.

### 4.3 Empirical strategy

We estimate the relationship between bank credit access and green practice adoption, and its moderation by SBFN status and regulatory quality, in four stages of increasing methodological sophistication, each addressing a specific limitation of the one before it.

**Stage 1 — classical benchmark.** We first estimate a pooled logistic regression,

$$\Pr(\text{Green}_{i,c}=1) = \Lambda\big(\beta_1 \text{Credit}_{i,c} + \beta_2 \text{SBFN}_c + \beta_3 (\text{Credit}_{i,c}\times \text{SBFN}_c) + \mathbf{X}_{i,c}'\boldsymbol{\gamma} + \delta_{s(i)}\big)$$

for firm $i$ in country $c$, where $\mathbf{X}_{i,c}$ is the firm-control vector and $\delta_{s(i)}$ is a sector fixed effect, with standard errors clustered by country. We deliberately do not include country fixed effects in this specification: because $\text{SBFN}_c$ is constant within country in a single cross-sectional wave, a country fixed effect would absorb it — and its interaction with $\text{Credit}_{i,c}$ — completely, making $\beta_2$ and $\beta_3$ unidentifiable by construction. This is not a modelling choice we are free to make differently; it is the reason a purely classical fixed-effects approach cannot answer H2/H3 as posed, and we report this specification, extended with a triple interaction for $\text{Regulatory quality}_c$, precisely to make that limitation visible.

**Stage 2 — Bayesian hierarchical (multilevel) model.** We re-estimate the same relationship allowing country to enter as a random rather than fixed effect, with a random slope on $\text{Credit}$:

$$\text{Green}_{i,c} \sim \text{Bernoulli}(p_{i,c}), \quad \text{logit}(p_{i,c}) = (\beta_1 + u_{1,c})\,\text{Credit}_{i,c} + \beta_2 \text{SBFN}_c + \beta_3(\text{Credit}_{i,c}\times \text{SBFN}_c) + \beta_4 (\text{Credit}_{i,c}\times \text{RegQuality}_c) + \mathbf{X}_{i,c}'\boldsymbol{\gamma} + (\alpha + u_{0,c})$$

$$\begin{pmatrix} u_{0,c} \\ u_{1,c} \end{pmatrix} \sim \mathcal{N}\left(\mathbf{0}, \boldsymbol{\Sigma}\right)$$

estimated via Hamiltonian Monte Carlo (No-U-Turn Sampler) in PyMC. This specification is the paper's primary vehicle for testing H2 and H3: because country enters through a variance component rather than a full set of dummies, the country-level moderators $\text{SBFN}_c$ and $\text{RegQuality}_c$ remain identified, while the random slope $u_{1,c}$ still absorbs unobserved country heterogeneity in the credit-green relationship and, together with partial pooling across countries, gives more defensible inference than cluster-robust standard errors computed over only 41 clusters (Cameron and Miller, 2015).

**Stage 3 — causal forest / double machine learning.** To avoid imposing a linear interaction functional form on how the treatment effect of credit access varies across the institutional landscape, we additionally estimate a Causal Forest with Double Machine Learning (Wager and Athey, 2018; Chernozhukov et al., 2018; Athey, Tibshirani, and Wager, 2019), using gradient-boosted nuisance models for the outcome and treatment propensity, and firm size, export status, SBFN status, and regulatory quality as effect-modifying features. This lets us recover conditional average treatment effects (CATEs) — the estimated effect of credit access on green adoption, separately for SBFN members versus non-members, and separately by regulatory-quality tercile — without imposing that the moderation take the single-coefficient interaction form assumed in Stages 1-2.

**Stage 4 — extension-sample robustness.** Finally, we re-estimate a reduced-form version of the credit-green relationship on the six-economy extension sample described above, using whichever of the two harmonizable outcome indicators (CO2-emissions monitoring; waste-minimization adoption) is available for a given economy, as an out-of-region check on whether the qualitative relationship generalizes beyond the ECA-MENA sample that anchors Stages 1-3.
