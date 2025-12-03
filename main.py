from multiprocessing import freeze_support
from src.utils.rename_file import rename_file
from src.utils.query_show import QueryShow
from src.utils.episode_image_fetcher import EpisodeImageFetcher
from src.utils.batch_processor import (
    get_checkpoint_path,
    filter_unprocessed_videos,
    save_result_to_checkpoint
)
from src.utils.video_processor import process_videos
from src.utils.user_interface import get_video_paths, display_result


def main():
    # Get user input for video file path
    video_paths = get_video_paths()
    if not video_paths:
        return
    
    # Prompt user for show name and season number
    query = QueryShow()
    show_id = query.query_show()
    season_number = int(input("Enter season number: "))
    
    # Ask if user wants additional metadata
    fetch_metadata = input("Do you want to fetch and display additional metadata? (y/n): ").strip().lower() == 'y'
    
    # Setup checkpoint for batch processing
    checkpoint_path = get_checkpoint_path(video_paths[0])
    videos_to_process, processed_videos = filter_unprocessed_videos(
        video_paths, checkpoint_path
    )
    
    if not videos_to_process:
        print("All videos already processed!")
        return
    
    # Fetch episode images
    print("Downloading episode images from TMDB...")
    fetcher = EpisodeImageFetcher()
    episode_images, images_temp_dir = fetcher.fetch_season_images(show_id, season_number, fetch_additional_metadata=fetch_metadata)
    
    try:
        # Multiprocessing for folders
        results = process_videos(videos_to_process, show_id, season_number, episode_images)
        
        # Display and save results
        for video_path, result in results:
            if display_result(video_path, result):
                rename_file(
                    video_path, season_number, result['episode_number'],
                    result['episode_name'], style='human'
                )
                save_result_to_checkpoint(checkpoint_path, processed_videos, video_path, result)
        
        print(f"\nBatch processing complete. Checkpoint saved to {checkpoint_path}")
    finally:
        fetcher.cleanup_temp_files(images_temp_dir)

if __name__ == "__main__":
    freeze_support()  # for multiprocessing with PyInstaller
    main()
    
