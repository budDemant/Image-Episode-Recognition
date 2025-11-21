import cv2
import os
#TODO: sample first few seconds for title cards
#TODO: the first minutes should be evaluated differently (for intros)
def sample_frames(video_path, output_dir, interval_seconds=5):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_seconds)
    
    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_count % frame_interval == 0:
            timestamp = frame_count / fps
            filename = f"frame_{saved_count:04d}_{timestamp:.1f}s.jpg"
            cv2.imwrite(os.path.join(output_dir, filename), frame)
            saved_count += 1
            
        frame_count += 1
    
    cap.release()
    return saved_count

def main():
    #TODO: handle invalid input
    video_path = input("Video Path: ")
    output_dir = input("Output Directory: ")
    sample_frames(video_path, output_dir, 5)

if __name__ == "__main__":
    main()
