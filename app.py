import traceback
from flask import Flask, request, jsonify, render_template
from lastfm import get_lastfm_data
from rescuetime import get_rescuetime_data
from ifttt import send_report
app = Flask(__name__)


@app.route('/daily_summary/', methods=['GET'])
def daily_summary():
    response = {}
    artists = get_lastfm_data()
    categories = get_rescuetime_data()
    max_seconds = max([category["seconds"] for category in categories])
    for category in categories:
        category["bar_width"] = 40 * category["seconds"] / max_seconds + 60
    send_report(artists, categories)
    response["message"] = "The report will arrive in a few minutes"

    return jsonify(response)

# A welcome message to test our server
@app.route('/sample_email')
def last_email_sample():
    sample_artist_data = [
        {
            "name": "Bayside",
            "rank": "1",
            "playcount": "23",
        },
        {
            "name": "La Dispute",
            "rank": "2",
            "playcount": "13",
        },
        {
            "name": "Anarbor",
            "rank": "3",
            "playcount": "12",
        },
    ]
    sample_categories_data = [
        {
            "rank": 1,
            "time": "2h 3m",
            "category": "Software Development",
            "seconds": 400,
        },
        {
            "rank": 2,
            "time": "1h 4m",
            "category": "Reference and Learning",
            "seconds": 300,
        },
    ]
    max_seconds = max([category["seconds"] for category in sample_categories_data])
    for category in sample_categories_data:
        category["bar_width"] = 100 * category["seconds"] / max_seconds
    return render_template(
        'email.jinja.html', 
        artists=sample_artist_data,
        categories=sample_categories_data,
    )


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
