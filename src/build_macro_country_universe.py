"""
Build the country-level treatment panel for the supplementary macro
staggered-DID analysis (Section on country-level evidence): every real
(non-aggregate) World Bank country, its SBFN ever-join year (from
data/sbfn_roster.csv, cross-checked against data/global_sbfn.csv), or
"never treated" if it appears on neither.
"""
import unicodedata

import pandas as pd
import requests

resp = requests.get(
    "https://api.worldbank.org/v2/country?format=json&per_page=400", timeout=30
)
data = resp.json()
countries = []
for c in data[1]:
    if c["region"]["value"] == "Aggregates":
        continue
    countries.append({
        "iso3": c["id"],
        "name": c["name"],
        "region": c["region"]["value"],
        "income_level": c["incomeLevel"]["value"],
    })
wb = pd.DataFrame(countries)
print(f"World Bank real-country list: {len(wb)} countries")


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    return s.lower().strip()


wb["name_norm"] = wb["name"].map(norm)

roster = pd.read_csv("data/sbfn_roster.csv")
print(f"SBFN roster: {len(roster)} member rows")

ALIASES = {
    "turkiye": "turkey", "kyrgyz republic": "kyrgyz republic", "lao pdr": "lao people's democratic republic",
    "laos": "lao people's democratic republic", "congo, dem. rep.": "congo, dem. rep.",
    "democratic republic of congo": "congo, dem. rep.", "republic of congo": "congo, rep.",
    "congo": "congo, rep.", "egypt": "egypt, arab rep.", "iran": "iran, islamic rep.",
    "venezuela": "venezuela, rb", "yemen": "yemen, rep.", "micronesia": "micronesia, fed. sts.",
    "cote d'ivoire": "cote d'ivoire", "ivory coast": "cote d'ivoire", "gambia": "gambia, the",
    "the gambia": "gambia, the", "bahamas": "bahamas, the", "cape verde": "cabo verde",
    "east timor": "timor-leste", "slovakia": "slovak republic",
    "north korea": "korea, dem. people's rep.", "south korea": "korea, rep.", "korea": "korea, rep.",
    "swaziland": "eswatini", "myanmar (burma)": "myanmar", "russia": "russian federation",
    "syria": "syrian arab republic", "vietnam": "viet nam", "brunei": "brunei darussalam",
}

wb_lookup = dict(zip(wb["name_norm"], wb["iso3"]))


def match_iso3(member_name):
    n = norm(member_name)
    if n in wb_lookup:
        return wb_lookup[n]
    if n in ALIASES and ALIASES[n] in wb_lookup:
        return wb_lookup[ALIASES[n]]
    hits = [iso for name, iso in wb_lookup.items() if n in name or name in n]
    return hits[0] if len(hits) == 1 else None


roster["iso3"] = roster["member_name"].map(match_iso3)
unmatched = roster[roster["iso3"].isna()]
if len(unmatched):
    print(f"WARNING: {len(unmatched)} unmatched roster rows:")
    print(unmatched[["member_name", "notes"]].to_string(index=False))

global_sbfn = pd.read_csv("data/global_sbfn.csv")
gs_members = global_sbfn[global_sbfn["sbfn_member"] == 1][["iso3", "sbfn_join_year"]].drop_duplicates()

roster_join = roster.dropna(subset=["iso3"])[["iso3", "join_year"]].rename(columns={"join_year": "join_year_roster"})
merged_check = gs_members.merge(roster_join, on="iso3", how="outer")
disagree = merged_check[
    merged_check["sbfn_join_year"].notna()
    & merged_check["join_year_roster"].notna()
    & (merged_check["sbfn_join_year"] != merged_check["join_year_roster"])
]
print(f"Join-year disagreements between global_sbfn.csv and sbfn_roster.csv: {len(disagree)}")

treat = roster.dropna(subset=["iso3"])[["iso3", "join_year"]].drop_duplicates(subset=["iso3"])
extra = gs_members[~gs_members["iso3"].isin(treat["iso3"])].rename(columns={"sbfn_join_year": "join_year"})
treat = pd.concat([treat, extra], ignore_index=True)
treat["join_year"] = treat["join_year"].astype(float)

panel = wb.merge(treat, on="iso3", how="left")
panel["ever_treated"] = panel["join_year"].notna()
print(f"Final country universe: {len(panel)} countries, {panel['ever_treated'].sum()} ever-SBFN-treated, "
      f"{(~panel['ever_treated']).sum()} never-treated (control pool)")

panel.to_csv("data/macro_country_treatment_panel.csv", index=False)
print("Saved data/macro_country_treatment_panel.csv")
