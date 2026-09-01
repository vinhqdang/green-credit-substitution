"""Benjamini-Hochberg FDR correction across every credit x institutional-moderator
interaction coefficient reported under a frequentist estimator in the paper
(Tables 4, 8, 9). Bayesian (Table 5) and causal-forest (Table 6) estimates are
excluded: they report credible/confidence intervals rather than p-values and are
not part of a classical multiple-testing family.

Where the manuscript text reports an exact p-value we use it; where only the
coefficient and standard error are reported (Table 4 model M3's fully-saturated
triple interaction), we recover an approximate two-sided p-value from a normal
approximation to the logit z-statistic (z = coef / se), which is standard for a
sample of this size (N = 23,914) and is flagged as such in the output.

Run from the repository root: python3 src/compute_fdr_interactions.py
"""
import csv
import math

def normal_p_two_sided(z):
    return 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))

# (table, specification, term, p_value, exact_or_approx)
tests = [
    ("Table 4", "M2 (SBFN)", "Credit x SBFN", 0.773, "exact"),
    ("Table 4", "M3 (triple interaction)", "Credit x SBFN",
     normal_p_two_sided(0.019 / 0.140), "approx (z=coef/se)"),
    ("Table 4", "M3 (triple interaction)", "Credit x RegQuality",
     normal_p_two_sided(0.144 / 0.142), "approx (z=coef/se)"),
    ("Table 4", "M3 (triple interaction)", "Credit x SBFN x RegQuality",
     normal_p_two_sided(-0.104 / 0.272), "approx (z=coef/se)"),
    ("Table 8", "(a) Continuous index, OLS", "Credit x SBFN", 0.739, "exact"),
    ("Table 8", "(b1) Overdraft", "Overdraft x SBFN", 0.031, "exact"),
    ("Table 8", "(b2) Finance obstacle (reverse-coded)", "Obstacle x SBFN", 0.849, "exact"),
    ("Table 8", "(c1) Manufacturing subsample", "Credit x SBFN", 0.826, "exact"),
    ("Table 8", "(c2) Services subsample", "Credit x SBFN", 0.426, "exact"),
    ("Table 9", "M1 (no country FE)", "Credit x SBFN", 0.430, "exact"),
    ("Table 9", "M1 (no country FE)", "Credit x RegQuality",
     normal_p_two_sided(0.092 / 0.089), "approx (z=coef/se)"),
    ("Table 9", "M2 (country FE)", "Credit x SBFN", 0.205, "exact"),
    ("Table 9", "M2 (country FE)", "Credit x RegQuality", 0.346, "exact"),
]

m = len(tests)
order = sorted(range(m), key=lambda i: tests[i][3])
raw_sorted = [tests[i][3] for i in order]

adj_sorted = [None] * m
adj_sorted[-1] = min(raw_sorted[-1] * m / m, 1.0)
for i in range(m - 2, -1, -1):
    adj_sorted[i] = min(adj_sorted[i + 1], raw_sorted[i] * m / (i + 1))

adjusted = [None] * m
for rank, i in enumerate(order):
    adjusted[i] = adj_sorted[rank]

out_rows = []
for i, (table, spec, term, p, kind) in enumerate(tests):
    out_rows.append({
        "table": table, "specification": spec, "term": term,
        "raw_p": round(p, 4), "p_type": kind, "bh_adjusted_p": round(adjusted[i], 4),
    })

out_rows_sorted = sorted(out_rows, key=lambda r: r["raw_p"])

with open("data/processed/table10_multiple_testing_correction.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["table", "specification", "term", "raw_p", "p_type", "bh_adjusted_p"])
    w.writeheader()
    w.writerows(out_rows_sorted)

print(f"m = {m} credit x institutional-moderator interaction tests (Tables 4, 8, 9)")
print(f"{'table':<9}{'specification':<28}{'term':<28}{'raw_p':>8}{'bh_adj_p':>10}  type")
for r in out_rows_sorted:
    print(f"{r['table']:<9}{r['specification']:<28}{r['term']:<28}{r['raw_p']:>8.3f}{r['bh_adjusted_p']:>10.3f}  {r['p_type']}")

min_raw = out_rows_sorted[0]
print(f"\nSmallest raw p-value: {min_raw['table']} {min_raw['specification']} / {min_raw['term']}, "
      f"raw p = {min_raw['raw_p']:.3f}, BH-adjusted p = {min_raw['bh_adjusted_p']:.3f}")
n_below_05 = sum(1 for r in out_rows_sorted if r["bh_adjusted_p"] < 0.05)
n_below_10 = sum(1 for r in out_rows_sorted if r["bh_adjusted_p"] < 0.10)
print(f"Tests with BH-adjusted p < 0.05: {n_below_05}; < 0.10: {n_below_10}")
