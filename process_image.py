import cv2

def preprocess_for_lbp(image):
    """
    Preprocess image for LBP feature extraction (FIXED VERSION)
    """
    # Convert to grayscale
    if len(image.shape) == 3: # if image has color channel
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    # Resize to standard dimensions (area-based interpolation best for downscaling)
    target_size = (256, 256) # Square works well with LBP
    resized = cv2.resize(gray, target_size, interpolation=cv2.INTER_AREA)
    
    # could be resulting in false positives
    # equalized = cv2.equalizeHist(resized)
    
    # Light noise reduction only (from video compression artifacts)
    denoised = cv2.GaussianBlur(resized, (3, 3), 0.5)
    
    return denoised

def main():
    image_path = input("Enter an image path: ")
    image = cv2.imread(image_path)
    
    # Check if image was loaded successfully
    if image is None:
        print(f"Error: Could not load image from {image_path}")
        return
    
    processed_image = preprocess_for_lbp(image)
    
    # Saves the processed image in the same parent directory as the input
    import os
    input_dir = os.path.dirname(image_path)
    input_filename = os.path.basename(image_path)
    name, ext = os.path.splitext(input_filename)
    
    # Create output filename with "_processed" suffix
    output_filename = f"{name}_processed{ext}"
    output_path = os.path.join(input_dir, output_filename)
    
    # Save the processed image
    success = cv2.imwrite(output_path, processed_image)
    if success:
        print(f"Processed image saved to: {output_path}")
    else:
        print(f"Error: Failed to save processed image to {output_path}")
    
if __name__ == "__main__":
    main()
    
    