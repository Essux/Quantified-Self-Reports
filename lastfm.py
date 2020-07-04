from flask import render_template
import requests
import os

from local_hour import get_local_day_timestamps

LASTFM_API_KEY = os.environ['LASTFM_API_KEY']
LASTFM_API = "http://ws.audioscrobbler.com/2.0/"


def get_lastfm_data():
    day_start_timestamp, day_end_timestamp = get_local_day_timestamps()
    payload = {
        "method": "user.getweeklyartistchart",
        "user": "jjsuarestra99",
        "api_key": LASTFM_API_KEY,
        "format": "json",
        "from": day_start_timestamp,
        "to": day_end_timestamp,
    }
    print("Querying LastFM server")
    r = requests.get(LASTFM_API, params=payload)
    print("Response obtained")

    r = r.json()
    if "error" in r:
        print(r)

    artist_data = r["weeklyartistchart"]["artist"]
    metadata = r["weeklyartistchart"]["@attr"]

    artists = []
    for artist in artist_data:
        rank = int(artist["@attr"]["rank"])
        playcount = artist["playcount"]
        name = artist["name"]
        if rank<=5:
            artists.append({
                "name": name,
                "rank": rank,
                "playcount": playcount
            })

    return artists
