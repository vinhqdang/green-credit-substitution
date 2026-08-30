"""
Build a harmonized firm-level dataset for the 6 non-ECA-MENA Green Economy
survey waves (Bangladesh2022, India2022, Indonesia2023, Peru2023,
Philippines2023, Timor-Leste2021).

These surveys used a shortened/randomized Green Economy module with
country-specific variable names, so only a narrower common indicator set
is harmonized here: CO2-emissions monitoring (5/6 countries; India lacks
this item) and waste-minimization/recycling adoption (5/6 countries;
Philippines lacks this item). Both are kept, each with its own valid
country coverage, rather than forcing a single pooled proxy across all six.

Output: data/processed/firm_analysis_extension.parquet
"""
import numpy as np
import pandas as pd

FILES = {
    'Bangladesh2022': 'raw_data/green_economy_other/WBES_Bangladesh2022_Data/Bangladesh-2022-full-data.dta',
    'India2022': 'raw_data/green_economy_other/WBES_India2022_Data/India-2022-full-data.dta',
    'Indonesia2023': 'raw_data/green_economy_other/WBES_Indonesia2023_Data/Indonesia-2023-full-data.dta',
    'Peru2023': 'raw_data/green_economy_other/WBES_Peru2023_Data/Peru-2023-full-data.dta',
    'Philippines2023': 'raw_data/green_economy_other/WBES_Philippines2023_Data/Philippines-2023-full-data.dta',
    'Timor-Leste2021': 'raw_data/green_economy_other/WBES_Timor-Leste2021_Data/Timor-Leste-2021-full-data.dta',
}

# per-country variable name map: co2 monitor item, waste-minimization item
GE_VARMAP = {
    'Bangladesh2022':   dict(co2_monitor='BMGc8',  waste_min=None),        # BMGc23m is a near-proxy, not identical wording -> excluded
    'India2022':        dict(co2_monitor=None,     waste_min='BMGc23e'),
    'Indonesia2023':    dict(co2_monitor='ge7_BR', waste_min='ge8e_BR'),
    'Peru2023':         dict(co2_monitor='ge7',    waste_min='ge8e'),
    'Philippines2023':  dict(co2_monitor='ge7',    waste_min=None),
    'Timor-Leste2021':   dict(co2_monitor='TLge7',  waste_min='TLge8e'),
}

SURVEY_YEAR = {
    'Bangladesh2022': 2022, 'India2022': 2022, 'Indonesia2023': 2023,
    'Peru2023': 2023, 'Philippines2023': 2023, 'Timor-Leste2021': 2021,
}


def recode_yn(s):
    return s.map({1: 1.0, 2: 0.0})


def load_one(label, path):
    df = pd.read_stata(path, convert_categoricals=False)
    out = pd.DataFrame(index=df.index)
    out['country_survey_label'] = label
    out['firm_id'] = df['idstd']
    out['survey_year'] = SURVEY_YEAR[label]
    out['size_cat'] = df['a6a'].map({1: 'Small', 2: 'Medium', 3: 'Large'})
    out['legal_status'] = df['b1'].where(df['b1'] > 0)

    vm = GE_VARMAP[label]
    out['co2_monitor'] = recode_yn(df[vm['co2_monitor']]) if vm['co2_monitor'] else np.nan
    out['waste_minimization'] = recode_yn(df[vm['waste_min']]) if vm['waste_min'] else np.nan

    out['fin_has_overdraft'] = recode_yn(df['k7'])
    out['fin_obstacle_access_to_finance'] = df['k30'].where(df['k30'] >= 0)
    out['fin_pct_workingcap_bank'] = df['k3bc'].where(df['k3bc'] >= 0)
    out['fin_pct_workingcap_nonbank'] = df['k3e'].where(df['k3e'] >= 0)
    # k8/k16 not present in all six extension files -> excluded from this sample
    if 'k8' in df.columns:
        out['fin_has_credit_line'] = recode_yn(df['k8'])
    else:
        out['fin_has_credit_line'] = np.nan

    out['pct_foreign_owned'] = df['b2b'].where(df['b2b'] >= 0)
    out['foreign_owned_dummy'] = (out['pct_foreign_owned'] > 0).astype(float)
    out.loc[out['pct_foreign_owned'].isna(), 'foreign_owned_dummy'] = np.nan

    exp_ind = df['d3b'].where(df['d3b'] >= 0, np.nan)
    exp_dir = df['d3c'].where(df['d3c'] >= 0, np.nan)
    out['export_share'] = (exp_ind.fillna(0) + exp_dir.fillna(0)).where(exp_ind.notna() | exp_dir.notna())
    out['exporter_dummy'] = (out['export_share'] > 0).astype(float)

    sales = df['d2'].where(df['d2'] > 0)
    out['log_sales'] = np.log(sales)

    return out


def main():
    parts = [load_one(label, path) for label, path in FILES.items()]
    ext = pd.concat(parts, ignore_index=True)
    ext.to_parquet('data/processed/firm_analysis_extension.parquet')
    print('Saved extension sample:', ext.shape)
    print(ext.groupby('country_survey_label')[['co2_monitor', 'waste_minimization', 'fin_has_overdraft']].mean())


if __name__ == '__main__':
    main()
