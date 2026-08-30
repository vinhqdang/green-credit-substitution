"""
Average marginal effect (probability scale) of fin_has_credit_line,
refit directly (avoids a patsy/pickle round-trip issue) for direct
comparability with the causal forest's ATE.
"""
import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_parquet('data/processed/analysis_main.parquet')
df['sbfn_member'] = pd.to_numeric(df['sbfn_member'], errors='coerce')
df = df.dropna(subset=['green_adoption_binary', 'fin_has_credit_line', 'sbfn_member',
                        'wgi_regulatory_quality', 'sector_broad', 'size_cat',
                        'log_sales', 'foreign_owned_dummy', 'exporter_dummy']).reset_index(drop=True)
df['sector_broad'] = df['sector_broad'].astype('category')
df['size_cat'] = df['size_cat'].astype('category')

formula = ('green_adoption_binary ~ fin_has_credit_line + log_sales + foreign_owned_dummy '
           '+ exporter_dummy + C(size_cat) + C(sector_broad)')
res = smf.logit(formula, data=df).fit(disp=0, cov_type='cluster', cov_kwds={'groups': df['country_survey_label']})
mfx = res.get_margeff(at='overall', method='dydx')
print(mfx.summary())
