"""
Build the harmonized firm-level analysis dataset from the WBES ECA-MENA
Green Economy Module combined file (41 economies, 2018-2020 rollout).

Output: data/processed/firm_analysis_eca_mena.parquet
"""
import numpy as np
import pandas as pd

RAW = 'raw_data/cross_economy/green_economy_eca_mena/combined WBES_ECA MENA_2020.dta'


def recode_yn(s):
    """WBES yes/no items: 1=Yes, 2=No, negative codes = missing."""
    return s.map({1: 1.0, 2: 0.0})


def main():
    df = pd.read_stata(RAW, convert_categoricals=False)

    out = pd.DataFrame(index=df.index)
    out['country_survey_label'] = df['country']
    out['firm_id'] = df['idstd']
    out['survey_year'] = df['a14y']
    out['sector_raw'] = df['a4ax'].replace('', np.nan)
    out['size_cat'] = df['a6a'].map({1: 'Small', 2: 'Medium', 3: 'Large'})
    out['legal_status'] = df['b1'].where(df['b1'] > 0)

    # --- Green Economy module outcomes (binary Yes/No) ---
    ge_items = {
        'ge_climate_energy_onsite': 'BMGc23b',   # climate-friendly energy generation on site
        'ge_energy_management': 'BMGc23d',
        'ge_waste_recycling': 'BMGc23e',
        'ge_air_pollution_control': 'BMGc23f',
        'ge_other_pollution_control': 'BMGc23j',
        'ge_energy_efficiency_any': 'BMGc25',
        'ge_uses_onsite_renewable': 'BMGe5',
        'ge_strategy_mentions_env': 'BMGa1',
        'ge_customer_env_certification_required': 'BMGa4',
        'ge_monitors_energy': 'BMGc1',
    }
    for new, old in ge_items.items():
        out[new] = recode_yn(df[old])

    green_components = [
        'ge_climate_energy_onsite', 'ge_energy_management', 'ge_waste_recycling',
        'ge_air_pollution_control', 'ge_other_pollution_control', 'ge_energy_efficiency_any',
        'ge_uses_onsite_renewable',
    ]
    out['green_adoption_index'] = out[green_components].mean(axis=1, skipna=True)
    out['green_adoption_binary'] = (out[green_components].sum(axis=1, skipna=True) > 0).astype(float)
    out.loc[out[green_components].isna().all(axis=1), 'green_adoption_binary'] = np.nan

    # --- Access-to-finance module ---
    out['fin_has_credit_line'] = recode_yn(df['k8'])
    out['fin_has_overdraft'] = recode_yn(df['k7'])
    out['fin_applied_new_loan'] = recode_yn(df['k16'])
    out['fin_obstacle_access_to_finance'] = df['k30'].where(df['k30'] >= 0)
    out['fin_pct_workingcap_bank'] = df['k3bc'].where(df['k3bc'] >= 0)
    out['fin_pct_workingcap_nonbank'] = df['k3e'].where(df['k3e'] >= 0)
    out['fin_pct_fixedassets_bank'] = df['k5bc'].where(df['k5bc'] >= 0)

    # --- Firm controls ---
    out['pct_foreign_owned'] = df['b2b'].where(df['b2b'] >= 0)
    out['foreign_owned_dummy'] = (out['pct_foreign_owned'] > 0).astype(float)
    out.loc[out['pct_foreign_owned'].isna(), 'foreign_owned_dummy'] = np.nan

    exp_ind = df['d3b'].where(df['d3b'] >= 0, np.nan)
    exp_dir = df['d3c'].where(df['d3c'] >= 0, np.nan)
    out['export_share'] = (exp_ind.fillna(0) + exp_dir.fillna(0)).where(exp_ind.notna() | exp_dir.notna())
    out['exporter_dummy'] = (out['export_share'] > 0).astype(float)

    sales = df['d2'].where(df['d2'] > 0)
    out['log_sales'] = np.log(sales)

    # --- Broad sector grouping ---
    manuf_terms = ['Metal', 'Chemical', 'Food', 'Furniture', 'Leather', 'Machinery',
                   'Manufacturing', 'Mineral', 'Petroleum', 'Rubber', 'Textiles', 'Garments',
                   'Wood']
    services_terms = ['Hospitality', 'Hotels', 'Retail', 'Services', 'Wholesale', 'Motor Vehicles']
    construction_terms = ['Construction']

    def broad_sector(s):
        if pd.isna(s):
            return np.nan
        if any(t in s for t in construction_terms):
            return 'Construction'
        if any(t in s for t in manuf_terms):
            return 'Manufacturing'
        if any(t in s for t in services_terms):
            return 'Services'
        return 'Other'

    out['sector_broad'] = out['sector_raw'].map(broad_sector)

    out.to_parquet('data/processed/firm_analysis_eca_mena.parquet')
    print('Saved:', out.shape)
    print(out[['green_adoption_binary', 'fin_has_credit_line', 'fin_obstacle_access_to_finance',
               'sector_broad']].describe(include='all'))
    print('\nCountry-year units:', out['country_survey_label'].nunique())


if __name__ == '__main__':
    main()
