import dotenv
import json
import os
import flask

from api import (
    get_access_token_from_auth_code,
    get_athlete_koms,
    get_strava_auth_url
)

if __name__ == "__main__":
    dotenv.load_dotenv()
    STRAVA_CLIENT_ID = os.environ.get("STRAVA_CLIENT_ID")
    STRAVA_CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET")
    redirect_uri = os.getenv('REDIRECT_URI')
    if not redirect_uri:
        redirect_uri = "http://localhost:5000/callback"

    app = flask.Flask(__name__)

    @app.route("/")
    def index():
        return flask.redirect(get_strava_auth_url(STRAVA_CLIENT_ID, redirect_uri))

    @app.route('/callback')
    def callback():
        auth_code = flask.request.args.get('code')
        if not auth_code:
            return "Authorization failed. No auth code received."

        access_token = get_access_token_from_auth_code(
            client_id=STRAVA_CLIENT_ID,
            client_secret=STRAVA_CLIENT_SECRET,
            auth_code=auth_code,
        )
        koms = get_athlete_koms(access_token)

        min_kom_lat = min([kom.segment_start_latitude for kom in koms])
        min_kom_long = min([kom.segment_start_longitude for kom in koms])
        max_kom_lat = max([kom.segment_start_latitude for kom in koms])
        max_kom_long = max([kom.segment_start_longitude for kom in koms])

        poi_data_json = json.dumps([kom.to_dict() for kom in koms])
        return flask.render_template(
            "index.html",
            poi_data=poi_data_json,
            min_bound=[min_kom_lat, min_kom_long],
            max_bound=[max_kom_lat, max_kom_long],
        )

    app.run(debug=True)
