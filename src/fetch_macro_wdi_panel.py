"""
Fetch WDI country-year panels for the macro supplementary event-study:
- EG.FEC.RNEW.ZS: renewable energy consumption (% of total final energy consumption)
- EN.GHG.CO2.PC.CE.AR5: CO2 emissions per capita (AR5 GWP-consistent series)
- NY.GDP.PCAP.KD: GDP per capita, constant 2015 US$ (covariate)
One bulk 'country/all' call per indicator, 2000-2024 (mechanical, no research needed).
"""
import time

import pandas as pd
import requests

INDICATORS = {
    "renew_pct": "EG.FEC.RNEW.ZS",
    "co2_pc": "EN.GHG.CO2.PC.CE.AR5",
}
YEARS = "2000:2024"

frames = []
for col, ind in INDICATORS.items():
    url = f"https://api.worldbank.org/v2/country/all/indicator/{ind}?date={YEARS}&format=json&per_page=20000"
    data = requests.get(url, timeout=30).json()
    rows = [{"iso3": o["countryiso3code"], "year": int(o["date"]), col: o["value"]} for o in data[1]]
    df = pd.DataFrame(rows)
    print(f"{col} ({ind}): {df[col].notna().sum()} non-null obs across {df['iso3'].nunique()} iso3 codes")
    frames.append(df.set_index(["iso3", "year"]))
    time.sleep(0.2)

wdi = frames[0].join(frames[1], how="outer").reset_index()
wdi.to_csv("data/macro_wdi_panel_raw.csv", index=False)
print(f"Saved data/macro_wdi_panel_raw.csv, {len(wdi)} rows")

url = f"https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.KD?date={YEARS}&format=json&per_page=20000"
data = requests.get(url, timeout=30).json()
rows = [{"iso3": o["countryiso3code"], "year": int(o["date"]), "gdppc": o["value"]} for o in data[1]]
gdp = pd.DataFrame(rows)
print(f"gdppc: {gdp['gdppc'].notna().sum()} non-null obs across {gdp['iso3'].nunique()} iso3 codes")
gdp.to_csv("data/macro_wdi_gdppc.csv", index=False)
print("Saved data/macro_wdi_gdppc.csv")
