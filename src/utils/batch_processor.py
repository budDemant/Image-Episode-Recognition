"""
Batch processing utilities for video episode recognition
Handles checkpointing and resume capability for data integrity
"""
import os
import json


def get_checkpoint_path(video_folder):
    """Get checkpoint file path for a video folder"""
    if os.path.isfile(video_folder):
        video_folder = os.path.dirname(video_folder)
    return os.path.join(video_folder, ".episode_recognition_checkpoint.json")


def load_checkpoint(checkpoint_path):
    """Load processed videos from checkpoint file"""
    if os.path.exists(checkpoint_path):
        try:
            with open(checkpoint_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load checkpoint: {e}")
    return {}


def save_checkpoint(checkpoint_path, processed_videos):
    """Save processed videos to checkpoint file"""
    try:
        with open(checkpoint_path, 'w') as f:
            json.dump(processed_videos, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save checkpoint: {e}")


def filter_unprocessed_videos(video_paths, checkpoint_path):
    """
    Filter out already processed videos using checkpoint
    
    Returns:
        tuple: (videos_to_process, processed_videos_dict)
    """
    processed_videos = load_checkpoint(checkpoint_path)
    videos_to_process = [vp for vp in video_paths if vp not in processed_videos]
    
    if len(videos_to_process) < len(video_paths):
        skipped = len(video_paths) - len(videos_to_process)
        print(f"\nResuming from checkpoint: skipping {skipped} already processed video(s)")
    
    return videos_to_process, processed_videos


def save_result_to_checkpoint(checkpoint_path, processed_videos, video_path, result):
    """Save a single video result to checkpoint after successful processing"""
    processed_videos[video_path] = {
        "episode_number": result['episode_number'],
        "episode_name": result['episode_name'],
        "confidence": result['confidence']
    }
    save_checkpoint(checkpoint_path, processed_videos)
