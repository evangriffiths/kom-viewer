# KOM Map Viewer

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

Get your API refresh code by running:

```bash
python authorize.py
```

This opens a browser window to the Strava API authorization page.

Once you authorize the app, you will be redirected to another page. If you look in your terminal log, you will find your refresh code:

```bash
STRAVA_REFRESH_TOKEN=...
```

Optionally add this to your .env file to prevent the need to authorize every time you use the app.

## Run

Run:

```bash
python app.py
```
