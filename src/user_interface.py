"""User interface functions for input and output"""
import os


def get_video_paths():
    """Get video filepath(s) from user input"""
    while True:
        path = input("Enter path to video file or folder (or 'q' to quit): ").strip().strip('"')
        if path.lower() == 'q':
            return None
        if os.path.isfile(path):
            return [path]
        elif os.path.isdir(path):
            videos = [
                os.path.join(path, f) for f in os.listdir(path)
                if f.endswith(('.mkv', '.mp4', '.avi'))
            ]
            if videos:
                return videos
            print("No video files found in folder.")
        else:
            print("Invalid path. Please try again.")


def display_result(video_path, result):
    """Display recognition result for a single video"""
    if not result or "error" in result:
        print(f"\nRecognition failed for {os.path.basename(video_path)}: {result}")
        return False
    
    print(f"\n=== RECOGNITION RESULT: {os.path.basename(video_path)} ===")
    print(f"Episode: {result['episode_number']} - {result['episode_name']}")
    if 'air_date' in result:
        print(f"Air Date: {result['air_date']}")
    if 'overview' in result:
        print(f"Synopsis: {result['overview']}")
    print(f"Confidence: {result['confidence']:.3f}")
    print(f"Similarity Score: {result['similarity_score']:.3f}")
    print(f"Good Matches: {result['good_matches']}")
    print(f"High Confidence: {result['is_confident']}")
    return True
