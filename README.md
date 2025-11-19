# Image-Based Episode Recognition from Unlabeled or Poorly Named Video Content

This project demonstrates a computer vision system for identifying and labeling video episodes based on visual similarity to known reference images (e.g., stills). The goal is to automate metadata recovery and organization for large media collections with incomplete or missing episode information.

## Project Overview
- **Input:**
  - Video file(s) (e.g., .mkv) with unknown episode label
- **Output:**
  - The best-matching season-episode number and episode name for each video file

## How It Works
1. **Frame Extraction:**
   - Samples frames from each video file at regular intervals (e.g., every 5 seconds).
2. **Image Preprocessing:**
   - Preprocesses both video frames and image stills (resize, grayscale, etc.) for robust comparison.
3. **Image Matching:**
   - Compares each sampled frame to the set of image stills using an image similarity method (pHash or CNN).
   - Selects the reference image with the highest match score.
   - Works even if only a portion of the episode is available, as long as it includes or resembles the image still frame.
4. **Result Reporting:**
   - Outputs the season-episode number and episode name for each video file or segment.

## Technologies Used
- Python 3
- Requests
- OpenCV (for image and video processing)
- NumPy
- TheMovieDB API
- Imagehash
- PIL
- (Potential Extension) deep learning libraries for advanced matching

## Setup Instructions

### Prerequisites
- Python 3.7 or higher installed on your system
- Git installed

### 1. Clone the Repository
```bash
git clone https://github.com/budDemant/Image-Episode-Recognition.git
cd Image-Episode-Recognition
```

### 2. Create a Virtual Environment (Recommended)

A virtual environment keeps this project's dependencies isolated from other Python projects.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install Dependencies

Install the runtime dependencies:

```bash
pip install -r requirements.txt
```

### 4. Run the Program

```bash
python main.py
```


## Getting Started
1. Launch the application.
2. Upload a video file you wish to identify.
3. Enter a TV show (name and year released).
4. Enter the Season number.
5. The best-matching episode name and number will be displayed.

## Potential Extensions
- Batch process entire seasons
- Create GUI for media selection
- Use advanced scene detection, deep learning, or other image matching methods (ORB, CLIP, etc.) for improved accuracy
- Support for partial video files or clips
- Rename/Generate metadata for uploaded file(s) automatically
- Apply system to identify other media domains (movies, games, etc.)

## License
MIT License

---

This project is inspired by the need to organize and identify video episodes from collections with incomplete metadata, using computer vision techniques. All examples and documentation use public domain or open-access content to ensure ethical and legal compliance. This product uses the TMDB API but is not endorsed or certified by TMDB.
