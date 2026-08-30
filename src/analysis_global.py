"""
Global-sample analysis (162 countries, co2_monitor outcome). With this
many clusters, country fixed effects become feasible and give a cleaner
test than the 41-country primary sample's clustered-SE-only approach:
country FE absorbs the SBFN main effect (collinear, as before) but NOT
its interaction with credit access, since credit varies within country.
We report both a no-country-FE specification (parallel to the primary
sample's Table 4, for comparability) and a country-FE specification
(the sharper test this larger sample newly affords).
"""
import pandas as pd
import statsmodels.formula.api as smf

pd.set_option('display.width', 160)


def load():
    df = pd.read_parquet('data/processed/analysis_global.parquet')
    df['sbfn_member'] = pd.to_numeric(df['sbfn_member'], errors='coerce')
    keep = ['co2_monitor', 'fin_has_credit_line', 'sbfn_member', 'wgi_regulatory_quality',
            'sector_broad', 'log_sales', 'foreign_owned_dummy', 'exporter_dummy',
            'country_survey_label']
    df = df.dropna(subset=keep).reset_index(drop=True)
    df['sector_broad'] = df['sector_broad'].astype('category')
    df['wgi_rq_z'] = (df['wgi_regulatory_quality'] - df['wgi_regulatory_quality'].mean()) / df['wgi_regulatory_quality'].std()
    return df


def main():
    df = load()
    print('N firms:', len(df), '| N countries:', df['country_survey_label'].nunique())
    print('SBFN member countries:', df.groupby('country_survey_label')['sbfn_member'].first().sum())

    controls = "log_sales + foreign_owned_dummy + exporter_dummy + C(sector_broad)"

    print('\n=== M1: No country FE (parallel to primary-sample Table 4) ===')
    f1 = f"co2_monitor ~ fin_has_credit_line * sbfn_member * wgi_rq_z + {controls}"
    r1 = smf.logit(f1, data=df).fit(disp=0, cov_type='cluster', cov_kwds={'groups': df['country_survey_label']})
    print(r1.summary())

    print('\n=== M2: Country fixed effects (main effects of sbfn_member/wgi_rq_z dropped -- '
          'collinear with FE by construction; only their firm-level interactions with credit '
          'access remain identified) ===')
    f2 = (f"co2_monitor ~ fin_has_credit_line + fin_has_credit_line:sbfn_member "
          f"+ fin_has_credit_line:wgi_rq_z + {controls} + C(country_survey_label)")
    r2 = smf.logit(f2, data=df).fit(disp=0, cov_type='cluster', cov_kwds={'groups': df['country_survey_label']}, maxiter=200)
    # only print the non-country-FE coefficients for readability
    focal = [p for p in r2.params.index if 'country_survey_label' not in p]
    with pd.option_context('display.max_columns', None, 'display.width', 200):
        print(r2.summary2().tables[1].loc[focal])

    import pickle  # trusted, locally-generated file for this repo's own pipeline
    with open('data/processed/global_results.pkl', 'wb') as f:
        pickle.dump({'M1_no_fe': r1, 'M2_country_fe_focal': r2.summary2().tables[1].loc[focal]}, f)
    print('\nSaved data/processed/global_results.pkl')


if __name__ == '__main__':
    main()
