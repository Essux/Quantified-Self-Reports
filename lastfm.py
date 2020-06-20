import requests
import os
from datetime import datetime, timezone, timedelta

LASTFM_API_KEY = os.environ['LASTFM_API_KEY']
print(LASTFM_API_KEY)
#LASTFM_API_KEY = "c3ba5cc66dea759e68b15becf7f22a6f"
LASTFM_API = "http://ws.audioscrobbler.com/2.0/"

IFTTT_API_KEY = os.environ['IFTTT_API_KEY']
#IFTTT_API_KEY = "b_pkxKIkzdFiLXPCLlEt-k"
IFTTT_API = f"https://maker.ifttt.com/trigger/lastfm_notify/with/key/{IFTTT_API_KEY}"

def get_local_day_timestamps():
    bogota_timezone = timezone(timedelta(hours=-5), "Bogota")
    current_time_local = datetime.now(timezone.utc).astimezone(tz=bogota_timezone)
    day_start_local = datetime(current_time_local.year, current_time_local.month, current_time_local.day, tzinfo=bogota_timezone)
    day_start_utc = day_start_local.astimezone(tz=timezone.utc)
    day_end_utc = day_start_utc + timedelta(days=1)
    day_start_timestamp = int(day_start_utc.timestamp())
    day_end_timestamp = int(day_end_utc.timestamp())
    return day_start_timestamp, day_end_timestamp


def send_lastfm_report():
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

    artist_text = []

    for artist in artist_data:
        rank = int(artist["@attr"]["rank"])
        playcount = artist["playcount"]
        name = artist["name"]
        if rank<=10:
            artist_text.append(f"{rank}. {name} - {playcount} plays")


    artist_text = '<br>'.join(artist_text)
    print(artist_text)

    from_timestamp = int(metadata["from"])
    to_timestamp = int(metadata["to"])
    from_date = datetime.utcfromtimestamp(from_timestamp)
    to_date = datetime.utcfromtimestamp(to_timestamp)
    print(from_date, to_date)

    payload = {
        "value1": artist_text
    }

    print("Querying IFTTT server")
    r = requests.post(IFTTT_API, data=payload)
    print("Response obtained")
    print(r.status_code)