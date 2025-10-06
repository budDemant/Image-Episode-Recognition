import cv2

def preprocess_for_lbp(image):
    """
    Preprocess image for LBP feature extraction
    """
    # Convert to grayscale
    if len(image.shape) == 3: # if image has color channel
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image.copy()
    
    #TODO: test other methods like padding/cropping
    # Resize to standard dimensions (area-based interpolation best for downscalling)
    target_size = (256, 256) # Square works well with LBP
    resized = cv2.resize(gray, target_size, interpolation=cv2.INTER_AREA)
    
    # CLAHE histogram equalization (for consistent contrast)
    equalized = cv2.equalizeHist(resized)
    
    #TODO: Test with and without noise reduction
    # Noise reduction (from video compression artifacts)
    denoised = cv2.GaussianBlur(equalized, (3, 3), 0.5)
    
    return denoised