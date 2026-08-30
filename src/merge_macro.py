"""
Merge firm-level analysis samples with country-level macro moderators
(SBFN status, WGI governance indicators) produced by the research agent
at data/macro_moderators.csv, plus the ISO3 mapping table.

Output:
  data/processed/analysis_main.parquet      (41-country ECA-MENA sample + macro)
  data/processed/analysis_extension.parquet (6-country supplementary sample + macro)
"""
import numpy as np
import pandas as pd

macro = pd.read_csv('data/macro_moderators.csv')


def attach_macro(firm_path, out_path):
    firm = pd.read_parquet(firm_path)
    macro_cols = macro.drop(columns=['survey_year', 'country_name'], errors='ignore')
    merged = firm.merge(macro_cols, on='country_survey_label', how='left', validate='many_to_one')
    n_unmatched = merged['sbfn_member'].isna().sum() if 'sbfn_member' in merged.columns else None
    print(f"{firm_path}: {firm.shape} -> merged {merged.shape}, unmatched rows for sbfn_member = {n_unmatched}")
    merged.to_parquet(out_path)
    return merged


if __name__ == '__main__':
    attach_macro('data/processed/firm_analysis_eca_mena.parquet', 'data/processed/analysis_main.parquet')
    attach_macro('data/processed/firm_analysis_extension.parquet', 'data/processed/analysis_extension.parquet')
