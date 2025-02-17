import os
import math
import urllib.request
import pandas as pd
import geopandas as gpd
import folium
import matplotlib.pyplot as plt
from matplotlib.colors import to_hex
from geopy.distance import geodesic
import networkx as nx
import pulp

def download_file(url, out_path):
    if not os.path.exists(out_path):
        print(f"Downloading {url} to {out_path} ...")
        urllib.request.urlretrieve(url, out_path)
    else:
        print(f"File {out_path} already exists.")

def load_county_city_tables():
    url = "https://en.wikipedia.org/wiki/List_of_cities_and_counties_in_Virginia#cite_note-wwwcensusgov2-8"
    try:
        tables = pd.read_html(url)
        county_table = tables[2]
        city_table = tables[3]
    except Exception as e:
        print(f"Error reading tables from Wikipedia: {e}")
        raise
    county_df = county_table[['County', 'Population[8]']].copy()
    county_df.rename(columns={'Population[8]': 'Population'}, inplace=True)
    city_df = city_table[['City', 'Population[11]']].copy()
    city_df.rename(columns={'Population[11]': 'Population'}, inplace=True)
    city_df['City'] = city_df['City'] + " city"
    return county_df, city_df

def load_adjacency_data():
    adj_file = "county_adjacency2024.txt"
    url = "https://www2.census.gov/geo/docs/reference/county_adjacency/county_adjacency2024.txt"
    download_file(url, adj_file)
    try:
        adjacency_df = pd.read_csv(adj_file, delimiter="|", header=0)
        print("Sample adjacency data:")
        print(adjacency_df.head())
    except Exception as e:
        print(f"Error reading adjacency data: {e}")
        raise
    return adjacency_df

def merge_county_city_data(county_df, city_df, adjacency_df):
    county_df.rename(columns={'County': 'County/City'}, inplace=True)
    city_df.rename(columns={'City': 'County/City'}, inplace=True)
    df = pd.concat([county_df, city_df], ignore_index=True)
    filtered_df = adjacency_df[
        adjacency_df['County Name'].str.contains(", VA") & adjacency_df['Neighbor Name'].str.contains(", VA")
    ].copy()
    filtered_df['County Name'] = filtered_df['County Name'].str.replace(', VA', '', regex=False)
    filtered_df['Neighbor Name'] = filtered_df['Neighbor Name'].str.replace(', VA', '', regex=False)
    filtered_df = filtered_df[filtered_df['County GEOID'] != filtered_df['Neighbor GEOID']]
    aggregated_df = filtered_df.groupby(['County Name', 'County GEOID']).agg(
        {'Neighbor Name': list, 'Neighbor GEOID': list}
    ).reset_index()
    aggregated_df.rename(columns={'Neighbor Name': 'Neighbor Names', 'Neighbor GEOID': 'Neighbor GEOIDs'}, inplace=True)
    df = pd.merge(df, aggregated_df, left_on='County/City', right_on='County Name', how='inner').drop(columns=['County Name'])
    df['County/City'] = df['County/City'].str.replace('city', 'City', regex=False)
    return df, filtered_df, aggregated_df

def visualize_counties(df, gdf, title="Virginia Counties"):
    m = folium.Map(location=[37.54, -77.46], zoom_start=8)
    folium.Choropleth(
        geo_data=gdf,
        name='Virginia Population',
        data=df,
        columns=['County/City', 'Population'],
        key_on='feature.properties.NAMELSAD',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Population',
        highlight=True,
    ).add_to(m)
    def style_function(feature):
        return {
            'fillColor': '#ffff00',
            'color': '#000000',
            'weight': 0.5,
            'fillOpacity': 0.5,
        }
    def highlight_function(feature):
        return {
            'fillColor': '#0000ff',
            'color': '#000000',
            'weight': 1,
            'fillOpacity': 0.7,
        }
    folium.GeoJson(
        gdf,
        style_function=style_function,
        highlight_function=highlight_function,
        tooltip=folium.GeoJsonTooltip(
            fields=['NAMELSAD'],
            aliases=['County/City:'],
            sticky=True,
        )
    ).add_to(m)
    m.save("counties_map.html")
    print("County visualization saved to counties_map.html")

