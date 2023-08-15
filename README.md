# KOM Viewer

A webapp using the Strava API to view your KOMs on a world map

## Setup

Install dependencies:

```python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create .env file with the following variables defined (based on values from https://www.strava.com/settings/api):

```bash
STRAVA_CLIENT_ID=...
STRAVA_CLIENT_SECRET=...
```

## Run locally

```bash
python app.py
```

Open `http://localhost:5000` in a browser. You'll be redirected to authorize this app by logging into your Strava account.

Once logged in you'll be redirected back to the app where you can view your KOMs overlaid on a world map.

## Hosting

Hosted on [Render](https://render.com/) at kom-viewer.onrender.com. Note that this link must be set in the 'Authorization Callback Domain' field at https://www.strava.com/settings/api. All configuration is done via Render's web GUI.
