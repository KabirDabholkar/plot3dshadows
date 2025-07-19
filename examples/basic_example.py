#!/usr/bin/env python3
"""
Basic example demonstrating the Plot3DShadows package.

This example shows how to create a simple 3D plot with shadows
projected onto coordinate planes.
"""

import matplotlib.pyplot as plt
import numpy as np
from plot3dshadows import Plot3DShadows

def main():
    # Set up the plot
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-5, 5)
    ax.grid(False)
    ax.view_init(elev=30)
    ax.set_axis_off()

    # Create the Plot3DShadows object with custom shadow positions
    plotter = Plot3DShadows(
        ax, 
        shadow_alpha_ratio=0.14, 
        shadow_planes=['xy', 'yz'],
        shadow_positions={
            'xy': 'min', 
            'yz': 'min'
        }
    )
    
    # Generate some sample data
    t = np.linspace(0, 4*np.pi, 100)
    x = np.cos(t)
    y = np.sin(t)
    z = t / (4*np.pi)
    
    # Plot a 3D spiral (shadows will be plotted later)
    plotter.plot(x, y, z, color='blue', linewidth=2, label='3D Spiral')
    
    # Add some scatter points (shadows will be plotted later)
    n_points = 20
    scatter_x = np.random.randn(n_points)
    scatter_y = np.random.randn(n_points)
    scatter_z = np.random.randn(n_points)
    
    plotter.scatter(scatter_x, scatter_y, scatter_z, color='red', s=50, label='Random Points')
    
    # Now plot all shadows at the current axis limits
    plotter.plot_shadows()
    plotter.plot_planes()
    plotter.plot_axes(partial=0.5)
    
    # Set labels and title
    plotter.set_labels('X', 'Y', 'Z')
    
    plt.tight_layout()
    plt.savefig('test_plots/basic_example.png', dpi=100, bbox_inches='tight')

if __name__ == "__main__":
    main() 