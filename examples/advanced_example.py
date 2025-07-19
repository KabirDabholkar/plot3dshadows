#!/usr/bin/env python3
"""
Advanced example demonstrating advanced features of the Plot3DShadows package.

This example shows:
- Custom shadow configurations
- Multiple data types
- Dynamic shadow position updates
- Coordinate planes and axes
"""

import matplotlib.pyplot as plt
import numpy as np
from plot3dshadows import Plot3DShadows

def main():
    # Set up the plot
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-5, 5)
    ax.grid(False)
    ax.view_init(elev=13, azim=30)
    ax.set_axis_off()

    # Create the Plot3DShadows object with advanced configuration
    plotter = Plot3DShadows(
        ax, 
        shadow_alpha_ratio=0.1,
        shadow_planes=['xy', 'xz', 'yz'],
        shadow_positions={
            'xy': 'min',  # Bottom plane
            'xz': 'min',  # Side plane  
        }
    )
    
    # Generate multiple types of data
    np.random.seed(42)
    
    # 1. Spiral data
    t = np.linspace(0, 6*np.pi, 200)
    spiral_x = 2 * np.cos(t)
    spiral_y = 2 * np.sin(t)
    spiral_z = t / (6*np.pi) * 6 - 3
    
    # 2. Random scatter points
    n_points = 30
    scatter_x = np.random.uniform(-2, 2, n_points)
    scatter_y = np.random.uniform(-2, 2, n_points)
    scatter_z = np.random.uniform(-2, 2, n_points)
    
    # 3. Surface-like data (points on a surface)
    u = np.linspace(-2, 2, 20)
    v = np.linspace(-2, 2, 20)
    U, V = np.meshgrid(u, v)
    surface_x = U
    surface_y = V
    surface_z = 0.5 * np.sin(U) * np.cos(V)
    
    # Plot the spiral with custom shadow alpha
    plotter.plot(spiral_x, spiral_y, spiral_z, 
                color='blue', linewidth=3, 
                shadow_alpha_ratio=0.1, label='Spiral')
    
    # Plot scatter points with different shadow alpha
    plotter.scatter(scatter_x, scatter_y, scatter_z, 
                   color='red', s=80, alpha=0.8,
                   shadow_alpha_ratio=0.2, label='Random Points')
    
    # Plot surface points
    plotter.scatter(surface_x.flatten(), surface_y.flatten(), surface_z.flatten(),
                   color='green', s=20, alpha=0.6,
                   shadow_alpha_ratio=0.1, label='Surface Points')
    
    # Plot shadows
    plotter.plot_shadows()
    
    # Add coordinate axes and planes
    plotter.plot_axes(partial=1.0)
    plotter.plot_planes()
    
    # Set labels and title
    plotter.set_labels('X Axis', 'Y Axis', 'Z Axis')
    
    # Demonstrate dynamic shadow position update
    print("Original shadow positions:", plotter.shadow_positions)
    
    # Update shadow positions
    # plotter.set_shadow_positions({'xy': 'max'})
    print("Updated shadow positions:", plotter.shadow_positions)
    
    plt.tight_layout()
    plt.savefig('test_plots/advanced_example.png', dpi=150, bbox_inches='tight')

if __name__ == "__main__":
    main() 