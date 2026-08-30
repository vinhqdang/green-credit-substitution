"""
Figure 3: world map of the full combined sample -- the 41-country
primary (rich-module) sample plus the 162-country global (minimal-
indicator) extension, shaded by SBFN status, showing the near-total
global reach of the combined dataset.
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd

primary = pd.read_parquet('data/processed/analysis_main.parquet')
primary['sbfn_member'] = pd.to_numeric(primary['sbfn_member'], errors='coerce')
primary_agg = primary.groupby(['country_survey_label', 'iso3'])['sbfn_member'].first().reset_index()
primary_agg['sample'] = 'primary'

glob = pd.read_parquet('data/processed/analysis_global.parquet')
glob['sbfn_member'] = pd.to_numeric(glob['sbfn_member'], errors='coerce')
glob_iso = pd.read_csv('data/global_country_iso_mapping.csv')[['country_survey_label', 'iso3']]
glob_agg = glob.groupby('country_survey_label')['sbfn_member'].first().reset_index()
glob_agg = glob_agg.merge(glob_iso, on='country_survey_label', how='left')
glob_agg['sample'] = 'global'

combined = pd.concat([primary_agg[['iso3', 'sbfn_member', 'sample']],
                       glob_agg[['iso3', 'sbfn_member', 'sample']]], ignore_index=True)
# dedupe by iso3, preferring primary sample's richer data where both exist
combined = combined.sort_values('sample').drop_duplicates(subset='iso3', keep='first')

world = gpd.read_file('data/geo/ne_110m_admin_0_countries')
world = world.merge(combined, left_on='ISO_A3', right_on='iso3', how='left')

fig, ax = plt.subplots(figsize=(14, 7.5))
world.plot(ax=ax, color='#e8e8e8', edgecolor='white', linewidth=0.3)
world[world['sbfn_member'] == 0.0].plot(ax=ax, color='#6baed6', edgecolor='white', linewidth=0.3)
world[world['sbfn_member'] == 1.0].plot(ax=ax, color='#08306b', edgecolor='white', linewidth=0.3)
ax.legend(handles=[
    mpatches.Patch(color='#08306b', label='SBFN policy member (as of survey year)'),
    mpatches.Patch(color='#6baed6', label='In sample, not an SBFN member'),
    mpatches.Patch(color='#e8e8e8', label='Not in sample'),
], loc='lower left', fontsize=9, frameon=False)
ax.set_title(f'Figure 3. Combined sample coverage: {combined["iso3"].nunique()} economies '
             f'(41 primary rich-module + 162 global minimal-indicator, net of overlap)', fontsize=11)
ax.axis('off')
plt.tight_layout()

import os
os.makedirs('output/figures', exist_ok=True)
plt.savefig('output/figures/fig3_global_map.png', dpi=250, bbox_inches='tight')
print('Saved output/figures/fig3_global_map.png')
print('Unique economies in combined map:', combined['iso3'].nunique())
