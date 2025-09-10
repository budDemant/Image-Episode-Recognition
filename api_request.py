import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("TMDB_API_KEY")

tv_show_query = str(input("Search for a TV Show: ")) # query value must be string


url = "https://api.themoviedb.org/3/search/tv"
params = {
    "api_key": API_KEY,
    "query": tv_show_query
}

response = requests.get(url, params=params)
if response.status_code == 200:
    print(f'Search results for "{tv_show_query}"')
    data = response.json()
    results = data.get("results", [])
    for show in results:
        name = show.get("name")
        first_air_date = show.get("first_air_date", "")
        year = first_air_date[:4] if first_air_date else "N/A"
        # TODO: numbered list of results, then prompt user for Season number
        print(f"{name} ({year})")
else:
    print(f"Error: {response.status_code} - {response.text}")