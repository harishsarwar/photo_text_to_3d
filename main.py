"""
Main entry point for the Photo/Text to 3D Model Converter application.
"""
import os
import argparse
import logging
from pathlib import Path

from models.image_to_model import convert_image_to_model
from models.text_to_model import convert_text_to_model
from utils.visualization import visualize_model

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_directories():
    """Create necessary directories if they don't exist."""
    os.makedirs("output", exist_ok=True)

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Convert a photo or text to a 3D model")
    
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("--image", type=str, help="Path to input image file (.jpg, .png)")
    input_group.add_argument("--text", type=str, help="Text description of object to generate")
    
    parser.add_argument("--output", type=str, default="output/model", 
                      help="Output file path (without extension)")
    parser.add_argument("--format", type=str, choices=["obj", "stl"], default="obj",
                      help="Output file format (obj or stl)")
    parser.add_argument("--visualize", action="store_true", 
                      help="Visualize the generated 3D model")
    
    return parser.parse_args()

def main():
    """Main function to run the application."""
    setup_directories()
    args = parse_arguments()
    
    output_path = f"{args.output}.{args.format}"
    
    # Process according to input type
    if args.image:
        if not os.path.exists(args.image):
            logger.error(f"Image file not found: {args.image}")
            return
        
        logger.info(f"Converting image {args.image} to 3D model")
        model_path = convert_image_to_model(args.image, output_path, format=args.format)
    else:
        logger.info(f"Converting text prompt '{args.text}' to 3D model")
        model_path = convert_text_to_model(args.text, output_path, format=args.format)
    
    if model_path:
        logger.info(f"3D model saved to {model_path}")
        
        if args.visualize:
            visualize_model(model_path)
    else:
        logger.error("Failed to generate 3D model")

if __name__ == "__main__":
    main()