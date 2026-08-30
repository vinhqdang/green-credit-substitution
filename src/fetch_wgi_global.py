"""
Fetch WGI Regulatory Quality and Government Effectiveness for every
country-year in the 162-country global sample via the World Bank
DataBank API (mechanical, no research needed).
"""
import time
import pandas as pd
import requests

df = pd.read_csv('data/global_country_iso_mapping.csv')

BASE = 'https://api.worldbank.org/v2/country/{iso3}/indicator/{ind}?date={y1}:{y2}&format=json&per_page=100'
INDICATORS = {'wgi_regulatory_quality': 'GOV_WGI_RQ_EST', 'wgi_government_effectiveness': 'GOV_WGI_GE_EST'}

results = []
for _, row in df.iterrows():
    iso3, year = row['iso3'], int(row['survey_year'])
    rec = {'country_survey_label': row['country_survey_label'], 'iso3': iso3, 'survey_year': year}
    for col, ind in INDICATORS.items():
        try:
            # WGI publishes with a lag; request a window ending at the survey
            # year and take the latest available observation within it
            url = BASE.format(iso3=iso3, ind=ind, y1=year - 4, y2=year)
            resp = requests.get(url, timeout=15)
            data = resp.json()
            val, used_year = None, None
            if isinstance(data, list) and len(data) > 1 and data[1]:
                for obs in data[1]:
                    if obs.get('value') is not None:
                        val = obs['value']
                        used_year = obs.get('date')
                        break
            rec[col] = val
            rec[f'{col}_year_used'] = used_year
        except Exception as e:
            rec[col] = None
            rec[f'{col}_error'] = str(e)
        time.sleep(0.05)
    results.append(rec)
    print(f"{row['country_survey_label']}: RQ={rec.get('wgi_regulatory_quality')} (yr {rec.get('wgi_regulatory_quality_year_used')}), "
          f"GE={rec.get('wgi_government_effectiveness')} (yr {rec.get('wgi_government_effectiveness_year_used')})")

out = pd.DataFrame(results)
out.to_csv('data/global_wgi.csv', index=False)
missing = out[out['wgi_regulatory_quality'].isna()]
print(f"\nTotal: {len(out)}, missing RQ: {len(missing)}")
print(missing[['country_survey_label', 'iso3', 'survey_year']])
