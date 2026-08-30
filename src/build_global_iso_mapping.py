"""
Build country_survey_label -> country_name, iso3 mapping for the 160
global-sample country-years, handling encoding artifacts and WBES-specific
naming quirks. Also folds in Bangladesh 2022 (present in our hand-built
extension sample but absent from the master standardized file).
"""
import re
import pandas as pd
import pycountry

with open('data/global_country_list.txt', encoding='utf-8') as f:
    labels = [l.strip() for l in f if l.strip()]

# manual fixes for concatenated / mis-encoded names before splitting off the year
NAME_FIXES = {
    'BurkinaFaso': 'Burkina Faso',
    'ElSalvador': 'El Salvador',
    'SriLanka': 'Sri Lanka',
    'SaudiArabia': 'Saudi Arabia',
    "CÃ´te d'Ivoire": "Cote d'Ivoire",
}

# manual ISO3 overrides where pycountry fuzzy search fails or is ambiguous
ISO3_OVERRIDES = {
    'Antigua and Barbuda': 'ATG', 'Bosnia and Herzegovina': 'BIH', 'Brunei Darussalam': 'BRN',
    "Cote d'Ivoire": 'CIV', 'DRC': 'COD', 'Federal Republic of Somalia': 'SOM',
    'Hong Kong SAR China': 'HKG', 'Kiribati': 'KIR', 'Korea Republic': 'KOR',
    'Kosovo': 'XKX', 'Lao PDR': 'LAO', 'North Macedonia': 'MKD', 'Papua New Guinea': 'PNG',
    'Sao Tome and Principe': 'STP', 'Solomon Islands': 'SLB', 'St. Lucia': 'LCA',
    'St. Vincent and the Grenadines': 'VCT', 'Taiwan China': 'TWN', 'Timor-Leste': 'TLS',
    'Trinidad and Tobago': 'TTO', 'Turkiye': 'TUR', 'Turkmenistan': 'TKM', 'Viet Nam': 'VNM',
    'West Bank And Gaza': 'PSE', 'Congo': 'COG', 'Cabo Verde': 'CPV', 'Eswatini': 'SWZ',
    'Equatorial Guinea': 'GNQ', 'Central African Republic': 'CAF', 'Czechia': 'CZE',
    'Slovak Republic': 'SVK', 'Kyrgyz Republic': 'KGZ', 'Moldova': 'MDA', 'Russian Federation': 'RUS',
    'Niger': 'NER', 'Nigeria': 'NGA', 'Gambia': 'GMB', 'DRC': 'COD',
}


def split_label(label):
    m = re.match(r'^(.*?)(\d{4})$', label)
    return (m.group(1).strip(), int(m.group(2))) if m else (label, None)


def get_iso3(name):
    if name in ISO3_OVERRIDES:
        return ISO3_OVERRIDES[name]
    try:
        result = pycountry.countries.search_fuzzy(name)
        return result[0].alpha_3
    except LookupError:
        return None


rows = []
for label in labels:
    raw_name, year = split_label(label)
    clean_name = NAME_FIXES.get(raw_name, raw_name)
    iso3 = get_iso3(clean_name)
    rows.append({'country_survey_label': label, 'country_name': clean_name, 'survey_year': year, 'iso3': iso3})

# add Bangladesh 2022 and Indonesia 2023 (both use the "_BR" randomized-module
# variable naming, which the master file's harmonization did not fold into the
# unprefixed ge7/ge8 columns -- confirmed absent from the 160-country list above;
# both are already available from our hand-built extension sample instead)
rows.append({'country_survey_label': 'Bangladesh2022', 'country_name': 'Bangladesh', 'survey_year': 2022, 'iso3': 'BGD'})
rows.append({'country_survey_label': 'Indonesia2023', 'country_name': 'Indonesia', 'survey_year': 2023, 'iso3': 'IDN'})

out = pd.DataFrame(rows)
unmatched = out[out['iso3'].isna()]
print(f"Total: {len(out)}, unmatched: {len(unmatched)}")
print(unmatched)

out.to_csv('data/global_country_iso_mapping.csv', index=False)
print("\nSaved data/global_country_iso_mapping.csv")
