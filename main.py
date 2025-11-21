from src.episode_recognizer import EpisodeRecognizer
from src.rename_file import rename_file
from src.query_show import QueryShow
from src.episode_image_fetcher import EpisodeImageFetcher
import os
from multiprocessing import Pool, cpu_count

def process_single_video(args):
    """Worker function for multiprocessing"""
    video_path, show_id, season_number, episode_images = args
    recognizer = EpisodeRecognizer()
    result = recognizer.recognize_episode(video_path, show_id, season_number,
                                         episode_images=episode_images)
    return (video_path, result)

def get_video_paths():
    '''Get video filepath(s) from user input'''
    while True:
        path = input ("Enter path to video file or folder (or 'q' to quit): ").strip().strip('"')
        
        if path.lower() == 'q':
            return None
        if os.path.isfile(path):
            return [path]
        elif os.path.isdir(path):
            videos = [os.path.join(path, f) for f in os.listdir(path)
                           if f.endswith(('.mkv', '.mp4', '.avi'))]
            if videos:
                return videos
            print("No video files found in folder.")
        else:
            print ("Invalid path. Please try again.")

def main():
    query = QueryShow()
    
    # Get video paths
    video_paths = get_video_paths()
    if not video_paths:
        return
    
    # Get show info
    show_id = query.query_show()
    season_number = int(input("Enter season number: "))
    
    # Fetch episode images per season
    print("Downloading episode images from TMDB...")
    fetcher = EpisodeImageFetcher()
    episode_images, images_temp_dir = fetcher.fetch_season_images(show_id, season_number)
    
    try:
        # Process videos
        if len(video_paths) > 1:
            with Pool(processes=cpu_count()) as pool:
                results = pool.map(process_single_video,
                                   [(video_path, show_id, season_number, episode_images)
                                    for video_path in video_paths])
        else:
            results = [process_single_video((video_paths[0], show_id, season_number, 
                                             episode_images))]

        # Display results
        for video_path, result in results:
            if result and "error" not in result:
                print(f"\n=== RECOGNITION RESULT ===")
                print(f"Episode: {result['episode_number']} - {result['episode_name']}")
                print(f"Confidence: {result['confidence']:.3f}")
                print(f"Similarity Score: {result['similarity_score']:.3f}")
                print(f"Good Matches: {result['good_matches']}")
                print(f"High Confidence: {result['is_confident']}")
                
                rename_file(video_path, season_number, result['episode_number'], 
                            result['episode_name'], style='human')
            else:
                print(f"Recognition failed for {os.path.basename(video_path)}: {result}")
    finally:
        # Cleanup episode images temp directory
        fetcher.cleanup_temp_files(images_temp_dir)

if __name__ == "__main__":
    main()
    
