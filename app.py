import webbrowser
import dotenv
import json
import os
import requests
import urllib3
from datetime import datetime
from flask import Flask, render_template, request

from authorize import get_refresh_token


class KOM:
    def __init__(self, post_response):
        self.segment_id: str = post_response["segment"]["id"]
        self.segment_name: str = post_response["segment"]["name"]
        self.segment_start_latitude = post_response["segment"]["start_latlng"][0]
        self.segment_start_longitude = post_response["segment"]["start_latlng"][1]
        self.datetime: datetime = datetime.strptime(
            post_response["start_date"], "%Y-%m-%dT%H:%M:%SZ"
        )

    def get_segment_url(self):
        return f"https://www.strava.com/segments/{self.segment_id}"

    def to_dict(self):
        return {
            "name": self.__str__(),
            "latitude": self.segment_start_latitude,
            "longitude": self.segment_start_longitude,
            "url": self.get_segment_url(),
            "date_string": self.datetime.strftime("%d/%m/%Y"),
        }

    def __str__(self):
        return f"{self.segment_name}"

    def __repr__(self):
        return self.__str__()


def make_strava_api_request(url, access_token, params={}):
    # Prevents "Unverified HTTPS request is being made to host 'www.strava.com'"
    # warning
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    header = {"Authorization": "Bearer " + access_token}
    response = requests.get(url, headers=header, params=params)
    if response.status_code != 200:
        raise Exception(
            f"Strava API request failed with status code {response.status_code}. "
            f"Response: {response.text}"
        )
    return response.json()


def get_all_pages(url: str, access_token: str, per_page: int = 200):
    page_num = 1
    all_responses = []
    while True:
        responses = make_strava_api_request(
            url, access_token, params={"per_page": per_page, "page": page_num}
        )
        if len(responses):
            all_responses.extend(responses)
            page_num += 1
        else:
            # All pages have been pulled
            break
    return all_responses


if __name__ == "__main__":
    dotenv.load_dotenv()
    STRAVA_CLIENT_ID = os.environ.get("STRAVA_CLIENT_ID")
    STRAVA_CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET")
    STRAVA_REFRESH_TOKEN = os.environ.get("STRAVA_REFRESH_TOKEN")

    # Launches browser for autherization
    if not STRAVA_REFRESH_TOKEN:
        print(
            "Warn: 'STRAVA_REFRESH_TOKEN' env var not found. Run "
            "\n\n  python3 authorize.py\n\n"
            "to get a refresh token with 'read_all' scope. Save this token as "
            "the above env var."
        )
        STRAVA_REFRESH_TOKEN = get_refresh_token(
            STRAVA_CLIENT_ID,
            STRAVA_CLIENT_SECRET,
        )

    payload = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "refresh_token": STRAVA_REFRESH_TOKEN,
        "grant_type": "refresh_token",
        "f": "json",
    }

    auth_url = "https://www.strava.com/oauth/token"
    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()["access_token"]

    # TODO try building swagger_client library
    # import swagger_client
    # swagger_client.configuration.access_token = access_token
    # api_instance = swagger_client.ActivitiesApi()

    app = Flask(__name__)

    @app.route("/")
    def index():
        athlete_url = "https://www.strava.com/api/v3/athlete"
        athlete_info = make_strava_api_request(athlete_url, access_token)
        athlete_id = athlete_info["id"]

        kom_responses = get_all_pages(
            url=f"https://www.strava.com/api/v3/athletes/{athlete_id}/koms",
            access_token=access_token,
        )

        koms = [KOM(post_response) for post_response in kom_responses]

        min_kom_lat = min([kom.segment_start_latitude for kom in koms])
        min_kom_long = min([kom.segment_start_longitude for kom in koms])
        max_kom_lat = max([kom.segment_start_latitude for kom in koms])
        max_kom_long = max([kom.segment_start_longitude for kom in koms])

        poi_data_json = json.dumps([kom.to_dict() for kom in koms])
        return render_template(
            "index.html",
            poi_data=poi_data_json,
            min_bound=[min_kom_lat, min_kom_long],
            max_bound=[max_kom_lat, max_kom_long],
        )

    app.run(debug=True)
