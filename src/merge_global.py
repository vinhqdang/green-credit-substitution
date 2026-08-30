"""
Merge the 162-country global firm-level sample with SBFN status and WGI
regulatory quality, producing the final analysis dataset.
"""
import pandas as pd

firm = pd.read_parquet('data/processed/firm_analysis_global.parquet')
sbfn = pd.read_csv('data/global_sbfn.csv')[['country_survey_label', 'sbfn_member', 'sbfn_join_year']]
wgi = pd.read_csv('data/global_wgi.csv')[['country_survey_label', 'wgi_regulatory_quality',
                                           'wgi_government_effectiveness']]

macro = sbfn.merge(wgi, on='country_survey_label', how='left')
merged = firm.merge(macro, on='country_survey_label', how='left', validate='many_to_one')

n_missing_sbfn = merged['sbfn_member'].isna().sum()
n_missing_wgi = merged['wgi_regulatory_quality'].isna().sum()
print(f"Merged: {merged.shape}")
print(f"Missing sbfn_member: {n_missing_sbfn}")
print(f"Missing wgi_regulatory_quality: {n_missing_wgi}")

if n_missing_wgi > 0:
    missing_countries = merged[merged['wgi_regulatory_quality'].isna()]['country_survey_label'].unique()
    print(f"Countries missing WGI: {list(missing_countries)}")

merged.to_parquet('data/processed/analysis_global.parquet')
print("\nSaved data/processed/analysis_global.parquet")
print("\nSBFN member distribution:")
print(merged.groupby('country_survey_label')['sbfn_member'].first().value_counts())
