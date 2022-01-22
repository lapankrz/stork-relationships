from cmath import inf
from datetime import datetime
import pandas as pd
import numpy as np
from geopy.distance import great_circle
import matplotlib.pyplot as plt
import networkx as nx
from LandUse import LandUse
import os.path

if not os.path.isfile('pajek/storks.net'):
    # csv file with stork gps data should be saved in "stork-data" directory
    # and named "LifeTrackWhiteStorkRheinland-Pfalz.csv"
    gps_data_filename = "stork-data/LifeTrackWhiteStorkRheinland-Pfalz.csv"

    col_names = ['event-id',
                'timestamp',
                'location-long',
                'location-lat',
                'individual-local-identifier',
                'tag-local-identifier']

    # reading csv file with gps data
    gps_df = pd.read_csv(gps_data_filename, usecols=col_names)
    gps_df["timestamp"] = pd.to_datetime(gps_df["timestamp"], format="%Y-%m-%d %H:%M:%S.%f")
    gps_df["timestamp"] = gps_df["timestamp"].dt.floor('Min')

    # finding the year with the most unique storks active between May and July
    max_year = 2015
    max_storks = 0
    for year in range(2015, 2022):
        mask = (gps_df["timestamp"] >= datetime(year, 5, 1)) & (gps_df["timestamp"] <= datetime(year, 7, 31))
        rows = gps_df.loc[mask]
        stork_count = len(rows["individual-local-identifier"].unique())
        if (stork_count > max_storks):
            max_storks = stork_count
            max_year = year
        print(str(year) + ": " + str(stork_count)) #the most (33) in 2018 and 2019

    # taking only the events from the most active year
    mask = (gps_df["timestamp"] >= datetime(max_year, 5, 1)) & (gps_df["timestamp"] <= datetime(max_year, 7, 31))
    gps_df = gps_df.loc[mask]
    stork_count = max_storks
    stork_ids = gps_df["individual-local-identifier"].unique()

    # calculating mean distance between each pair of storks
    distances = np.zeros((max_storks, max_storks), dtype=float)
    for i in range(max_storks):
        print(i)
        for j in range(max_storks):
            id_1 = stork_ids[i]
            id_2 = stork_ids[j]
            rows_1 = gps_df.loc[gps_df["individual-local-identifier"] == id_1].dropna(subset = ['location-long','location-lat'])
            rows_2 = gps_df.loc[gps_df["individual-local-identifier"] == id_2].dropna(subset = ['location-long','location-lat'])
            joined = pd.merge(rows_1, rows_2, on='timestamp', how='inner')
            distance = 0
            n = 0
            for index, row in joined.iterrows():
                coords_1 = (row["location-lat_x"], row["location-long_x"])
                coords_2 = (row["location-lat_y"], row["location-long_y"])
                dist = great_circle(coords_1, coords_2).km
                distance += dist**2
                n += 1
            if n > 0:
                distance /= n
                distances[i,j] = distances[j,i] = distance
            else:
                distances[i,j] = distances[j,i] = -1

    # creating the graph of stork relationships
    G = nx.Graph()
    for id in stork_ids:
        rows = gps_df.loc[gps_df["individual-local-identifier"] == id].dropna(subset = ['location-long','location-lat'])
        lat = rows['location-lat'].mean()
        long = rows['location-long'].mean()
        land_use = LandUse()
        use = land_use.get_land_use(lat, long)
        color = land_use.get_land_use_color(use)
        G.add_node(id, land_use=use, color=color)

    # adding edges with weight equal to average distance
    for i in range(max_storks):
        print("Distance to " + stork_ids[i] + ": ")
        for j in range(max_storks):
            if i != j:
                dist = distances[i,j]
                if (dist > 0):
                    G.add_edge(stork_ids[i], stork_ids[j], weight=dist)
                    print("\t" + stork_ids[j] + ": " + "{:.2f}".format(dist) + " km")

    # graph visualisation and exporting to Pajek
    nx.write_pajek(G, "storks2.net")
else:
    G = nx.read_pajek("pajek/storks.net")
    weights = nx.get_edge_attributes(G,'weight')
    H = nx.DiGraph()
    colors = nx.get_node_attributes(G,'color')
    for i in G.nodes:
        H.add_node(i, color=colors[i])
        closest_node = -1
        min_dist = inf
        for j in G.nodes:
            e = (i, j, 0)
            if e in weights:
                dist = weights[e]
                if i != j and dist < min_dist:
                    min_dist = dist
                    closest_node = j
        if closest_node != -1 and min_dist < 1000:
            weight = weights[(i, closest_node, 0)]
            H.add_edge(i, closest_node, weight=weight, inv=1/weight)
    G = H

pos = nx.spring_layout(G, iterations=150, weight='inv')
labels = dict([((u,v,), f"{d['weight']:.2f}") for u,v,d in G.edges(data=True)])
colors = nx.get_node_attributes(G,'color').values()
nx.draw(G, pos, node_color=colors)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()