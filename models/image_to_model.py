"""
Module for converting images to 3D models.
"""
import logging
import numpy as np
import trimesh
from PIL import Image
from skimage import measure
from utils.preprocessing import preprocess_image, extract_depth_map

logger = logging.getLogger(__name__)

def convert_image_to_model(image_path, output_path, format="obj"):
    """
    Convert an image to a 3D model.
    
    Args:
        image_path (str): Path to the input image
        output_path (str): Path to save the output 3D model
        format (str): Output format, either 'obj' or 'stl'
        
    Returns:
        str: Path to the generated 3D model if successful, None otherwise
    """
    try:
        # Load and preprocess the image
        logger.info("Loading and preprocessing image...")
        image = Image.open(image_path)
        processed_image = preprocess_image(image)
        
        # Generate a depth map from the processed image
        logger.info("Generating depth map...")
        depth_map = extract_depth_map(processed_image)
        
        # Create a 3D volume from the depth map
        logger.info("Creating 3D volume...")
        volume = create_volume_from_depth(depth_map)
        
        # Extract mesh using marching cubes algorithm
        logger.info("Extracting mesh with marching cubes...")
        verts, faces, _, _ = measure.marching_cubes(volume, level=0.5)
        
        # Create and save the mesh
        logger.info(f"Creating and saving {format} file...")
        mesh = trimesh.Trimesh(vertices=verts, faces=faces)
        
        if format.lower() == "obj":
            mesh.export(output_path, file_type="obj")
        else:
            mesh.export(output_path, file_type="stl")
            
        return output_path
        
    except Exception as e:
        logger.error(f"Error converting image to model: {str(e)}")
        return None

def create_volume_from_depth(depth_map, thickness=10):
    """
    Create a 3D volume from a depth map.
    
    Args:
        depth_map (numpy.ndarray): The depth map
        thickness (int): The thickness of the 3D model
        
    Returns:
        numpy.ndarray: 3D volume representation
    """
    height, width = depth_map.shape
    # Normalize depth values to range [0, 1]
    depth_norm = (depth_map - np.min(depth_map)) / (np.max(depth_map) - np.min(depth_map))
    
    # Create 3D volume
    volume = np.zeros((height, width, thickness))
    
    # Fill the volume based on depth values
    for i in range(height):
        for j in range(width):
            # Calculate how deep to fill based on depth
            fill_depth = int(depth_norm[i, j] * (thickness - 1))
            volume[i, j, 0:fill_depth+1] = 1.0
    
    return volume