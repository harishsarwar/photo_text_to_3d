"""
Utilities for visualizing 3D models.
"""
import logging
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import trimesh

logger = logging.getLogger(__name__)

def visualize_model(model_path):
    """
    Visualize a 3D model using matplotlib.
    
    Args:
        model_path (str): Path to the 3D model file (.obj or .stl)
    """
    try:
        # Load the mesh
        mesh = trimesh.load(model_path)
        
        # Get vertices and faces
        vertices = mesh.vertices
        faces = mesh.faces
        
        # Create a 3D plot
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot the triangular mesh
        ax.plot_trisurf(
            vertices[:, 0], vertices[:, 1], vertices[:, 2],
            triangles=faces,
            cmap='viridis',
            alpha=0.5,
            edgecolor='k',
            linewidth=0.2
        )
        
        # Set equal aspect ratio
        ax.set_box_aspect([1, 1, 1])
        
        # Set labels and title
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'3D Model Visualization: {model_path}')
        
        # Show the plot
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        logger.error(f"Error visualizing 3D model: {str(e)}")
        logger.info("Falling back to simple visualization...")
        visualize_simple(model_path)

def visualize_simple(model_path):
    """
    A simpler visualization fallback if the main visualization fails.
    
    Args:
        model_path (str): Path to the 3D model file (.obj or .stl)
    """
    try:
        # Load the mesh
        mesh = trimesh.load(model_path)
        
        # Get vertices and faces
        vertices = mesh.vertices
        
        # Create a 3D plot - simpler version
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        
        # Plot just the vertices as a point cloud
        ax.scatter(
            vertices[:, 0],
            vertices[:, 1],
            vertices[:, 2],
            c='b',
            marker='.',
            s=1
        )
        
        # Set equal aspect ratio
        ax.set_box_aspect([1, 1, 1])
        
        # Set labels and title
        ax.set_title(f'Simple Visualization: {model_path}')
        
        # Show the plot
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        logger.error(f"Simple visualization also failed: {str(e)}")