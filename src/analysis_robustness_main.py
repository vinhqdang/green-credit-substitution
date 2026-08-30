"""
Table 8: additional robustness on the main ECA-MENA sample --
(a) continuous green_adoption_index via OLS instead of the binary via logit;
(b) alternative finance measures (overdraft; finance obstacle, reverse-coded);
(c) manufacturing-only and services-only subsample splits.
All retain sector FE (where applicable) and country-clustered SE, no country FE
(same rationale as the Section 4.3 baseline).
"""
import pandas as pd
import statsmodels.formula.api as smf

pd.set_option('display.width', 160)

df = pd.read_parquet('data/processed/analysis_main.parquet')
df['sbfn_member'] = pd.to_numeric(df['sbfn_member'], errors='coerce')
base = df.dropna(subset=['green_adoption_binary', 'green_adoption_index', 'fin_has_credit_line',
                          'fin_has_overdraft', 'fin_obstacle_access_to_finance', 'sbfn_member',
                          'wgi_regulatory_quality', 'sector_broad', 'size_cat',
                          'log_sales', 'foreign_owned_dummy', 'exporter_dummy']).reset_index(drop=True)
base['sector_broad'] = base['sector_broad'].astype('category')
base['size_cat'] = base['size_cat'].astype('category')

controls = "log_sales + foreign_owned_dummy + exporter_dummy + C(size_cat) + C(sector_broad)"


def cluster_fit(formula, data, family='logit'):
    if family == 'logit':
        return smf.logit(formula, data=data).fit(disp=0, cov_type='cluster',
                                                   cov_kwds={'groups': data['country_survey_label']})
    return smf.ols(formula, data=data).fit(cov_type='cluster',
                                             cov_kwds={'groups': data['country_survey_label']})


print('=== (a) Continuous index, OLS ===')
res_a = cluster_fit(f'green_adoption_index ~ fin_has_credit_line * sbfn_member + {controls}', base, 'ols')
print(res_a.summary())

print('\n=== (b1) Overdraft instead of credit line ===')
res_b1 = cluster_fit(f'green_adoption_binary ~ fin_has_overdraft * sbfn_member + {controls}', base)
print(res_b1.summary())

print('\n=== (b2) Finance obstacle (reverse-coded: higher = more access) ===')
base['fin_access_ease'] = 4 - base['fin_obstacle_access_to_finance']
res_b2 = cluster_fit(f'green_adoption_binary ~ fin_access_ease * sbfn_member + {controls}', base)
print(res_b2.summary())

print('\n=== (c1) Manufacturing subsample ===')
manuf = base[base['sector_broad'] == 'Manufacturing'].reset_index(drop=True)
res_c1 = cluster_fit(f'green_adoption_binary ~ fin_has_credit_line * sbfn_member + log_sales + '
                      f'foreign_owned_dummy + exporter_dummy + C(size_cat)', manuf)
print(f'N={len(manuf)}')
print(res_c1.summary())

print('\n=== (c2) Services subsample ===')
serv = base[base['sector_broad'] == 'Services'].reset_index(drop=True)
res_c2 = cluster_fit(f'green_adoption_binary ~ fin_has_credit_line * sbfn_member + log_sales + '
                      f'foreign_owned_dummy + exporter_dummy + C(size_cat)', serv)
print(f'N={len(serv)}')
print(res_c2.summary())
