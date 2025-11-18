from src.episode_recognizer import EpisodeRecognizer
from src.rename_file import rename_file
from src.query_show import QueryShow


def main():
    recognizer = EpisodeRecognizer()
    query = QueryShow()
    
    video_path = input("Enter path to video file: ").strip().strip('"')
    show_id = query.query_show()
    season_number = int(input("Enter season number: "))
    
    result = recognizer.recognize_episode(video_path, show_id, season_number)
    
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