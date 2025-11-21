"""
Episode Recognition System
Combines video frame sampling with TMDB episode image matching
"""
import tempfile
from pathlib import Path
import cv2
import numpy as np

from .sample_frame import sample_frames
from .match_image_pHash import PerceptualHashMatcher
from .episode_image_fetcher import EpisodeImageFetcher

class EpisodeRecognizer:
    def __init__(self):
        self.fetcher = EpisodeImageFetcher()
        self.matcher = PerceptualHashMatcher()
        self.temp_dirs = []  # Track temp directories for cleanup
    
    def recognize_episode(self, video_path, tv_id, season_number, confidence_threshold=0.3, episode_images=None):
        """
        Main function to identify which episode a video represents
        
        Args:
            video_path: Path to the video file
            tv_id: TMDB TV show ID
            season_number: Season number to compare against
            confidence_threshold: Similarity threshold for matches
            episode_images: Optional pre-fetched episode images dict to reuse
            
        Returns:
            dict: Best match information including episode number, name, and confidence
        """
        try:
            # Sample frames from video
            video_temp_dir = tempfile.mkdtemp(prefix="video_frames_")
            self.temp_dirs.append(video_temp_dir)
            
            print("Extracting frames from video...")
            frame_count = sample_frames(video_path, video_temp_dir, interval_seconds=10)
            print(f"Extracted {frame_count} frames")

            # Download episode images (skip if already provided)
            if episode_images is None:
                print("Downloading episode images from TMDB...")
                episode_images, images_temp_dir = self.fetcher.fetch_season_images(tv_id, season_number)
                self.temp_dirs.append(images_temp_dir)
            
            # Load video frames
            video_frames = self._load_video_frames(video_temp_dir)
            
            # Find best matches
            print("Comparing frames with episode images...")
            best_match = self._find_best_episode_match(video_frames, episode_images, confidence_threshold)
            
            return best_match
            
        except Exception as e:
            print(f"Error during episode recognition: {e}")
            return None
        finally:
            self._cleanup_temp_files()
    
    def _load_video_frames(self, frames_dir):
        """Load all sampled video frames"""
        frames = []
        frames_path = Path(frames_dir)
        
        for frame_file in sorted(frames_path.glob("*.jpg")):
            frame = cv2.imread(str(frame_file))
            if frame is not None:
                frames.append(frame)
        
        return frames
    
    def _find_best_episode_match(self, video_frames, episode_images, threshold):
        """
        Compare video frames against all episode images to find best match
        Uses a scoring system that considers multiple frame matches per episode
        """
        episode_scores = {}
        
        # For each episode, calculate similarity scores
        for ep_num, ep_data in episode_images.items():
            episode_name = ep_data["name"]
            ep_image_paths = ep_data["images"]
            
            if not ep_image_paths:
                continue
            
            # Load episode images
            ep_images = []
            for img_path in ep_image_paths:
                img = cv2.imread(img_path)
                if img is not None:
                    ep_images.append(img)
            
            if not ep_images:
                continue
            
            # Score this episode against all video frames
            episode_similarities = []
            
            for video_frame in video_frames:
                # Find best match for this frame among episode images
                _, best_similarity, all_similarities = self.matcher.find_best_match(
                    video_frame, ep_images, method='phash'
                )
                episode_similarities.append(best_similarity)
            
            # Calculate episode score (multiple strategies possible)
            # Strategy 1: Best single frame match
            best_frame_match = min(episode_similarities) if episode_similarities else 1.0
            
            # Strategy 2: Average of top 3 matches
            top_matches = sorted(episode_similarities)[:3]
            avg_top_matches = np.mean(top_matches) if top_matches else 1.0
            
            # Strategy 3: Count of good matches
            good_matches = sum(1 for sim in episode_similarities if sim < threshold)
            
            episode_scores[ep_num] = {
                "name": episode_name,
                "best_match": best_frame_match,
                "avg_top_3": avg_top_matches,
                "good_matches_count": good_matches,
                "total_comparisons": len(episode_similarities)
            }
            
            print(f"Episode {ep_num} ({episode_name}): "
                  f"best={best_frame_match:.3f}, "
                  f"avg_top3={avg_top_matches:.3f}, "
                  f"good_matches={good_matches}")
        
        # Determine best episode using combined scoring
        if not episode_scores:
            return {"error": "No episode images found for comparison"}
        
        # Primary: best single match, Secondary: good matches count
        best_episode = min(episode_scores.items(), 
                          key=lambda x: (x[1]["best_match"], -x[1]["good_matches_count"]))
        
        ep_num, scores = best_episode
        confidence = 1.0 - scores["best_match"]  # Convert distance to confidence
        
        return {
            "episode_number": ep_num,
            "episode_name": scores["name"],
            "confidence": confidence,
            "similarity_score": scores["best_match"],
            "good_matches": scores["good_matches_count"],
            "is_confident": scores["best_match"] < threshold
        }
    
    def _cleanup_temp_files(self):
        """Clean up all temporary directories"""
        for temp_dir in self.temp_dirs:
            try:
                import shutil
                shutil.rmtree(temp_dir)
                print(f"Cleaned up: {temp_dir}")
            except Exception as e:
                print(f"Error cleaning {temp_dir}: {e}")
        self.temp_dirs.clear()

    