import os
import requests
import json
from datetime import datetime

# Set your OpenWeatherMap API key as an environment variable: OPENWEATHER_API_KEY
API_KEY = os.environ.get('OPENWEATHER_API_KEY')
DATA_DIR = 'data'

if not API_KEY:
    raise ValueError("No API key provided. Set the OPENWEATHER_API_KEY environment variable.")

# List of cities with country code for disambiguation (OpenWeatherMap format: City,CC)
CITIES = {
    "aberdeen":     "Aberdeen,GB",
    "london":       "London,GB",
    "glasgow":      "Glasgow,GB",
    "bourne":       "Bourne,GB",
    "bristol":      "Bristol,GB",
    "sandwich":     "Sandwich,GB",
    "krugersdorp":  "Krugersdorp,ZA",
    "cape-town":    "Cape Town,ZA",
    "durban":       "Durban,ZA",
    "johannesburg": "Johannesburg,ZA",
    "bloemfontein": "Bloemfontein,ZA",
    "paris":        "Paris,FR",
    "milan":        "Milan,IT",
    "moscow":       "Moscow,RU",
    "new-york":     "New York,US",
    "los-angeles":  "Los Angeles,US",
    "beijing":      "Beijing,CN"
}

os.makedirs(DATA_DIR, exist_ok=True)
now = datetime.utcnow().strftime('%Y-%m-%d_%H')

for key, name in CITIES.items():
    print(f"Fetching weather for {name}...")
    url = f'https://api.openweathermap.org/data/2.5/weather?q={name}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Save latest-city.json
        latest_path = os.path.join(DATA_DIR, f'latest-{key}.json')
        with open(latest_path, 'w') as f:
            json.dump(data, f, indent=2)
        # (Optional) Save timestamped history
        ts_path = os.path.join(DATA_DIR, f'{now}-{key}.json')
        with open(ts_path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved: {latest_path}")
    else:
        print(f"Failed to fetch {name}: {response.status_code} {response.text}")
