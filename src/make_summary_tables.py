"""
Table 1 (sample composition, one row per country-year, in the style of
reference Paper 1's Table 1) and Table 2 (summary statistics of all
analysis variables). Requires data/processed/analysis_main.parquet
(produced after the macro merge).
"""
import pandas as pd

pd.set_option('display.width', 200)
pd.set_option('display.max_rows', 60)


def table1_country_composition():
    df = pd.read_parquet('data/processed/analysis_main.parquet')
    df['sbfn_member'] = pd.to_numeric(df['sbfn_member'], errors='coerce')

    t = df.groupby('country_survey_label').agg(
        n_firms=('firm_id', 'count'),
        survey_year=('survey_year', 'first'),
        sbfn_member=('sbfn_member', 'first'),
        wgi_regulatory_quality=('wgi_regulatory_quality', 'first'),
        green_adoption_rate=('green_adoption_binary', 'mean'),
        credit_line_rate=('fin_has_credit_line', 'mean'),
    ).sort_values('country_survey_label')

    t.to_csv('data/processed/table1_country_composition.csv')
    print(t)
    print('\nTotal firms:', t['n_firms'].sum(), '| Total countries:', len(t))
    return t


def table2_summary_stats():
    df = pd.read_parquet('data/processed/analysis_main.parquet')
    df['sbfn_member'] = pd.to_numeric(df['sbfn_member'], errors='coerce')

    varlist = [
        'green_adoption_binary', 'green_adoption_index', 'fin_has_credit_line',
        'fin_has_overdraft', 'fin_obstacle_access_to_finance', 'sbfn_member',
        'wgi_regulatory_quality', 'wgi_government_effectiveness', 'log_sales',
        'foreign_owned_dummy', 'exporter_dummy',
    ]
    stats = df[varlist].describe().T
    stats['n_obs'] = df[varlist].notna().sum()
    stats.to_csv('data/processed/table2_summary_stats.csv')
    print(stats)
    return stats


if __name__ == '__main__':
    table1_country_composition()
    print('\n' + '=' * 100 + '\n')
    table2_summary_stats()
