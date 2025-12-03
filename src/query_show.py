import os
import requests
from dotenv import load_dotenv

load_dotenv()

class QueryShow:
    def __init__(self):
        self.api_key = os.environ.get("TMDB_API_KEY")
        self.url = "https://api.themoviedb.org/3/search/tv"
    
    def search_show_by_name(self, show_name):
        params = {
            "api_key": self.api_key,
            "query": show_name
        }
        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            return results   
        else:
            return []
    
    def search_show_cli(self):
        tv_show_query = str(input("Search for a TV Show: "))
        results = self.search_show_by_name(tv_show_query)
        if results:
            print(f'Search results for "{tv_show_query}"')
        else:
            print("No results found or API error occurred")
        return results

    def show_numbered_list(self, shows):
        """Display numbered list of shows"""
        for i, show in enumerate(shows, 1):
            name = show.get("name")
            first_air_date = show.get("first_air_date", "")
            year = first_air_date[:4] if first_air_date else "N/A"
            print(f"{i}. {name} ({year})")
        
    def select_show(self, shows):
        """Get user selection from the displayed show list"""
        while True:
            try:
                choice = int(input(f"\nSelect a show (1-{len(shows)}): ")) - 1
            except ValueError:
                print("Please enter a valid number.")
                continue  # Skip to next iteration
            
            if 0 <= choice < len(shows):
                return shows[choice]    
            
            print("Invalid selection. Please try again.")
            
    def get_id(self, show_choice):
            id = show_choice.get("id")
            return id
            # print(id)
            
    def select_season(self):
        """Get user selection of Season number"""
        # TODO: Prompt user to choose Season number
        return True
    
    def query_show(self):
        results = self.search_show_cli()
        self.show_numbered_list(results)
        selected_show = self.select_show(results)
        show_id = self.get_id(selected_show)
        return show_id

def main():
    query = QueryShow()
    show_id = query.query_show()

if __name__ == "__main__":
    main()




