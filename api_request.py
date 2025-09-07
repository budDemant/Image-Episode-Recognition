import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("TMDB_API_KEY")

url = "https://api.themoviedb.org/3/search/tv"
params = {
    "api_key": API_KEY,
    "query": "The Sopranos"
}

response = requests.get(url, params=params)
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")