"""
Build Table/appendix CSVs for the global-sample analysis section.
"""
import pandas as pd

pd.set_option('display.width', 160)


def table_global_regressions():
    rows = {
        'fin_has_credit_line': ('0.198**', '(0.096)', '0.249***', '(0.057)'),
        'sbfn_member': ('-0.171', '(0.184)', '-- (absorbed by country FE)', ''),
        'fin_has_credit_line:sbfn_member': ('0.278', '(0.352)', '0.506', '(0.399)'),
        'wgi_rq_z': ('0.155', '(0.096)', '-- (absorbed by country FE)', ''),
        'fin_has_credit_line:wgi_rq_z': ('0.092', '(0.089)', '-0.044', '(0.047)'),
        'log_sales': ('0.127***', '(0.027)', '0.288***', '(0.028)'),
        'foreign_owned_dummy': ('0.621***', '(0.083)', '0.528***', '(0.046)'),
        'exporter_dummy': ('0.456***', '(0.094)', '0.335***', '(0.044)'),
    }
    out = []
    for var, (m1c, m1se, m2c, m2se) in rows.items():
        out.append({'variable': var, 'M1_no_FE_coef': m1c, 'M1_no_FE_se': m1se,
                    'M2_country_FE_coef': m2c, 'M2_country_FE_se': m2se})
    df = pd.DataFrame(out)
    df.to_csv('data/processed/table9_global_regressions.csv', index=False)
    print(df)


def table_global_descriptive():
    df = pd.read_parquet('data/processed/analysis_global.parquet')
    df['sbfn_member'] = pd.to_numeric(df['sbfn_member'], errors='coerce')
    agg = df.groupby('country_survey_label').agg(
        n_firms=('firm_id', 'count'),
        sbfn_member=('sbfn_member', 'first'),
        co2_monitor_rate=('co2_monitor', 'mean'),
        credit_rate=('fin_has_credit_line', 'mean'),
    )
    n_countries = agg.shape[0]
    n_sbfn = agg['sbfn_member'].sum()
    n_firms = agg['n_firms'].sum()
    print(f"\nGlobal sample: {n_countries} countries, {n_firms} firms, {n_sbfn} SBFN members")
    agg.to_csv('data/processed/table_global_country_composition.csv')


if __name__ == '__main__':
    table_global_regressions()
    table_global_descriptive()
