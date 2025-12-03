import os
import requests
import tempfile
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class EpisodeImageFetcher:
    def __init__(self):
        self.api_key = os.environ.get("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3"
        self.image_base_url = "https://image.tmdb.org/t/p/w500"  # Medium resolution
        
    def get_season_episodes(self, tv_id, season_number):
        """Fetch all episodes for a specific season"""
        url = f"{self.base_url}/tv/{tv_id}/season/{season_number}"
        params = {"api_key": self.api_key}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get("episodes", [])
        return []
    
    def get_episode_images(self, tv_id, season_number, episode_number):
        """Fetch images for a specific episode"""
        url = f"{self.base_url}/tv/{tv_id}/season/{season_number}/episode/{episode_number}/images"
        params = {"api_key": self.api_key}
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            # 'stills' are scene captures from episodes, so not including posters and related
            return data.get("stills", [])
        return []
    
    def download_image(self, image_path, save_path):
        """Download a single image from TMDB"""
        if not image_path:
            return False
            
        url = f"{self.image_base_url}{image_path}"
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
                return True
        except Exception as e:
            print(f"Error downloading {url}: {e}")
        return False
    
    def fetch_season_images(self, tv_id, season_number, temp_dir=None, fetch_additional_metadata=False):
        """
        Download all episode images for a season
        Returns: dict mapping episode numbers to lists of image file paths
        """
        if temp_dir is None:
            temp_dir = tempfile.mkdtemp(prefix="tmdb_images_")
        
        season_dir = Path(temp_dir) / f"season_{season_number}"
        season_dir.mkdir(parents=True, exist_ok=True)
        
        episodes = self.get_season_episodes(tv_id, season_number)
        episode_images = {}
        
        print(f"Downloading images for {len(episodes)} episodes...")
        
        for episode in episodes:
            ep_num = episode["episode_number"]
            ep_name = episode.get("name", f"Episode {ep_num}")
            
            # Create episode directory
            episode_dir = season_dir / f"episode_{ep_num:02d}"
            episode_dir.mkdir(exist_ok=True)
            
            # Get episode images
            images = self.get_episode_images(tv_id, season_number, ep_num)
            downloaded_paths = []
            
            for i, image in enumerate(images):
                image_path = image.get("file_path")
                if image_path:
                    # Create descriptive filename
                    filename = f"still_{i:02d}.jpg"
                    save_path = episode_dir / filename
                    
                    if self.download_image(image_path, save_path):
                        downloaded_paths.append(str(save_path))
            
            episode_images[ep_num] = {
                "name": ep_name,
                "images": downloaded_paths
            }
            
            if fetch_additional_metadata:
                episode_images[ep_num]["air_date"] = episode.get("air_date", "N/A")
                episode_images[ep_num]["overview"] = episode.get("overview", "N/A")
            
            print(f"Episode {ep_num}: {len(downloaded_paths)} images downloaded")
        
        return episode_images, str(season_dir)
    
    def cleanup_temp_files(self, temp_dir):
        """Remove temporary downloaded images"""
        try:
            shutil.rmtree(temp_dir)
            print(f"Cleaned up temporary files: {temp_dir}")
        except Exception as e:
            print(f"Error cleaning up {temp_dir}: {e}")


if __name__ == "__main__":
    fetcher = EpisodeImageFetcher()
    
    # fetch images for Breaking Bad Season 1
    tv_id = 1396  # Breaking Bad's TMDB ID
    season_number = 1
    
    episode_images, temp_dir = fetcher.fetch_season_images(tv_id, season_number)
    
    print(f"\nDownloaded images stored in: {temp_dir}")
    for ep_num, ep_data in episode_images.items():
        print(f"Episode {ep_num} ({ep_data['name']}): {len(ep_data['images'])} images")
    
    # TODO: cleanup when done or cache for later
    # fetcher.cleanup_temp_files(temp_dir)