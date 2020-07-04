from flask import render_template
import requests
import os

IFTTT_API_KEY = os.environ['IFTTT_API_KEY']
IFTTT_API = f"https://maker.ifttt.com/trigger/lastfm_notify/with/key/{IFTTT_API_KEY}"

def send_report(artists, categories):
    email_html = render_template("email.jinja.html", artists=artists, categories=categories)
    payload = {
        "value1": email_html
    }

    print("Querying IFTTT server")
    r = requests.post(IFTTT_API, data=payload)
    print("Response obtained")
    print(r.status_code)
