from zipcode import get_zipcode
from collections import defaultdict
import overpass
import pandas as pd
from rich import print
from tqdm.auto import tqdm
api = overpass.API()

def proc_zipcode(row):
    return get_zipcode(float(row['Lat']), float(row['Lon']))

def collect_locations(city, query, feat='amenity'):
    return \
        f"""
        area[name="{city}"];
        node["{feat}"~"{query}"](area);
        out;
        """

def collect_location(cities, query, feat='amenity'):
    coords = defaultdict(list)
    archive = defaultdict(list)
    for city in tqdm(cities):
        response = api.get(collect_locations(city, query, feat))
        for feature in response['features']:
            try:
                coords[city].append(feature['geometry']['coordinates'])
                archive[city].append(feature)
            except:
                continue

    df = pd.DataFrame(columns=['City', 'Lat', 'Lon', 'Zipcode'])
    for k,v in coords.items():
        for lon, lat in v:
            df.loc[len(df)] = [k, lat, lon, '']
    return df

def collect_locations_zip(cities, amenity, feat='amenity'):
    tqdm.pandas()
    df = collect_location(cities, amenity, feat)
    df['Zipcode'] = df.progress_apply(proc_zipcode, axis=1)
    return df
