import webbrowser
import queue
import requests
import threading
from flask import Flask, request


def get_auth_code(client_id, port=8000):
    """
    Opens a browser window to the Strava API authorization page.

    Once you authorize the app, launches a local server to handle the GET
    request from the callback. This gets the auth code, which is then returned
    from this function.

    If forgotton what's going on here, see
    https://chat.openai.com/c/e5bcc3af-924a-4683-bc2c-8c82f5dd99ed
    """
    route = "/auth_code"
    auth_url = (
        f"https://www.strava.com/oauth/authorize?client_id={client_id}"
        f"&redirect_uri=http://localhost:{port}{route}"
        f"&response_type=code&scope=activity:read_all"
    )

    webbrowser.open(auth_url, new=0, autoraise=True)

    app = Flask(__name__)
    authorization_queue = queue.Queue()

    @app.route(route, methods=["GET"])
    def handle_callback():
        code = request.args.get("code")
        if code:
            authorization_queue.put(code)
            return "Authorization Code Received. You can now close this window."
        else:
            return "No Authorization Code Received. Something went wrong!"

    server_thread = threading.Thread(
        target=app.run, kwargs={"host": "localhost", "port": port}
    )
    server_thread.daemon = True  # Set as a daemon thread to allow the script to exit
    server_thread.start()

    return authorization_queue.get()


def get_refresh_token(client_id, client_secret, port=8000):
    # Launches browser for autherization
    auth_code = get_auth_code(client_id, port)

    url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": auth_code,
    }
    response = requests.post(url, data=payload).json()
    return response["refresh_token"]


if __name__ == "__main__":
    import dotenv
    import os

    dotenv.load_dotenv()
    STRAVA_CLIENT_ID = os.environ.get("STRAVA_CLIENT_ID")
    STRAVA_CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET")
    STRAVA_REFRESH_TOKEN = os.environ.get("STRAVA_REFRESH_TOKEN")
    if STRAVA_REFRESH_TOKEN:
        print(
            "Doing nothing. STRAVA_REFRESH_TOKEN environment variable is "
            "already set."
        )
    else:
        STRAVA_REFRESH_TOKEN = get_refresh_token(
            STRAVA_CLIENT_ID,
            STRAVA_CLIENT_SECRET,
        )
        print(f"Add to .env:\n\nSTRAVA_REFRESH_TOKEN={STRAVA_REFRESH_TOKEN}")
