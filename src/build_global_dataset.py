"""
Build the ~160-country global minimal-indicator sample from the master
standardized WBES database (2006-2026), for the expanded extension/
robustness analysis. Outcome: ge7 (CO2 emissions monitoring, last 3
years) -- the one item consistently available across this much larger
but thinner sample. Finance: k8 (credit line/loan), k7 (overdraft).
"""
import numpy as np
import pandas as pd
import re

CORE_PATH = 'raw_data/cross_economy/standardized_core/New_Comprehensive_July_28_2026.dta'
PROD_PATH_ZIP = 'raw_data/cross_economy/Productivity Database/Firm Level Factor Ratios_Data_and_Documentation.zip'


def recode_yn(s):
    return s.map({1: 1.0, 2: 0.0})


def main():
    cols = ['country', 'idstd', 'ge3', 'ge7', 'k7', 'k8', 'k30', 'a14y', 'b2b', 'd3b', 'd3c', 'd2']
    df = pd.read_stata(CORE_PATH, columns=cols, convert_categoricals=False)
    df = df[df['ge7'].notna()].copy()
    print('Rows with ge7 non-null:', df.shape)
    print('Unique country-years:', df['country'].nunique())

    out = pd.DataFrame(index=df.index)
    out['country_survey_label'] = df['country']
    out['firm_id'] = df['idstd']
    out['survey_year'] = df['a14y']
    out['co2_monitor'] = recode_yn(df['ge7'])
    out['climate_damage_exposure'] = recode_yn(df['ge3'])
    out['fin_has_overdraft'] = recode_yn(df['k7'])
    out['fin_has_credit_line'] = recode_yn(df['k8'])
    out['fin_obstacle_access_to_finance'] = df['k30'].where(df['k30'] >= 0)

    out['pct_foreign_owned'] = df['b2b'].where(df['b2b'] >= 0)
    out['foreign_owned_dummy'] = (out['pct_foreign_owned'] > 0).astype(float)
    out.loc[out['pct_foreign_owned'].isna(), 'foreign_owned_dummy'] = np.nan

    exp_ind = df['d3b'].where(df['d3b'] >= 0, np.nan)
    exp_dir = df['d3c'].where(df['d3c'] >= 0, np.nan)
    out['export_share'] = (exp_ind.fillna(0) + exp_dir.fillna(0)).where(exp_ind.notna() | exp_dir.notna())
    out['exporter_dummy'] = (out['export_share'] > 0).astype(float)

    sales = df['d2'].where(df['d2'] > 0)
    out['log_sales'] = np.log(sales)

    # merge sector + size proxy from Productivity Database via idstd
    import zipfile
    with zipfile.ZipFile(PROD_PATH_ZIP) as z:
        dta_name = [n for n in z.namelist() if n.endswith('.dta')][0]
        with z.open(dta_name) as src, open('raw_data/_tmp_prod_full.dta', 'wb') as dst:
            dst.write(src.read())
    prod = pd.read_stata('raw_data/_tmp_prod_full.dta', convert_categoricals=False)
    print('\nProductivity DB columns:', list(prod.columns))
    prod_keep = prod[['idstd', 'sector_MS']].drop_duplicates(subset='idstd')
    out = out.merge(prod_keep, left_on='firm_id', right_on='idstd', how='left', suffixes=('', '_prod'))
    out['sector_broad'] = out['sector_MS']
    out.drop(columns=['sector_MS'], errors='ignore', inplace=True)
    if 'idstd_prod' in out.columns:
        out.drop(columns=['idstd_prod'], inplace=True)

    print('\nsector_broad match rate:', out['sector_broad'].notna().sum(), '/', len(out))

    import os
    os.remove('raw_data/_tmp_prod_full.dta')

    # fold in Bangladesh 2022 and Indonesia 2023: both use the "_BR" randomized
    # module naming, absent from the master file's harmonized ge7/ge8 columns,
    # but already extracted (as co2_monitor) in our hand-built extension sample
    ext = pd.read_parquet('data/processed/firm_analysis_extension.parquet')
    ext_bd_id = ext[ext['country_survey_label'].isin(['Bangladesh2022', 'Indonesia2023'])].copy()
    ext_bd_id['co2_monitor'] = ext_bd_id['co2_monitor']
    ext_bd_id['climate_damage_exposure'] = np.nan
    keep_cols = ['country_survey_label', 'firm_id', 'survey_year', 'co2_monitor',
                 'climate_damage_exposure', 'fin_has_overdraft', 'fin_has_credit_line',
                 'fin_obstacle_access_to_finance', 'pct_foreign_owned', 'foreign_owned_dummy',
                 'export_share', 'exporter_dummy', 'log_sales', 'sector_broad']
    for c in keep_cols:
        if c not in ext_bd_id.columns:
            ext_bd_id[c] = np.nan
    out = pd.concat([out[keep_cols], ext_bd_id[keep_cols]], ignore_index=True)

    out.to_parquet('data/processed/firm_analysis_global.parquet')
    print('\nSaved data/processed/firm_analysis_global.parquet', out.shape)
    print('Country-years:', out['country_survey_label'].nunique())

    # unique country-year list for the ISO mapping / SBFN-WGI lookup
    unique_countries = sorted(out['country_survey_label'].unique())
    with open('data/global_country_list.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(unique_countries))
    print(f'\nWrote {len(unique_countries)} country-year labels to data/global_country_list.txt')


if __name__ == '__main__':
    main()
