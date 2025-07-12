import os
import requests
import json
from datetime import datetime

# --- CONFIG ---
API_KEY = os.environ.get('OPENWEATHER_API_KEY')
CITY = os.environ.get('CITY', 'London')
DATA_DIR = 'data'

if not API_KEY:
    raise ValueError("No API key provided. Set the OPENWEATHER_API_KEY environment variable.")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Build API URL
url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric'

# Fetch weather data
response = requests.get(url)
if response.status_code != 200:
    raise RuntimeError(f"Failed to fetch weather data: {response.status_code} {response.text}")
data = response.json()

# Timestamp for file name
now = datetime.utcnow().strftime('%Y-%m-%d_%H')
filename = f'{DATA_DIR}/{now}.json'

# Write timestamped file
with open(filename, 'w') as f:
    json.dump(data, f, indent=2)

# Update 'latest.json' for easy access
with open(f'{DATA_DIR}/latest.json', 'w') as f:
    json.dump(data, f, indent=2)

print(f"Saved weather data to {filename} and updated data/latest.json")
