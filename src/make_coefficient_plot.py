"""
Figure 4: coefficient forest plot spanning every specification in the
paper -- the single consolidated visual answer to "where are the
results," replacing the reader's need to hunt coefficients out of
prose across five subsections.
"""
import matplotlib.pyplot as plt
import numpy as np

# (label, coef, se, dof for a rough 95% CI via 1.96*se)
CREDIT = [
    ('Primary: baseline logit (M1)', 0.571, 0.123),
    ('Primary: Bayesian hierarchical', 0.330, 0.097),
    ('Global: no country FE (M1)', 0.198, 0.096),
    ('Global: country FE (M2)', 0.249, 0.057),
]
SBFN_INTERACTION = [
    ('Primary: baseline logit (M2)', 0.049, 0.168),
    ('Primary: Bayesian hierarchical', 0.072, 0.211),
    ('Global: no country FE (M1)', 0.278, 0.352),
    ('Global: country FE (M2)', 0.506, 0.399),
]
WGI_INTERACTION = [
    ('Primary: baseline logit (M3)', 0.144, 0.142),
    ('Primary: Bayesian hierarchical', 0.004, 0.087),
    ('Global: no country FE (M1)', 0.092, 0.089),
    ('Global: country FE (M2)', -0.044, 0.047),
]

PANELS = [
    ('A. Credit access\n(H1: main effect)', CREDIT, '#08306b'),
    ('B. Credit × SBFN member\n(H2: policy interaction)', SBFN_INTERACTION, '#c0392b'),
    ('C. Credit × Regulatory quality\n(H3: institutional interaction)', WGI_INTERACTION, '#c0392b'),
]

fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=False)

for ax, (title, data, color) in zip(axes, PANELS):
    labels = [d[0] for d in data][::-1]
    coefs = np.array([d[1] for d in data])[::-1]
    ses = np.array([d[2] for d in data])[::-1]
    ci = 1.96 * ses
    y = np.arange(len(labels))
    ax.errorbar(coefs, y, xerr=ci, fmt='o', color=color, ecolor=color, capsize=4, markersize=7)
    ax.axvline(0, color='grey', linestyle='--', linewidth=1)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_title(title, fontsize=10)
    ax.set_xlabel('Logit coefficient (95% CI)', fontsize=9)
    ax.spines[['top', 'right']].set_visible(False)

fig.suptitle('Figure 4. Coefficient estimates across every specification and both samples\n'
             '(Panel A: robust and significant everywhere; Panels B-C: null everywhere)', fontsize=11)
plt.tight_layout(rect=[0, 0, 1, 0.90])

import os
os.makedirs('output/figures', exist_ok=True)
plt.savefig('output/figures/fig4_coefficient_plot.png', dpi=250, bbox_inches='tight')
print('Saved output/figures/fig4_coefficient_plot.png')
