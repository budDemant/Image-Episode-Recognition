from episode_recognizer import EpisodeRecognizer
from rename_file import rename_file

def main():
    recognizer = EpisodeRecognizer()
    
    video_path = input("Enter path to video file: ").strip().strip('"')
    tv_id = int(input("Enter TMDB TV show ID: "))
    season_number = int(input("Enter season number: "))
    
    result = recognizer.recognize_episode(video_path, tv_id, season_number)
    
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
        print(f"Recognition failed: {result}")

if __name__ == "__main__":
    main()