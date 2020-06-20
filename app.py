from flask import Flask, request, jsonify, render_template
from lastfm import send_lastfm_report
app = Flask(__name__)


@app.route('/daily_summary/', methods=['GET'])
def daily_summary():
    response = {}
    try:
        send_lastfm_report()
        response["message"] = "The report will arrive in a few minutes"
    except Exception:
        response["error"] = "An error has occurred"

    return jsonify(response)

# A welcome message to test our server
@app.route('/lastfm_email')
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
    return render_template('email.html', artists=sample_artist_data)


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)
