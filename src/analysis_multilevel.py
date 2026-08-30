"""
Bayesian hierarchical (multilevel) logistic model: firms nested in
countries, with a random slope on access-to-finance and cross-level
interactions with the SBFN policy indicator and WGI regulatory quality.
This is the paper's primary specification for H2/H3 -- it lets country
be a random effect (so SBFN status, a level-2 constant, is identified
rather than absorbed) while properly modeling the correlated-error
structure that ~41 country clusters make unreliable for cluster-robust
OLS (Cameron & Miller, 2015).
"""
import arviz as az
import bambi as bmb
import pandas as pd

pd.set_option('display.width', 160)


def load():
    df = pd.read_parquet('data/processed/analysis_main.parquet')
    df['sbfn_member'] = pd.to_numeric(df['sbfn_member'], errors='coerce')
    keep = ['green_adoption_binary', 'fin_has_credit_line', 'sbfn_member',
            'wgi_regulatory_quality', 'log_sales', 'foreign_owned_dummy',
            'exporter_dummy', 'size_cat', 'sector_broad', 'country_survey_label']
    df = df.dropna(subset=keep)
    # z-standardize the continuous moderator to make coefficients comparable / aid sampling
    df['wgi_rq_z'] = (df['wgi_regulatory_quality'] - df['wgi_regulatory_quality'].mean()) / df['wgi_regulatory_quality'].std()
    return df


def main():
    df = load()
    print('N firms:', len(df), '| N countries:', df['country_survey_label'].nunique())

    formula = (
        "green_adoption_binary ~ fin_has_credit_line * sbfn_member "
        "+ fin_has_credit_line * wgi_rq_z "
        "+ log_sales + foreign_owned_dummy + exporter_dummy "
        "+ C(size_cat) + C(sector_broad) "
        "+ (1 + fin_has_credit_line | country_survey_label)"
    )

    model = bmb.Model(formula, df, family='bernoulli')
    idata = model.fit(draws=1000, tune=1000, chains=4, random_seed=42,
                       inference_method='nutpie')

    print(az.summary(idata, var_names=[
        'Intercept', 'fin_has_credit_line', 'sbfn_member',
        'fin_has_credit_line:sbfn_member', 'wgi_rq_z', 'fin_has_credit_line:wgi_rq_z'
    ]))

    idata.to_netcdf('data/processed/multilevel_idata.nc')
    print('Saved posterior to data/processed/multilevel_idata.nc')

    diag = az.summary(idata)
    max_rhat = diag['r_hat'].max()
    min_ess = diag['ess_bulk'].min()
    print(f'\nConvergence check: max r_hat={max_rhat:.3f} (want <1.01), min ess_bulk={min_ess:.0f} (want >400)')


if __name__ == '__main__':
    main()
