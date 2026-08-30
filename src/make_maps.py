"""
Figure 1: two-panel world choropleth -- Panel A: green practice adoption
rate by country (47 economies), Panel B: SBFN green-finance policy status
by country. Modeled on the reference article's Fig. 1 world-map device.
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

pd.set_option('display.width', 160)


def build_country_agg():
    main = pd.read_parquet('data/processed/analysis_main.parquet')
    ext = pd.read_parquet('data/processed/analysis_extension.parquet')

    main_agg = main.groupby(['country_survey_label', 'iso3', 'sbfn_member']).agg(
        green_rate=('green_adoption_binary', 'mean'), n=('firm_id', 'count')
    ).reset_index()

    # extension sample: use whichever green indicator is available for each country
    ext['green_proxy'] = ext['co2_monitor'].fillna(ext['waste_minimization'])
    ext_agg = ext.groupby(['country_survey_label']).agg(
        green_rate=('green_proxy', 'mean'), n=('firm_id', 'count')
    ).reset_index()
    macro = pd.read_csv('data/macro_moderators.csv')
    ext_agg = ext_agg.merge(macro[['country_survey_label', 'iso3', 'sbfn_member']],
                             on='country_survey_label', how='left')

    full = pd.concat([main_agg, ext_agg], ignore_index=True)
    full['sbfn_member'] = pd.to_numeric(full['sbfn_member'], errors='coerce')
    return full


def main():
    agg = build_country_agg()
    agg.to_csv('data/processed/country_map_data.csv', index=False)

    world = gpd.read_file('data/geo/ne_110m_admin_0_countries')
    world = world.merge(agg, left_on='ISO_A3', right_on='iso3', how='left')

    fig, axes = plt.subplots(2, 1, figsize=(14, 14))

    world.plot(column='green_rate', ax=axes[0], legend=True, cmap='YlGn',
               missing_kwds={'color': 'lightgrey'}, edgecolor='white', linewidth=0.3,
               legend_kwds={'label': 'Green practice adoption rate', 'shrink': 0.6})
    axes[0].set_title('Panel A: Firm-level green practice adoption rate, by economy', fontsize=12)
    axes[0].axis('off')

    import matplotlib.patches as mpatches
    world.plot(ax=axes[1], color='#e8e8e8', edgecolor='white', linewidth=0.3)  # base layer: not in sample
    world[world['sbfn_member'] == 0.0].plot(ax=axes[1], color='#6baed6', edgecolor='white', linewidth=0.3)
    world[world['sbfn_member'] == 1.0].plot(ax=axes[1], color='#08306b', edgecolor='white', linewidth=0.3)
    axes[1].legend(handles=[
        mpatches.Patch(color='#08306b', label='SBFN sustainable-finance policy member'),
        mpatches.Patch(color='#6baed6', label='In sample, not an SBFN member'),
        mpatches.Patch(color='#e8e8e8', label='Not in sample'),
    ], loc='lower left', fontsize=9, frameon=False)
    axes[1].set_title('Panel B: SBFN sustainable-finance policy membership, by economy', fontsize=12)
    axes[1].axis('off')

    plt.tight_layout()
    import os
    os.makedirs('output/figures', exist_ok=True)
    plt.savefig('output/figures/fig1_world_map.png', dpi=250, bbox_inches='tight')
    print('Saved output/figures/fig1_world_map.png')


if __name__ == '__main__':
    main()
