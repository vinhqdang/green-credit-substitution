"""
Callaway & Sant'Anna (2021) staggered-adoption event study of SBFN
membership on country-level macro environmental outcomes (renewable-energy
share, CO2 emissions per capita), with and without a log-GDP-per-capita
control, plus a naive two-way-fixed-effects comparison illustrating the
staggered-timing bias the CS estimator avoids, and a not-yet-treated
comparison-group robustness check for the doubly-robust specification.
Produces Table 11 (summary) and Figure 6 (event-study plot, GDP-controlled,
never-treated specification).

Requires: pandas, numpy, requests, statsmodels, matplotlib, differences==0.3.0
(a separate virtual environment is recommended -- these pin newer pandas/numpy
than the rest of this repo's scripts may assume).
"""
import csv

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from differences import ATTgt

treat = pd.read_csv("data/macro_country_treatment_panel.csv")
wdi = pd.read_csv("data/macro_wdi_panel_raw.csv")
gdp = pd.read_csv("data/macro_wdi_gdppc.csv")

df = wdi.merge(gdp, on=["iso3", "year"], how="left")
df = df.merge(treat[["iso3", "join_year", "ever_treated", "income_level"]], on="iso3", how="inner")
df = df[df["year"].between(2000, 2024)]
df = df[df["income_level"] != "Not classified"]
df["log_gdppc"] = np.log(df["gdppc"])

print(f"Panel: {df['iso3'].nunique()} countries x {df['year'].nunique()} years = {len(df)} rows")


def run_cs(outcome, formula, est_method, tag, control_group="never_treated"):
    sub = df.dropna(subset=[c for c in [outcome] + (["log_gdppc"] if "log_gdppc" in formula else []) if c]).copy()
    sub["cohort"] = sub["join_year"]  # NaN = never treated (required convention)
    sub = sub.set_index(["iso3", "year"])
    att_gt = ATTgt(data=sub, cohort_column="cohort")
    att_gt.fit(formula=formula, control_group=control_group, est_method=est_method,
               boot_iterations=999, random_state=42, progress_bar=False)
    simple = att_gt.aggregate("simple")
    event = att_gt.aggregate("event")
    simple.to_csv(f"data/processed/macro_did_simple_att_{tag}.csv")
    event.to_csv(f"data/processed/macro_did_event_study_byperiod_{tag}.csv")
    print(f"{tag}: n_countries={sub.reset_index()['iso3'].nunique()}")
    return simple, event


run_cs("renew_pct", "renew_pct", "reg", "renew_pct")
run_cs("co2_pc", "co2_pc", "reg", "co2_pc")
run_cs("co2_pc", "co2_pc ~ log_gdppc", "dr", "co2_pc_gdpctrl")
run_cs("renew_pct", "renew_pct ~ log_gdppc", "dr", "renew_pct_gdpctrl")
# Robustness: not-yet-treated comparison group (vs. the never-treated default
# above), doubly-robust specification only -- addresses the completeness gap
# flagged in the third review pass (output/review_cfp_fit_2026-09_v3.md, B2).
run_cs("co2_pc", "co2_pc ~ log_gdppc", "dr", "co2_pc_gdpctrl_notyet", control_group="not_yet_treated")
run_cs("renew_pct", "renew_pct ~ log_gdppc", "dr", "renew_pct_gdpctrl_notyet", control_group="not_yet_treated")

# --- Naive TWFE comparison (known to be biased under staggered adoption when
#     already-treated units serve as controls for later-treated ones) ---
for outcome in ["renew_pct", "co2_pc"]:
    sub = df.dropna(subset=[outcome]).copy()
    sub["post"] = ((sub["ever_treated"]) & (sub["year"] >= sub["join_year"])).astype(int)
    model = smf.ols(f"{outcome} ~ post + C(iso3) + C(year)", data=sub).fit(
        cov_type="cluster", cov_kwds={"groups": sub["iso3"]}
    )
    coef, se, p = model.params["post"], model.bse["post"], model.pvalues["post"]
    print(f"{outcome} naive TWFE: coef={coef:.4f} se={se:.4f} p={p:.4f} N={int(model.nobs)}")
    with open(f"data/processed/macro_did_naive_twfe_{outcome}.txt", "w") as f:
        f.write(f"coef={coef:.6f}\nse={se:.6f}\np={p:.6f}\nN={int(model.nobs)}\n")

