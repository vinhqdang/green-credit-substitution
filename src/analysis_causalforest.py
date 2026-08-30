"""
Heterogeneous treatment-effect estimation via CausalForestDML (Wager &
Athey, 2018; Chernozhukov et al., 2018), implemented in econml. The
"treatment" is firm access to a bank credit line/loan; the outcome is
green practice adoption; heterogeneity (effect-modifier) features are
the two institutional moderators (SBFN status, WGI regulatory quality)
plus firm size and export status, so the model can recover how the
finance -> green-adoption effect varies across the institutional
landscape without imposing a parametric interaction form.
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, GradientBoostingRegressor
from econml.dml import CausalForestDML

pd.set_option('display.width', 160)


def load():
    df = pd.read_parquet('data/processed/analysis_main.parquet')
    df['sbfn_member'] = pd.to_numeric(df['sbfn_member'], errors='coerce')
    keep = ['green_adoption_binary', 'fin_has_credit_line', 'sbfn_member',
            'wgi_regulatory_quality', 'log_sales', 'foreign_owned_dummy',
            'exporter_dummy', 'size_cat', 'sector_broad', 'country_survey_label']
    df = df.dropna(subset=keep).reset_index(drop=True)
    df = pd.get_dummies(df, columns=['size_cat', 'sector_broad'], drop_first=True)
    return df


def main():
    df = load()
    print('N firms:', len(df), '| N countries:', df['country_survey_label'].nunique())

    Y = df['green_adoption_binary'].values.astype(float)
    T = df['fin_has_credit_line'].values.astype(float)

    control_cols = [c for c in df.columns if c.startswith('size_cat_') or c.startswith('sector_broad_')] \
        + ['log_sales', 'foreign_owned_dummy', 'exporter_dummy']
    W = df[control_cols].astype(float).values

    het_cols = ['sbfn_member', 'wgi_regulatory_quality', 'log_sales', 'exporter_dummy']
    X = df[het_cols].astype(float).values

    est = CausalForestDML(
        model_y=GradientBoostingRegressor(n_estimators=200, max_depth=3, random_state=42),
        model_t=GradientBoostingClassifier(n_estimators=200, max_depth=3, random_state=42),
        discrete_treatment=True,
        n_estimators=2000,
        min_samples_leaf=20,
        max_depth=None,
        cv=5,
        random_state=42,
    )
    est.fit(Y, T, X=X, W=W)

    ate = est.ate(X)
    ate_interval = est.ate_interval(X)
    print(f'\nOverall ATE of bank credit access on green adoption: {ate:.4f}  95% CI {ate_interval}')

    # heterogeneity: effect by SBFN status
    for sbfn_val in [0, 1]:
        mask = df['sbfn_member'].values == sbfn_val
        if mask.sum() > 20:
            cate = est.ate(X[mask])
            ci = est.ate_interval(X[mask])
            print(f'CATE | sbfn_member={sbfn_val} (n={mask.sum()}): {cate:.4f}  95% CI {ci}')

    # heterogeneity: effect by regulatory-quality tercile
    rq = df['wgi_regulatory_quality'].values
    terciles = np.quantile(rq, [1/3, 2/3])
    labels = np.where(rq <= terciles[0], 'low', np.where(rq <= terciles[1], 'mid', 'high'))
    for lab in ['low', 'mid', 'high']:
        mask = labels == lab
        cate = est.ate(X[mask])
        ci = est.ate_interval(X[mask])
        print(f'CATE | regulatory quality tercile={lab} (n={mask.sum()}): {cate:.4f}  95% CI {ci}')

    # feature importance for heterogeneity
    print('\nFeature importances (which moderators explain effect heterogeneity):')
    try:
        importances = est.feature_importances_
        for name, imp in zip(het_cols, importances):
            print(f'  {name}: {imp:.4f}')
    except Exception as e:
        print('  (feature_importances_ unavailable):', e)

    import joblib
    joblib.dump({'est': est, 'X_cols': het_cols, 'W_cols': control_cols}, 'data/processed/causalforest_model.joblib')
    print('\nSaved model to data/processed/causalforest_model.joblib')


if __name__ == '__main__':
    main()
