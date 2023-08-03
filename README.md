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

## Deploy on heroku

Following instructions [here](https://devcenter.heroku.com/articles/getting-started-with-python#create-and-deploy-the-app): 

```bash
heroku login
heroku create kom-viewer
git push heroku main

# Set up env vars
heroku config:set STRAVA_CLIENT_ID=...
heroku config:set STRAVA_CLIENT_SECRET=...
heroku config:set REDIRECT_URI=http://<your-heroku-app-url>/callback
```

Note you can get the url for your app with:

```bash
heroku domains --app kom-viewer
```
