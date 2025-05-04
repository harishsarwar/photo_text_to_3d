"""
Module for converting text descriptions to 3D models.
"""
import logging
import os
import numpy as np
import trimesh
from trimesh.creation import box, cylinder, capsule, cone, icosphere
from trimesh.transformations import translation_matrix

logger = logging.getLogger(__name__)

# Dictionary of primitive shapes and their parameters
PRIMITIVE_SHAPES = {
    "cube": box,
    "box": box,
    "cylinder": cylinder,
    "capsule": capsule,
    "cone": cone,
    "sphere": icosphere
}

def convert_text_to_model(text_prompt, output_path, format="obj"):
    """
    Convert a text description to a 3D model.
    
    Args:
        text_prompt (str): Text description of the object
        output_path (str): Path to save the output 3D model
        format (str): Output format, either 'obj' or 'stl'
        
    Returns:
        str: Path to the generated 3D model if successful, None otherwise
    """
    try:
        # Parse the text prompt to determine shape and parameters
        logger.info(f"Parsing text prompt: '{text_prompt}'")
        shape_info = parse_text_prompt(text_prompt)
        
        # Generate the 3D model
        logger.info(f"Generating 3D model for: {shape_info['shape']}")
        mesh = generate_shape_mesh(shape_info)
        
        # Save the mesh to file
        logger.info(f"Saving model to {output_path}")
        if format.lower() == "obj":
            mesh.export(output_path, file_type="obj")
        else:
            mesh.export(output_path, file_type="stl")
            
        return output_path
        
    except Exception as e:
        logger.error(f"Error converting text to model: {str(e)}")
        return None

def parse_text_prompt(text_prompt):
    """
    Parse the text prompt to determine the shape and parameters.
    
    This is a simplified parser that tries to identify:
    1. The basic shape (cube, sphere, cylinder, etc.)
    2. Size adjectives (small, large, tiny, etc.)
    
    Args:
        text_prompt (str): Text description of the object
        
    Returns:
        dict: Dictionary containing shape information
    """
    text = text_prompt.lower()
    
    # Default shape is a cube if none is specified
    shape_info = {
        "shape": "cube",
        "scale": 1.0,
    }
    
    # Try to identify a primitive shape
    for shape_name in PRIMITIVE_SHAPES.keys():
        if shape_name in text:
            shape_info["shape"] = shape_name
            break
    
    # Adjust scale based on size adjectives
    if any(adj in text for adj in ["small", "tiny", "little"]):
        shape_info["scale"] = 0.5
    elif any(adj in text for adj in ["large", "big", "huge"]):
        shape_info["scale"] = 2.0
    
    # Look for specific objects and map them to shapes
    if "car" in text:
        shape_info["shape"] = "capsule"
        shape_info["custom"] = "car"
    elif "ball" in text or "sphere" in text:
        shape_info["shape"] = "sphere"
    elif "bottle" in text:
        shape_info["shape"] = "cylinder"
        shape_info["height"] = 2.0
        shape_info["radius"] = 0.5
    
    return shape_info

def generate_shape_mesh(shape_info):
    """
    Generate a 3D mesh based on the shape information.
    
    Args:
        shape_info (dict): Dictionary containing shape information
        
    Returns:
        trimesh.Trimesh: The generated 3D mesh
    """
    shape = shape_info["shape"]
    scale = shape_info.get("scale", 1.0)
    
    # Handle custom objects
    if "custom" in shape_info:
        if shape_info["custom"] == "car":
            return create_simple_car(scale)
    
    # Generate basic primitive shape
    if shape in PRIMITIVE_SHAPES:
        shape_func = PRIMITIVE_SHAPES[shape]
        
        if shape == "box" or shape == "cube":
            extents = [1.0, 1.0, 1.0]
            if "width" in shape_info:
                extents[0] = shape_info["width"]
            if "height" in shape_info:
                extents[1] = shape_info["height"]
            if "depth" in shape_info:
                extents[2] = shape_info["depth"]
                
            return shape_func(extents=np.array(extents) * scale)
        
        elif shape == "cylinder" or shape == "cone":
            height = shape_info.get("height", 1.0) * scale
            radius = shape_info.get("radius", 0.5) * scale
            return shape_func(height=height, radius=radius)
        
        elif shape == "sphere":
            radius = shape_info.get("radius", 0.5) * scale
            return shape_func(radius=radius, subdivisions=2)
        
        elif shape == "capsule":
            height = shape_info.get("height", 1.0) * scale
            radius = shape_info.get("radius", 0.5) * scale
            return shape_func(height=height, radius=radius)
    
    # Default to a cube if shape not recognized
    logger.warning(f"Shape '{shape}' not recognized, using cube as default")
    return box(extents=[1.0, 1.0, 1.0] * scale)

def create_simple_car(scale=1.0):
    """
    Create a simple car model from primitive shapes.
    
    Args:
        scale (float): Scale factor for the car
        
    Returns:
        trimesh.Trimesh: The car mesh
    """
    # Create the car body (box)
    body = box(extents=[2.0, 1.0, 0.5] * scale)
    
    # Create the car cabin (another box)
    cabin = box(extents=[1.0, 0.8, 0.4] * scale)
    cabin.apply_transform(translation_matrix([0.2, 0, 0.45] * scale))
    
    # Create wheels (cylinders)
    wheel_radius = 0.25 * scale
    wheel_height = 0.1 * scale
    
    # Positions for the four wheels
    wheel_positions = [
        [-0.5, -0.6, -0.2],  # front-left
        [-0.5, 0.6, -0.2],   # front-right
        [0.8, -0.6, -0.2],   # rear-left
        [0.8, 0.6, -0.2]     # rear-right
    ]
    
    wheels = []
    for pos in wheel_positions:
        wheel = cylinder(radius=wheel_radius, height=wheel_height)
        wheel.apply_transform(translation_matrix(np.array(pos) * scale))
        wheels.append(wheel)
    
    # Combine all parts
    car = trimesh.util.concatenate([body, cabin] + wheels)
    return car