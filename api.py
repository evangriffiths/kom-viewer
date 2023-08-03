import requests
import urllib3

from kom import KOM

def get_strava_auth_url(client_id: str, redirect_uri: str) -> str:
    return (
        f"https://www.strava.com/oauth/authorize?client_id={client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code&scope=activity:read_all"
    )

def get_refresh_token_from_auth_code(client_id: str, client_secret: str, auth_code: str) -> str:
    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": auth_code,
    }
    response = requests.post(url, data=payload).json()
    return response["refresh_token"]


def get_access_token_from_refresh_token(client_id: str, client_secret: str, refresh_token: str) -> str:
    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "f": "json",
    }
    response = requests.post(url, data=payload, verify=False).json()
    return response["access_token"]

def get_access_token_from_auth_code(client_id: str, client_secret: str, auth_code: str) -> str:
    refresh_token = get_refresh_token_from_auth_code(client_id, client_secret, auth_code)
    return get_access_token_from_refresh_token(client_id, client_secret, refresh_token)

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

def get_athlete_koms(access_token: str) -> list[KOM]:
    athlete_url = "https://www.strava.com/api/v3/athlete"
    athlete_info = make_strava_api_request(athlete_url, access_token)
    athlete_id = athlete_info["id"]

    kom_responses = get_all_pages(
        url=f"https://www.strava.com/api/v3/athletes/{athlete_id}/koms",
        access_token=access_token,
    )
    return [KOM(post_response) for post_response in kom_responses]
