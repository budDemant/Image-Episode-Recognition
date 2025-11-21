from src.episode_recognizer import EpisodeRecognizer
from src.rename_file import rename_file
from src.query_show import QueryShow
import os

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
    recognizer = EpisodeRecognizer()
    query = QueryShow()
    
    # Get video paths
    video_paths = get_video_paths()
    if not video_paths:
        return
    
    # Get show info
    show_id = query.query_show()
    season_number = int(input("Enter season number: "))
    
    # Process videos
    results = []
    for video_path in video_paths:
        result = recognizer.recognize_episode(video_path, show_id, season_number)
        results.append((video_path, result))

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

if __name__ == "__main__":
    main()
    
