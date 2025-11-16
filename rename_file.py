import os


def rename_file(old_path, season_number, episode_number, episode_name, style='db'):
    
    directory, old_filename = os.path.split(old_path) # separate filename from entire path
    name, ext = os.path.splitext(old_filename) # separate extension from filename
    
    if style == 'human':
        new_name = f"Season {season_number} Episode {episode_number} - {episode_name}"
    elif style == 'db':
        new_name = f"S{season_number}E{episode_number}" # Default: TMDB style
        
    new_path = os.path.join(directory, new_name + ext)
    
    try:
        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed '{old_path}' to '{new_path}' successfully.")
    except FileNotFoundError:
        print(f"The file '{old_path}' does not exist.")
    except PermissionError:
        print("Permission denied. Unable to rename the file.")
    except Exception as e:
        print(f"An error occurred: {e}")