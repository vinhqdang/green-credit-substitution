"""
Follow-up on the causal forest's headline result (firm size explains 75.6%
of effect heterogeneity): compute CATEs by firm-size category directly,
reusing the already-fitted model (joblib -- trusted, locally-generated file).
"""
import joblib  # trusted, locally-generated file (written by analysis_causalforest.py in this repo)
import numpy as np
import pandas as pd

pd.set_option('display.width', 160)


def load():
    df = pd.read_parquet('data/processed/analysis_main.parquet')
    df['sbfn_member'] = pd.to_numeric(df['sbfn_member'], errors='coerce')
    keep = ['green_adoption_binary', 'fin_has_credit_line', 'sbfn_member',
            'wgi_regulatory_quality', 'log_sales', 'foreign_owned_dummy',
            'exporter_dummy', 'size_cat', 'sector_broad', 'country_survey_label']
    df = df.dropna(subset=keep).reset_index(drop=True)
    return df


def main():
    bundle = joblib.load('data/processed/causalforest_model.joblib')
    est = bundle['est']
    het_cols = bundle['X_cols']

    df = load()
    X = df[het_cols].astype(float).values

    print('CATEs by firm size category:')
    rows = []
    for size in ['Small', 'Medium', 'Large']:
        mask = (df['size_cat'] == size).values
        cate = est.ate(X[mask])
        ci = est.ate_interval(X[mask])
        print(f'  {size} (n={mask.sum()}): CATE={cate:.4f}  95% CI ({ci[0]:.4f}, {ci[1]:.4f})')
        rows.append({'size_cat': size, 'n': int(mask.sum()), 'cate': cate, 'ci_low': ci[0], 'ci_high': ci[1]})

    pd.DataFrame(rows).to_csv('data/processed/table6b_cate_by_size.csv', index=False)
    print('\nSaved data/processed/table6b_cate_by_size.csv')


if __name__ == '__main__':
    main()
