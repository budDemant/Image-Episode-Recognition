# Image-Based Episode Recognition from Unlabeled or Poorly Named Video Content

This project demonstrates a computer vision system for identifying and labeling video episodes based on visual similarity to known reference images (e.g., thumbnails). The goal is to automate metadata recovery and organization for large media collections with incomplete or missing episode information.

## Project Overview
- **Input:**
  - Video file(s) (e.g., .mkv) with unknown or partial episode label
- **Output:**
  - The best-matching episode name and number for each video file

## How It Works
1. **Frame Extraction:**
   - Samples frames from each video file at regular intervals (e.g., every 10 seconds).
2. **Image Preprocessing:**
   - Preprocesses both video frames and thumbnails (resize, grayscale, etc.) for robust comparison.
3. **Image Matching:**
   - Compares each sampled frame to the set of thumbnails using an image similarity method (e.g. LBP-based feature extraction and histogram comparison, deep learning-based feature extraction using CNN, etc. ).
   - Selects the reference image with the highest match score.
   - Works even if only a portion of the episode is available, as long as it includes or resembles the thumbnail.
4. **Result Reporting:**
   - Outputs the episode name and number for each video file or segment.

## Technologies Used
- Python 3
- OpenCV (for image and video processing)
- NumPy
- TheMovieDB
- (Potential Extension) scikit-image, deep learning libraries for advanced matching

## Getting Started
1. Launch the application.
2. Upload a video file you wish to identify.
3. Enter a TV show (name and year released).
4. The best-matching episode name and number will be displayed.


## Potential Extensions
- Batch process entire seasons
- Create GUI for media selection
- Use advanced scene detection, deep learning, or other image matching methods (ORB, CLIP, pHash, etc.) for improved accuracy
- Return a confidence score
- Support for partial video files or clips
- Rename/Generate metadata for uploaded file(s) automatically
- Apply system to identify other media domains (movies, games, etc.)
- Support for various file types (.mp4, .avi, .mov, etc.)

## License
MIT License

---

This project is inspired by the need to organize and identify video episodes from collections with incomplete metadata, using computer vision techniques. All examples and documentation use public domain or open-access content to ensure ethical and legal compliance. This product uses the TMDB API but is not endorsed or certified by TMDB.