# --- Table 11: consolidated summary ---
def read_simple_att(path):
    with open(path) as f:
        rows_ = list(csv.reader(f))
    d = dict(zip(rows_[2], rows_[3]))
    return float(d["ATT"]), float(d["std_error"]), float(d["lower"]), float(d["upper"]), d["zero_not_in_cband"].strip() == "*"


summary = []
for outcome, label in [("renew_pct", "Renewable energy % (WDI EG.FEC.RNEW.ZS)"),
                        ("co2_pc", "CO2 emissions per capita (WDI EN.GHG.CO2.PC.CE.AR5)")]:
    att, se, lo, hi, sig = read_simple_att(f"data/processed/macro_did_simple_att_{outcome}.csv")
    summary.append({"outcome": label, "specification": "Callaway-Sant'Anna, no covariates",
                     "att": att, "se": se, "ci_low": lo, "ci_high": hi, "sig_5pct": sig})
    att, se, lo, hi, sig = read_simple_att(f"data/processed/macro_did_simple_att_{outcome}_gdpctrl.csv")
    summary.append({"outcome": label, "specification": "Callaway-Sant'Anna, doubly-robust, log GDP p.c. control (never-treated)",
                     "att": att, "se": se, "ci_low": lo, "ci_high": hi, "sig_5pct": sig})
    att, se, lo, hi, sig = read_simple_att(f"data/processed/macro_did_simple_att_{outcome}_gdpctrl_notyet.csv")
    summary.append({"outcome": label, "specification": "Callaway-Sant'Anna, doubly-robust, log GDP p.c. control (not-yet-treated)",
                     "att": att, "se": se, "ci_low": lo, "ci_high": hi, "sig_5pct": sig})
    with open(f"data/processed/macro_did_naive_twfe_{outcome}.txt") as f:
        d = dict(line.strip().split("=") for line in f if line.strip())
    coef, se_, p_ = float(d["coef"]), float(d["se"]), float(d["p"])
    summary.append({"outcome": label, "specification": "Naive TWFE (post dummy, country+year FE)",
                     "att": coef, "se": se_, "ci_low": coef - 1.96 * se_, "ci_high": coef + 1.96 * se_,
                     "sig_5pct": p_ < 0.05})

out = pd.DataFrame(summary)
out.to_csv("data/processed/table11_macro_did_summary.csv", index=False)
print(out.to_string(index=False))


# --- Figure 6: event-study plot (GDP-controlled specification) ---
def load_event(path):
    edf = pd.read_csv(path, header=None, skiprows=4)
    edf.columns = ["k", "att", "se", "lo", "hi", "sig"]
    edf["k"] = edf["k"].astype(int)
    return edf.sort_values("k")


fig, axes = plt.subplots(1, 2, figsize=(11, 4.2), sharex=True)
specs = [
    ("renew_pct_gdpctrl", "Renewable energy consumption (% of final energy)", axes[0]),
    ("co2_pc_gdpctrl", "CO2 emissions per capita", axes[1]),
]
for key, title, ax in specs:
    edf = load_event(f"data/processed/macro_did_event_study_byperiod_{key}.csv")
    edf = edf[edf["k"].between(-12, 9)]
    ax.axhline(0, color="#888888", lw=0.8, zorder=1)
    ax.axvline(-0.5, color="#888888", lw=0.8, ls="--", zorder=1)
    ax.fill_between(edf["k"], edf["lo"], edf["hi"], color="#4C72B0", alpha=0.25, zorder=2)
    ax.plot(edf["k"], edf["att"], color="#4C72B0", marker="o", ms=3, lw=1.2, zorder=3)
    ax.set_title(title, fontsize=10)
    ax.set_xlabel("Years relative to SBFN adoption")
    ax.set_ylabel("ATT (event-time coefficient)")

fig.suptitle("Country-level staggered event-study, SBFN adoption on macro environmental outcomes\n"
             "(Callaway-Sant'Anna, doubly-robust, log GDP per capita control; shaded = pointwise 95% CI;\n"
             "relative periods beyond $\\pm$12/9 trimmed, too few surviving cohorts to be informative)",
             fontsize=9.5)
fig.tight_layout(rect=[0, 0, 1, 0.86])
fig.savefig("output/figures/fig6_macro_event_study.png", dpi=200)
print("Saved output/figures/fig6_macro_event_study.png")
