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

def show_query_list(shows):
    """Display numbered list of shows"""
    for i, show in enumerate(shows, 1):
        name = show.get("name")
        first_air_date = show.get("first_air_date", "")
        year = first_air_date[:4] if first_air_date else "N/A"
        print(f"{i}. {name} ({year})")

def select_show(shows):
    """Get user selection from the displayed show list"""
    while True:
        try:
            choice = int(input(f"\nSelect a show (1-{len(shows)}): ")) - 1
            if 0 <= choice < len(shows):
                return shows[choice]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def select_season():
    """Get user selection of Season number"""
    # TODO: Prompt user to choose Season number
    return True

response = requests.get(url, params=params)
if response.status_code == 200:
    print(f'Search results for "{tv_show_query}"')
    data = response.json()
    results = data.get("results", [])
    show_query_list(results)
    selected_show = select_show(results)
    
else:
    print(f"Error: {response.status_code} - {response.text}")




