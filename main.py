from src.episode_recognizer import EpisodeRecognizer
from src.rename_file import rename_file
from src.query_show import QueryShow
from src.episode_image_fetcher import EpisodeImageFetcher
from src.batch_processor import (
    get_checkpoint_path,
    filter_unprocessed_videos,
    save_result_to_checkpoint
)
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
    
    # Setup checkpoint for batch processing
    checkpoint_path = get_checkpoint_path(video_paths[0])
    videos_to_process, processed_videos = filter_unprocessed_videos(video_paths, checkpoint_path)
    
    if not videos_to_process:
        print("All videos already processed!")
        return
    
    # Fetch episode images per season
    print("Downloading episode images from TMDB...")
    fetcher = EpisodeImageFetcher()
    episode_images, images_temp_dir = fetcher.fetch_season_images(show_id, season_number)
    
    try:
        # Process videos
        if len(videos_to_process) > 1:
            with Pool(processes=cpu_count()) as pool:
                results = pool.map(process_single_video,
                                   [(video_path, show_id, season_number, episode_images)
                                    for video_path in videos_to_process])
        else:
            results = [process_single_video((videos_to_process[0], show_id, season_number, 
                                             episode_images))]

        # Display and save results incrementally
        for video_path, result in results:
            if result and "error" not in result:
                print(f"\n=== RECOGNITION RESULT: {os.path.basename(video_path)} ===")
                print(f"Episode: {result['episode_number']} - {result['episode_name']}")
                print(f"Confidence: {result['confidence']:.3f}")
                print(f"Similarity Score: {result['similarity_score']:.3f}")
                print(f"Good Matches: {result['good_matches']}")
                print(f"High Confidence: {result['is_confident']}")
                
                rename_file(video_path, season_number, result['episode_number'], 
                            result['episode_name'], style='human')
                
                # Save to checkpoint after successful processing
                save_result_to_checkpoint(checkpoint_path, processed_videos, video_path, result)
            else:
                print(f"\nRecognition failed for {os.path.basename(video_path)}: {result}")
        
        print(f"\nBatch processing complete. Checkpoint saved to {checkpoint_path}")
    finally:
        # Cleanup episode images temp directory
        fetcher.cleanup_temp_files(images_temp_dir)

if __name__ == "__main__":
    main()
    
