"""
Figure 5: causal forest CATEs, visualized -- turns Table 6/6b's numbers
(currently only narrated in prose) into a single glance-able chart.
"""
import matplotlib.pyplot as plt
import numpy as np

GROUPS = [
    ('Overall ATE', 0.0733, -0.0396, 0.1862, '#333333'),
    ('', None, None, None, None),
    ('SBFN: non-member', 0.0723, -0.0300, 0.1746, '#6baed6'),
    ('SBFN: member', 0.0758, -0.0591, 0.2107, '#08306b'),
    ('', None, None, None, None),
    ('Reg. quality: low tercile', 0.0753, -0.0568, 0.2075, '#fdae6b'),
    ('Reg. quality: mid tercile', 0.0697, -0.0355, 0.1749, '#e6550d'),
    ('Reg. quality: high tercile', 0.0749, -0.0203, 0.1701, '#a63603'),
    ('', None, None, None, None),
    ('Firm size: small', 0.0797, -0.0409, 0.2004, '#c7e9c0'),
    ('Firm size: medium', 0.0747, -0.0344, 0.1838, '#74c476'),
    ('Firm size: large', 0.0569, -0.0428, 0.1565, '#238b45'),
]

fig, ax = plt.subplots(figsize=(8, 7))
y = np.arange(len(GROUPS))[::-1]

for yi, (label, cate, lo, hi, color) in zip(y, GROUPS):
    if cate is None:
        continue
    err = np.array([[cate - lo], [hi - cate]])
    ax.errorbar(cate, yi, xerr=err, fmt='o', color=color, ecolor=color, capsize=4, markersize=8)

ax.axvline(0, color='grey', linestyle='--', linewidth=1)
labels = [g[0] for g in GROUPS]
ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=10)
ax.set_xlabel('Causal forest CATE on green/CO2-monitoring adoption (95% CI)', fontsize=10)
ax.set_title('Figure 5. Causal forest conditional average treatment effects\n'
             '(all subgroup CIs overlap the overall ATE and each other -- no institutional or size heterogeneity)',
             fontsize=11)
ax.spines[['top', 'right']].set_visible(False)
plt.tight_layout()

import os
os.makedirs('output/figures', exist_ok=True)
plt.savefig('output/figures/fig5_cate_plot.png', dpi=250, bbox_inches='tight')
print('Saved output/figures/fig5_cate_plot.png')
