"""
Table 2 (baseline, "naive" benchmark): pooled OLS/Logit with sector fixed
effects and country-clustered standard errors. Country fixed effects are
deliberately NOT included here, because SBFN status is a country-level,
time-invariant variable in this single-wave cross-section: including
country FE would perfectly absorb it (and its interactions), leaving
nothing to estimate. That absorption problem is the paper's methodological
bridge to the hierarchical model in analysis_multilevel.py.
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm

pd.set_option('display.width', 160)


def load():
    df = pd.read_parquet('data/processed/analysis_main.parquet')
    df['sbfn_member'] = pd.to_numeric(df['sbfn_member'], errors='coerce')
    df = df.dropna(subset=['green_adoption_binary', 'fin_has_credit_line', 'sbfn_member',
                            'wgi_regulatory_quality', 'sector_broad', 'size_cat',
                            'log_sales', 'foreign_owned_dummy', 'exporter_dummy'])
    df['sector_broad'] = df['sector_broad'].astype('category')
    df['size_cat'] = df['size_cat'].astype('category')
    df = df.reset_index(drop=True)
    return df


def run_models(df):
    base_rhs = ('fin_has_credit_line + log_sales + foreign_owned_dummy + exporter_dummy '
                '+ C(size_cat) + C(sector_broad)')

    specs = {
        'M1_baseline': f'green_adoption_binary ~ {base_rhs}',
        'M2_sbfn_main': f'green_adoption_binary ~ fin_has_credit_line * sbfn_member + log_sales '
                         f'+ foreign_owned_dummy + exporter_dummy + C(size_cat) + C(sector_broad)',
        'M3_triple_interaction': f'green_adoption_binary ~ fin_has_credit_line * sbfn_member * wgi_regulatory_quality '
                                  f'+ log_sales + foreign_owned_dummy + exporter_dummy + C(size_cat) + C(sector_broad)',
    }

    results = {}
    for name, formula in specs.items():
        model = smf.logit(formula, data=df)
        res = model.fit(disp=0, cov_type='cluster', cov_kwds={'groups': df['country_survey_label']})
        results[name] = res
        print(f"\n=== {name} ===")
        print(res.summary())

    return results


if __name__ == '__main__':
    df = load()
    print('N firms:', len(df), '| N countries:', df['country_survey_label'].nunique())
    results = run_models(df)

    import pickle
    with open('data/processed/baseline_results.pkl', 'wb') as f:
        pickle.dump({k: v for k, v in results.items()}, f)
