#@title Load libraries
import numpy as np
import pandas as pd

from bs4 import BeautifulSoup

from sklearn.cluster import KMeans

from scipy.spatial.distance import cdist

from flask import Flask, render_template, url_for, request, redirect


google_map_api_key ='AIzaSyCXiYNuz_bIzPDXFeMVcYSNhSTSZwHflCE'

app = Flask(__name__)

def destinations(kml_filename):
    places = []

    with open(kml_filename, "r") as file:
        content = file.readlines()
        content = "".join(content)
        bs_content = BeautifulSoup(content, "xml")

        placemarks = bs_content.findAll('Placemark')
        for placemark in placemarks:
            coordinates = placemark.find('coordinates').text.strip()
            long = coordinates.split(',')[0]
            lat = coordinates.split(',')[1]

            places.append({
                'name': placemark.find('name').text.strip(),
                'lat': lat,
                'long': long
            })

    places = pd.DataFrame(places)
    places['lat'] = places['lat'].astype(float)
    places['long'] = places['long'].astype(float)

    mean_lat = places['lat'].mean()
    mean_long = places['long'].mean()

    places_lat_long = places[['lat', 'long']].values.tolist()
    places_lat_long = np.array(places_lat_long)

    return places


def state(df, location):
    df = df[df["state"] == location]
    return df


def trip_plan(num_days, places):
    places_lat_long = places[['lat', 'long']].values.tolist()
    places_lat_long = np.array(places_lat_long)
    kmeans = KMeans(n_clusters=int(num_days), random_state=0).fit(places_lat_long)
    group = list(kmeans.labels_)
    places['cluster'] = pd.Series(group, index=places.index)
    return places


def planner(starting_point, places, journey_type):
    mean_lat_long_by_group = places.groupby('cluster').mean()
    distance_matrix = cdist(
        mean_lat_long_by_group.values,
        mean_lat_long_by_group.values)

    df_distance_matrix = pd.DataFrame(distance_matrix)
    cur_index = starting_point

    seq = [cur_index]
    while len(seq) < len(list(df_distance_matrix.keys())):
        if journey_type == 1:
            nearest_clusters = list(df_distance_matrix[cur_index].sort_values().index)
            for cluster_id in nearest_clusters:
                if cluster_id != cur_index and cluster_id not in seq:
                    seq.append(cluster_id)
                    cur_index = cluster_id
                    break

        if journey_type == 0:
            nearest_clusters = list(df_distance_matrix[cur_index].sort_values(ascending=False).index)
            for cluster_id in nearest_clusters:
                if cluster_id != cur_index and cluster_id not in seq:
                    seq.append(cluster_id)
                    cur_index = cluster_id
                    break

    replace_group_to_day = {}

    for i in range(0, len(seq)):
        replace_group_to_day[seq[i]] = i

    places['days'] = places['cluster']
    places['days'].replace(replace_group_to_day, inplace=True)
    places['days'] += 1
    planned = places.sort_values(by=['days'])
    print(' -> '.join(str(x) for x in seq))

    return planned

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':

        selected_destination = request.form['places']
        num_days = request.form['days']

        malaysia = destinations("malaysia.kml")
        new = malaysia["name"].str.split(", ", n=1, expand=True)
        malaysia["place"] = new[0]
        malaysia["state"] = new[1]

        kl = state(malaysia, selected_destination)
        kl_trip = trip_plan(num_days, kl)
        kl_plan = planner(1, kl_trip, 1)
        return render_template('index.html', tables=[kl_plan.to_html(classes='kl')])



if __name__ == "__main__":


    app.run(debug=True)
