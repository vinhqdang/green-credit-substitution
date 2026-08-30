"""
Appendix A: full 47-economy SBFN status/sourcing table (transparency device,
mirrors Paper 2's per-variable Source column applied at the country level).
Appendix B: Bayesian model convergence diagnostics for every parameter.
"""
import pandas as pd

macro = pd.read_csv('data/macro_moderators.csv')
appendix_a = macro[['country_survey_label', 'sbfn_member', 'sbfn_join_year',
                     'sbfn_policy_stage_at_survey', 'wgi_regulatory_quality', 'wgi_year_used']].copy()
appendix_a = appendix_a.sort_values('country_survey_label')
appendix_a.to_csv('data/processed/appendix_a_sbfn_status.csv', index=False)
print('Saved data/processed/appendix_a_sbfn_status.csv')
print(appendix_a)
