"""
Determine SBFN membership status as of the survey year for all 162
global-sample country-years, using the SBFN data portal's full member
roster (data/sbfn_roster.csv, fetched 2026-08-30 from
data.sbfnetwork.org/country-profiles) plus a join_year <= survey_year
rule. Where a country-year already has a deeply-sourced determination
from the original 47-country research pass (data/macro_moderators.csv),
that prior determination is kept in preference to the roster-only rule.
"""
import pandas as pd

mapping = pd.read_csv('data/global_country_iso_mapping.csv')
roster = pd.read_csv('data/sbfn_roster.csv')
old_macro = pd.read_csv('data/macro_moderators.csv')

roster_dict = {}
for _, r in roster.iterrows():
    roster_dict[r['member_name']] = int(r['join_year'])

rows = []
for _, row in mapping.iterrows():
    label = row['country_survey_label']
    name = row['country_name']
    year = int(row['survey_year'])

    old_row = old_macro[old_macro['country_survey_label'] == label]
    if len(old_row) == 1:
        o = old_row.iloc[0]
        rows.append({
            'country_survey_label': label, 'iso3': row['iso3'], 'survey_year': year,
            'sbfn_member': o['sbfn_member'], 'sbfn_join_year': o['sbfn_join_year'],
            'source': 'prior deep-research pass (macro_moderators.csv)',
        })
        continue

    join_year = roster_dict.get(name)
    if join_year is not None:
        member = 1 if join_year <= year else 0
        rows.append({
            'country_survey_label': label, 'iso3': row['iso3'], 'survey_year': year,
            'sbfn_member': member, 'sbfn_join_year': join_year if member else None,
            'source': 'SBFN data portal roster (data.sbfnetwork.org/country-profiles, fetched 2026-08-30)'
                      + (' -- ex-ante non-adopter: joined after survey year' if not member else ''),
        })
    else:
        rows.append({
            'country_survey_label': label, 'iso3': row['iso3'], 'survey_year': year,
            'sbfn_member': 0, 'sbfn_join_year': None,
            'source': 'Absent from SBFN data portal roster (67 members, fetched 2026-08-30) -- coded non-member',
        })

out = pd.DataFrame(rows)
out.to_csv('data/global_sbfn.csv', index=False)
print("Saved data/global_sbfn.csv")
print(f"\nTotal: {len(out)}")
print(f"SBFN member=1: {(out['sbfn_member']==1).sum()}")
print(f"SBFN member=0: {(out['sbfn_member']==0).sum()}")
print(f"\nFrom prior deep-research pass: {(out['source'].str.contains('prior')).sum()}")
print(f"From roster: {(out['source'].str.contains('roster')).sum()}")
