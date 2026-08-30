"""
Table 7: extension-sample robustness. Pooled logit of the closest-available
green indicator (CO2 monitoring; separately, waste minimization) on finance
access, across the 5/6 extension economies where each item is available.
Country-clustered SE. Descriptive country-level rates also reported.
"""
import pandas as pd
import statsmodels.formula.api as smf

pd.set_option('display.width', 160)

df = pd.read_parquet('data/processed/analysis_extension.parquet')
df['sbfn_member'] = pd.to_numeric(df['sbfn_member'], errors='coerce')

print('=== Country-level descriptive rates ===')
desc = df.groupby('country_survey_label').agg(
    n=('firm_id', 'count'),
    co2_monitor_rate=('co2_monitor', 'mean'),
    waste_min_rate=('waste_minimization', 'mean'),
    overdraft_rate=('fin_has_overdraft', 'mean'),
    sbfn_member=('sbfn_member', 'first'),
)
print(desc)
desc.to_csv('data/processed/table7_extension_descriptives.csv')

controls = "log_sales + foreign_owned_dummy + exporter_dummy + C(size_cat)"

for outcome in ['co2_monitor', 'waste_minimization']:
    sub = df.dropna(subset=[outcome, 'fin_has_overdraft', 'log_sales',
                             'foreign_owned_dummy', 'exporter_dummy', 'size_cat']).reset_index(drop=True)
    sub['size_cat'] = sub['size_cat'].astype('category')
    n_countries = sub['country_survey_label'].nunique()
    print(f'\n=== {outcome} pooled logit (N={len(sub)}, countries={n_countries}) ===')
    formula = f'{outcome} ~ fin_has_overdraft + {controls}'
    res = smf.logit(formula, data=sub).fit(disp=0, cov_type='cluster',
                                            cov_kwds={'groups': sub['country_survey_label']})
    print(res.summary())
