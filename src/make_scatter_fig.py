"""
Figure 2: country-level scatter of green adoption rate against regulatory
quality, split by SBFN status, with separate fitted lines -- the visual
complement to the "main effects, no interaction" finding: if the two
fitted lines are close to parallel, that IS the null-interaction result,
shown rather than only tabulated.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df = pd.read_parquet('data/processed/analysis_main.parquet')
df['sbfn_member'] = pd.to_numeric(df['sbfn_member'], errors='coerce')

agg = df.groupby('country_survey_label').agg(
    green_rate=('green_adoption_binary', 'mean'),
    credit_rate=('fin_has_credit_line', 'mean'),
    reg_quality=('wgi_regulatory_quality', 'first'),
    sbfn=('sbfn_member', 'first'),
    n=('firm_id', 'count'),
).dropna()

fig, ax = plt.subplots(figsize=(9, 6.5))

for sbfn_val, color, label in [(0, '#6baed6', 'Non-SBFN-member economies'), (1, '#08306b', 'SBFN policy-member economies')]:
    sub = agg[agg['sbfn'] == sbfn_val]
    ax.scatter(sub['reg_quality'], sub['green_rate'], s=sub['n'] / 10, color=color, alpha=0.75,
               label=label, edgecolor='white', linewidth=0.5)
    if len(sub) >= 3:
        z = np.polyfit(sub['reg_quality'], sub['green_rate'], 1)
        xs = np.linspace(sub['reg_quality'].min(), sub['reg_quality'].max(), 50)
        ax.plot(xs, np.polyval(z, xs), color=color, linestyle='--', linewidth=2)

ax.set_xlabel('WGI Regulatory Quality (survey year)', fontsize=11)
ax.set_ylabel('Country-level green practice adoption rate', fontsize=11)
ax.set_title('Figure 2. Green adoption vs. regulatory quality, by SBFN status\n'
              'Near-parallel slopes = no credit x institution interaction; the level gap = SBFN\'s negative main effect',
              fontsize=11)
ax.legend(fontsize=9, frameon=False, loc='upper left')
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()

import os
os.makedirs('output/figures', exist_ok=True)
plt.savefig('output/figures/fig2_scatter_regquality.png', dpi=250, bbox_inches='tight')
print('Saved output/figures/fig2_scatter_regquality.png')
print(agg.sort_values('reg_quality'))
