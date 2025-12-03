"""Multiprocessing for videos"""
from multiprocessing import Pool, cpu_count
from .episode_recognizer import EpisodeRecognizer


def process_single_video(args):
    """Worker function for multiprocessing"""
    video_path, show_id, season_number, episode_images = args
    recognizer = EpisodeRecognizer()
    result = recognizer.recognize_episode(
        video_path, show_id, season_number, episode_images=episode_images
    )
    return (video_path, result)


def process_videos(video_paths, show_id, season_number, episode_images):
    """Process multiple videos using multiprocessing if needed"""
    if len(video_paths) > 1:
        with Pool(processes=cpu_count()) as pool:
            results = pool.map(
                process_single_video,
                [(video_path, show_id, season_number, episode_images)
                 for video_path in video_paths]
            )
    else:
        results = [process_single_video((video_paths[0], show_id, season_number, episode_images))]
    
    return results
