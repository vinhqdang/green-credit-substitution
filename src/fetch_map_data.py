import os
import urllib.request
import zipfile

os.makedirs('data/geo', exist_ok=True)
url = 'https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip'
zpath = 'data/geo/ne_110m_admin_0_countries.zip'
if not os.path.exists(zpath):
    urllib.request.urlretrieve(url, zpath)
    print('downloaded', zpath)
else:
    print('already exists')

with zipfile.ZipFile(zpath) as z:
    z.extractall('data/geo/ne_110m_admin_0_countries')
print('extracted')

import geopandas as gpd
gdf = gpd.read_file('data/geo/ne_110m_admin_0_countries')
print(gdf.shape)
print(gdf.columns.tolist())
print(gdf[['ADMIN', 'ISO_A3']].head(10))
