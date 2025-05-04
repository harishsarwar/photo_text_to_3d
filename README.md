# Photo/Text to 3D Model Converter

A simple prototype that converts photos or text descriptions to basic 3D models (.obj or .stl format).

## Features

- Convert a single object image to a 3D model
- Convert a text description to a 3D model
- Output in standard 3D formats (.obj or .stl)
- Simple 3D visualization

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/photo_text_to_3d.git
cd photo_text_to_3d
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

### Converting an image to a 3D model

```
python main.py --image path/to/your/image.jpg --output output/model --format obj --visualize
```

### Converting a text description to a 3D model

```
python main.py --text "A small toy car" --output output/model --format stl --visualize
```

### Command-line arguments

- `--image`: Path to input image file (.jpg, .png)
- `--text`: Text description of object to generate
- `--output`: Output file path without extension (default: "output/model")
- `--format`: Output file format, either "obj" or "stl" (default: "obj")
- `--visualize`: Flag to visualize the generated 3D model

## How It Works

### Image to 3D Conversion
1. Image preprocessing (resize, enhance, grayscale conversion)
2. Depth map estimation using edge detection and distance transforms
3. 3D volume creation from depth map
4. Mesh extraction using marching cubes algorithm

### Text to 3D Conversion
1. Text prompt parsing to identify shape and parameters
2. Generation of 3D mesh using primitive shapes
3. For specific objects (like "car"), construction from multiple primitives

## Limitations

- Image-based conversion uses a simplified depth estimation approach without ML
- Text-based conversion supports only basic primitive shapes and simple objects
- Not suitable for complex or detailed 3D modeling

## Future Improvements

- Integrate ML-based depth estimation models for more accurate image conversion
- Expand text-to-3D capabilities with more object types and properties
- Add texture support for more realistic models

## License

MIT License