import pandas as pd
pd.set_option('display.width', 160)
pd.set_option('display.max_rows', 60)

df = pd.read_parquet('data/processed/firm_analysis_eca_mena.parquet')

agg = df.groupby('country_survey_label').agg(
    n_firms=('firm_id', 'count'),
    green_adoption_rate=('green_adoption_binary', 'mean'),
    green_index_mean=('green_adoption_index', 'mean'),
    credit_line_rate=('fin_has_credit_line', 'mean'),
    fin_obstacle_mean=('fin_obstacle_access_to_finance', 'mean'),
).sort_values('green_adoption_rate')

print(agg)
print('\nOverall correlation (firm-level) green_index vs has_credit_line:',
      df[['green_adoption_index', 'fin_has_credit_line']].corr().iloc[0, 1])
print('Overall correlation (firm-level) green_index vs finance obstacle:',
      df[['green_adoption_index', 'fin_obstacle_access_to_finance']].corr().iloc[0, 1])

agg.to_csv('data/processed/country_level_descriptives.csv')