def base_model_redistricting(df, target_population, num_districts=11):
    print("\nSetting up base model redistricting with PuLP...")
    df = df.copy()
    df['Population'] = df['Population'].astype(int)
    base_model_df = df.set_index('County GEOID')
    county_cities = base_model_df.to_dict(orient='index')
    counties = list(county_cities.keys())
    populations = {key: int(value['Population']) for key, value in county_cities.items()}
    prob = pulp.LpProblem("RedistrictingBase", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("x", [(i, j) for i in counties for j in range(num_districts)], cat='Binary')
    abs_diff = pulp.LpVariable.dicts("abs_diff", [j for j in range(num_districts)], lowBound=0, cat='Continuous')
    prob += pulp.lpSum(abs_diff[j] for j in range(num_districts))
    for i in counties:
        prob += pulp.lpSum(x[i, j] for j in range(num_districts)) == 1
    for j in range(num_districts):
        district_pop = pulp.lpSum(populations[i] * x[(i, j)] for i in counties)
        prob += district_pop - target_population <= abs_diff[j]
        prob += target_population - district_pop <= abs_diff[j]
    print("Solving base model...")
    prob.solve()
    print(f"Base Model Status: {pulp.LpStatus[prob.status]}")
    district_assignments = {}
    for i in counties:
        for j in range(num_districts):
            if pulp.value(x[i, j]) == 1:
                print(f"County {county_cities[i]['County/City']} (GEOID: {i}) -> District {j}")
                district_assignments[i] = j + 1
    base_model_df['District'] = base_model_df.index.map(district_assignments).fillna(-1)
    district_populations = base_model_df.groupby('District')['Population'].sum()
    district_counties = base_model_df.groupby('District')['County/City'].apply(list)
    result_df = pd.DataFrame({'Population': district_populations, 'Counties': district_counties})
    print("\nBase Model District Summary:")
    print(result_df)
    return base_model_df

def add_contiguity_and_run(df, base_model_df, num_districts=11, deviation=0.30):
    print("\nSetting up contiguity model...")
    total_population = df['Population'].sum()
    L = math.ceil((1 - deviation/2) * total_population / num_districts)
    U = math.floor((1 + deviation/2) * total_population / num_districts)
    print(f"Population bounds: L = {L}, U = {U}")
    counties = list(base_model_df.index)
    dist = {(i, j): 1.0 for i in counties for j in counties}
    prob = pulp.LpProblem("RedistrictingContiguity", pulp.LpMinimize)
    x = pulp.LpVariable.dicts("x", [(i, j) for i in counties for j in counties], cat='Binary')
    prob += pulp.lpSum(dist[i, j]**2 * base_model_df.loc[i, 'Population'] * x[i, j] for i in counties for j in counties)
    for i in counties:
        prob += pulp.lpSum(x[i, j] for j in counties) == 1
    prob += pulp.lpSum(x[j, j] for j in counties) == num_districts
    for i in counties:
        for j in counties:
            prob += x[i, j] <= x[j, j]
    DG = nx.DiGraph()
    for county in df.index:
        DG.add_node(county)
    for index, row in df.iterrows():
        neighbors = row['Neighbor Names']
        neighbor_geoids = row['Neighbor GEOIDs']
        for n, neighbor in enumerate(neighbors):
            neighbor_geoid = neighbor_geoids[n]
            if neighbor_geoid in DG:
                DG.add_edge(index, neighbor_geoid)
                DG.add_edge(neighbor_geoid, index)
    print(f"Contiguity graph: {DG.number_of_nodes()} nodes, {DG.number_of_edges()} edges")
    f = pulp.LpVariable.dicts("f", [(j, u, v) for j in DG.nodes for u, v in DG.edges], lowBound=0, cat='Continuous')
    M = len(DG.nodes) - 1
    for j in DG.nodes:
        for u in DG.neighbors(j):
            prob += pulp.lpSum(f[j, u, j] for _ in DG.neighbors(j)) == 0
    print("Solving contiguity model...")
    prob.solve(pulp.PULP_CBC_CMD(msg=True))
    print(f"Contiguity Model Status: {pulp.LpStatus[prob.status]}")
    centers = [j for j in counties if pulp.value(x[j, j]) > 0.5]
    districts = [[i for i in counties if pulp.value(x[i, j]) > 0.5] for j in centers]
    for idx, district in enumerate(districts):
        for county in district:
            base_model_df.loc[county, 'District'] = idx + 1
    return base_model_df, districts

def add_historical_voting(df):
    print("\nLoading historical voting data...")
    election_url = "https://historical.elections.virginia.gov/elections/download/144567/precincts_include:0/"
    try:
        election_df = pd.read_csv(election_url)
    except Exception as e:
        print(f"Error loading election data: {e}")
        return None
    election_df = election_df.drop(0).reset_index(drop=True)
    election_df = election_df.drop(['Unnamed: 1', 'Unnamed: 2'], axis=1)
    election_df.columns = ['County/City', 'Democratic', 'Republican', 'Libertarian', 'All Others', 'Total Votes']
    election_df = election_df.drop(election_df.index[-1]).reset_index(drop=True)
    for col in ['Democratic', 'Republican', 'Libertarian', 'All Others', 'Total Votes']:
        election_df[col] = pd.to_numeric(election_df[col].str.replace(',', ''), errors='coerce').fillna(0).astype(int)
    election_df['County/City'] = election_df['County/City'].str.strip()
    print("Sample election data:")
    print(election_df.head())
    return election_df

def main():
    county_df, city_df = load_county_city_tables()
    adjacency_df = load_adjacency_data()
    df, filtered_df, aggregated_df = merge_county_city_data(county_df, city_df, adjacency_df)
    print("First few rows of combined county/city data:")
    print(df.head())
    population_sum = df['Population'].sum()
    chosen_state = 'Virginia'
    num_districts = 11
    print(f"Total population: {population_sum:,}")
    print(f"Number of counties/independent cities: {len(df)}")
    target_population = population_sum // num_districts
    print(f"Target population per district: {target_population:,}")
    shapefile_path = "./data/VirginiaCounty.shp"
    if os.path.exists(shapefile_path):
        gdf = gpd.read_file(shapefile_path)
    else:
        print(f"Shapefile {shapefile_path} not found. Skipping county visualization.")
        gdf = None
    if gdf is not None:
        visualize_counties(df, gdf)
    base_model_df = base_model_redistricting(df, target_population, num_districts)
    base_model_df, districts = add_contiguity_and_run(df, base_model_df, num_districts)
    print("District assignments after contiguity model:")
    print(base_model_df[['County/City', 'Population', 'District']])
    election_df = add_historical_voting(df)
    if election_df is not None:
        print("Historical voting data processed.")
    base_model_df.to_csv("final_district_assignments.csv")
    print("Final district assignments saved to final_district_assignments.csv")

if __name__ == '__main__':
    main()
