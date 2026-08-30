"""
Format the baseline logit results (data/processed/baseline_results.pkl) into
a clean regression table (Table 4), one column per specification, with
stars for significance and coefficients/SEs stacked.
"""
import pickle  # trusted, locally-generated file (written by analysis_baseline.py in this repo) -- not untrusted input
import numpy as np
import pandas as pd

pd.set_option('display.width', 200)


def stars(p):
    if p < 0.01:
        return '***'
    if p < 0.05:
        return '**'
    if p < 0.10:
        return '*'
    return ''


def format_model(res, varnames):
    rows = {}
    for v in varnames:
        if v in res.params.index:
            b = res.params[v]
            se = res.bse[v]
            p = res.pvalues[v]
            rows[v] = f"{b:.3f}{stars(p)}\n({se:.3f})"
        else:
            rows[v] = ''
    rows['N'] = f"{int(res.nobs)}"
    rows['Pseudo R2'] = f"{res.prsquared:.3f}"
    return rows


def main():
    with open('data/processed/baseline_results.pkl', 'rb') as f:
        results = pickle.load(f)

    varnames = [
        'fin_has_credit_line', 'sbfn_member', 'fin_has_credit_line:sbfn_member',
        'wgi_regulatory_quality', 'fin_has_credit_line:wgi_regulatory_quality',
        'sbfn_member:wgi_regulatory_quality',
        'fin_has_credit_line:sbfn_member:wgi_regulatory_quality',
        'log_sales', 'foreign_owned_dummy', 'exporter_dummy',
    ]

    table = pd.DataFrame({name: format_model(res, varnames) for name, res in results.items()})
    print(table)
    table.to_csv('data/processed/table4_baseline_regressions.csv')
    print('\nSaved data/processed/table4_baseline_regressions.csv')


if __name__ == '__main__':
    main()
