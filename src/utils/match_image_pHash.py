"""
Perceptual Hash Image Matching
"""
import cv2
import numpy as np
import imagehash
from PIL import Image

class PerceptualHashMatcher:
    def __init__(self, hash_size=8): # 8 x 8 grid, 64 bit length
        self.hash_size = hash_size
    
    def preprocess_image(self, image):
        # Check if image is 3-channel BGR image (from OpenCV)
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image
        # Convert OpenCV format to PIL Image object
        return Image.fromarray(image_rgb)
    
    def calculate_hash(self, image, method='phash'):
        if isinstance(image, np.ndarray):
            pil_image = self.preprocess_image(image)
        else:
            pil_image = image
        
        if method == 'phash': # Perceptual hash: DCT Transform
            return imagehash.phash(pil_image, hash_size=self.hash_size)
        elif method == 'ahash': # Average hash: brightness patterns
            return imagehash.average_hash(pil_image, hash_size=self.hash_size)
        elif method == 'dhash': # Difference hash: more robust ahash
            return imagehash.dhash(pil_image, hash_size=self.hash_size)
        elif method == 'whash': # Wavelet hash: for color features
            return imagehash.whash(pil_image, hash_size=self.hash_size)
        else:
            raise ValueError(f"Unknown hash method: {method}")
    
    def compare_hashes(self, hash1, hash2):
        # Compute bitwise XOR of two hashes then count set bits
        hamming_distance = hash1 - hash2
        max_distance = self.hash_size * self.hash_size # 64 bits
        return hamming_distance / max_distance
    
    def match_images(self, image1, image2, method='phash'):
        hash1 = self.calculate_hash(image1, method)
        hash2 = self.calculate_hash(image2, method)
        return self.compare_hashes(hash1, hash2)
    
    # For comparing several DB thumbnails to each video sample frame
    def find_best_match(self, query_image, reference_images, method='phash'):
        query_hash = self.calculate_hash(query_image, method)
        similarities = []
        
        for ref_image in reference_images:
            ref_hash = self.calculate_hash(ref_image, method)
            similarity = self.compare_hashes(query_hash, ref_hash)
            similarities.append(similarity)
        
        best_match_index = np.argmin(similarities)
        best_similarity = similarities[best_match_index]
        
        return best_match_index, best_similarity, similarities

def load_and_match_images(image_path1, image_path2, method='phash'):
    img1 = cv2.imread(image_path1)
    img2 = cv2.imread(image_path2)
    
    # Check if images load correctly
    if img1 is None:
        raise ValueError(f"Could not load image: {image_path1}")
    if img2 is None:
        raise ValueError(f"Could not load image: {image_path2}")
    
    matcher = PerceptualHashMatcher()
    return matcher.match_images(img1, img2, method)

if __name__ == "__main__":
    # Works with or without quotes surrounding file path
    image1_path = input("Enter path to first image: ").strip().strip('"')
    image2_path = input("Enter path to second image: ").strip().strip('"')
    
    try:
        similarity = load_and_match_images(image1_path, image2_path)
        print(f"Similarity: {similarity:.4f}")
        
        if similarity < 0.3:
            print("Likely match")
        elif similarity < 0.5:
            print("Possibly related")
        else:
            print("Different images")
            
    except Exception as e:
        print(f"Error: {e}")