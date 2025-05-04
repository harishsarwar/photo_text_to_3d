"""
Image preprocessing utilities for 3D model generation.
"""
import numpy as np
import cv2
from PIL import Image

def preprocess_image(image, target_size=(256, 256)):
    """
    Preprocess the image for depth estimation.
    
    Args:
        image (PIL.Image): Input image
        target_size (tuple): Target size (width, height) for resizing
        
    Returns:
        numpy.ndarray: Preprocessed image
    """
    # Convert PIL image to numpy array
    img_array = np.array(image)
    
    # Convert to grayscale if image is RGB
    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:
        gray = img_array
    
    # Resize to target size
    resized = cv2.resize(gray, target_size)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)
    
    # Apply adaptive histogram equalization to improve contrast
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(blurred)
    
    return enhanced

def extract_depth_map(image):
    """
    Generate a simple depth map from an image.
    
    For a more accurate depth map, you would typically use a 
    specialized model like MiDaS or other depth estimation networks.
    This is a simplified approach using edge detection and blurring.
    
    Args:
        image (numpy.ndarray): Preprocessed grayscale image
        
    Returns:
        numpy.ndarray: Simple depth map
    """
    # Detect edges using Canny
    edges = cv2.Canny(image, 50, 150)
    
    # Invert edges to get a basic depth map
    depth = 255 - edges
    
    # Apply distance transform to create a gradient from edges
    dist_transform = cv2.distanceTransform(depth, cv2.DIST_L2, 3)
    
    # Normalize the distance transform
    norm_dist = cv2.normalize(dist_transform, None, 0, 255, cv2.NORM_MINMAX)
    
    # Apply Gaussian blur to smooth the depth map
    smooth_depth = cv2.GaussianBlur(norm_dist, (15, 15), 0)
    
    return smooth_depth