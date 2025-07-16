#!/usr/bin/env python3
"""
Tests for the Plot3DShadows package.
"""

import pytest
import numpy as np
import matplotlib.pyplot as plt
from plot3dshadows import Plot3DShadows

class TestPlot3DShadows:
    """Test cases for the Plot3DShadows class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.set_zlim(-5, 5)
        
    def teardown_method(self):
        """Clean up after tests."""
        plt.close(self.fig)
    
    def test_initialization(self):
        """Test basic initialization."""
        plotter = Plot3DShadows(self.ax)
        assert plotter.ax == self.ax
        assert plotter.shadow_alpha_ratio == 0.3
        assert plotter.shadow_planes == ['xy', 'xz', 'yz']
        assert plotter.shadow_positions == {'xy': 'min', 'xz': 'min', 'yz': 'min'}
    
    def test_custom_initialization(self):
        """Test initialization with custom parameters."""
        plotter = Plot3DShadows(
            self.ax,
            shadow_alpha_ratio=0.5,
            shadow_planes=['xy', 'xz'],
            shadow_positions={'xy': 'max', 'xz': 'min'}
        )
        assert plotter.shadow_alpha_ratio == 0.5
        assert plotter.shadow_planes == ['xy', 'xz']
        assert plotter.shadow_positions == {'xy': 'max', 'xz': 'min'}
    
    def test_invalid_shadow_plane(self):
        """Test that invalid shadow planes raise ValueError."""
        with pytest.raises(ValueError, match="Invalid shadow plane"):
            Plot3DShadows(self.ax, shadow_planes=['xy', 'invalid'])
    
    def test_invalid_shadow_position(self):
        """Test that invalid shadow positions raise ValueError."""
        with pytest.raises(ValueError, match="Invalid shadow position"):
            Plot3DShadows(self.ax, shadow_positions={'xy': 'invalid'})
    
    def test_plot_method(self):
        """Test the plot method."""
        plotter = Plot3DShadows(self.ax)
        x = [1, 2, 3]
        y = [1, 2, 3]
        z = [1, 2, 3]
        
        plotter.plot(x, y, z, color='blue')
        assert len(plotter.plot_data) == 1
        assert np.array_equal(plotter.plot_data[0]['x'], np.array(x))
        assert np.array_equal(plotter.plot_data[0]['y'], np.array(y))
        assert np.array_equal(plotter.plot_data[0]['z'], np.array(z))
        assert plotter.plot_data[0]['kwargs']['color'] == 'blue'
    
    def test_scatter_method(self):
        """Test the scatter method."""
        plotter = Plot3DShadows(self.ax)
        x = [1, 2, 3]
        y = [1, 2, 3]
        z = [1, 2, 3]
        
        plotter.scatter(x, y, z, color='red', s=50)
        assert len(plotter.scatter_data) == 1
        assert np.array_equal(plotter.scatter_data[0]['x'], np.array(x))
        assert np.array_equal(plotter.scatter_data[0]['y'], np.array(y))
        assert np.array_equal(plotter.scatter_data[0]['z'], np.array(z))
        assert plotter.scatter_data[0]['kwargs']['color'] == 'red'
        assert plotter.scatter_data[0]['kwargs']['s'] == 50
    
    def test_set_labels(self):
        """Test setting axis labels."""
        plotter = Plot3DShadows(self.ax)
        plotter.set_labels('X Label', 'Y Label', 'Z Label')
        
        assert self.ax.get_xlabel() == 'X Label'
        assert self.ax.get_ylabel() == 'Y Label'
        assert self.ax.get_zlabel() == 'Z Label'
    
    def test_set_title(self):
        """Test setting plot title."""
        plotter = Plot3DShadows(self.ax)
        plotter.set_title('Test Title')
        assert self.ax.get_title() == 'Test Title'
    
    def test_set_shadow_positions(self):
        """Test updating shadow positions."""
        plotter = Plot3DShadows(self.ax)
        new_positions = {'xy': 'max', 'xz': 'min'}
        plotter.set_shadow_positions(new_positions)
        
        assert plotter.shadow_positions['xy'] == 'max'
        assert plotter.shadow_positions['xz'] == 'min'
        assert plotter.shadow_positions['yz'] == 'min'  # unchanged
    
    def test_plot_shadows_no_data(self):
        """Test that plot_shadows works with no data."""
        plotter = Plot3DShadows(self.ax)
        # Should not raise any exceptions
        plotter.plot_shadows()
    
    def test_plot_shadows_with_data(self):
        """Test that plot_shadows works with data."""
        plotter = Plot3DShadows(self.ax)
        x = [1, 2, 3]
        y = [1, 2, 3]
        z = [1, 2, 3]
        
        plotter.plot(x, y, z, color='blue')
        plotter.scatter(x, y, z, color='red')
        
        # Should not raise any exceptions
        plotter.plot_shadows()

if __name__ == "__main__":
    pytest.main([__file__]) 