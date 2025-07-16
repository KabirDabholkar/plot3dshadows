import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

class Plot3DShadows:
    """
    A class for 3D plotting with shadows on coordinate planes.
    
    This class wraps a matplotlib 3D axis and provides methods to plot
    3D data with automatic shadows projected onto the coordinate planes.
    """
    
    def __init__(self, ax, shadow_alpha_ratio=0.3, shadow_planes=['xy', 'xz', 'yz'], 
                 shadow_positions={'xy': 'min', 'xz': 'min', 'yz': 'min'}):
        """
        Initialize the Plot3DShadows object.
        
        Parameters:
        -----------
        ax : matplotlib.axes.Axes3D
            The 3D matplotlib axis object
        shadow_alpha_ratio : float, optional
            Ratio to multiply the original alpha by for shadow plots (default: 0.3)
        shadow_planes : list, optional
            List of shadow planes to plot. Options: 'xy', 'xz', 'yz'
            (default: ['xy', 'xz', 'yz'])
        shadow_positions : dict, optional
            Dictionary specifying whether to project shadows at 'min' or 'max' 
            for each plane. Keys: 'xy', 'xz', 'yz'. Values: 'min' or 'max'
            (default: {'xy': 'min', 'xz': 'min', 'yz': 'min'})
        """
        self.ax = ax
        self.shadow_alpha_ratio = shadow_alpha_ratio
        self.shadow_planes = shadow_planes
        self.shadow_positions = shadow_positions
        
        # Store plot data for shadow plotting
        self.scatter_data = []
        self.plot_data = []
        
        # Validate shadow planes
        valid_planes = ['xy', 'xz', 'yz']
        for plane in self.shadow_planes:
            if plane not in valid_planes:
                raise ValueError(f"Invalid shadow plane '{plane}'. Must be one of {valid_planes}")
        
        # Validate shadow positions
        valid_positions = ['min', 'max']
        for plane, position in self.shadow_positions.items():
            if position not in valid_positions:
                raise ValueError(f"Invalid shadow position '{position}' for plane '{plane}'. Must be one of {valid_positions}")
    
    def scatter(self, x, y, z, shadow_alpha_ratio=None, **kwargs):
        """
        Plot 3D scatter points and store data for shadow plotting.
        
        Parameters:
        -----------
        x, y, z : array-like
            Coordinates of the points
        shadow_alpha_ratio : float, optional
            Override the default shadow alpha ratio for this plot
        **kwargs : dict
            Additional arguments passed to ax.scatter
        """
        # Plot the main 3D scatter
        self.ax.scatter(x, y, z, **kwargs)
        
        # Store data for shadow plotting
        self.scatter_data.append({
            'x': np.array(x),
            'y': np.array(y),
            'z': np.array(z),
            'shadow_alpha_ratio': shadow_alpha_ratio,
            'kwargs': kwargs.copy()
        })
    
    def plot(self, x, y, z, shadow_alpha_ratio=None, **kwargs):
        """
        Plot 3D lines and store data for shadow plotting.
        
        Parameters:
        -----------
        x, y, z : array-like
            Coordinates of the line points
        shadow_alpha_ratio : float, optional
            Override the default shadow alpha ratio for this plot
        **kwargs : dict
            Additional arguments passed to ax.plot
        """
        # Plot the main 3D line
        self.ax.plot(x, y, z, **kwargs)
        
        # Store data for shadow plotting
        self.plot_data.append({
            'x': np.array(x),
            'y': np.array(y),
            'z': np.array(z),
            'shadow_alpha_ratio': shadow_alpha_ratio,
            'kwargs': kwargs.copy()
        })
    
    def plot_shadows(self):
        """
        Plot shadows for all accumulated data at the current axis limits.
        """
        # Get current axis limits
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()
        z_min, z_max = self.ax.get_zlim()
        
        # Define shadow plane configurations
        plane_configs = {
            'xy': {'x': lambda x: x, 'y': lambda y: y, 'z': lambda z: np.full_like(z, z_min if self.shadow_positions.get('xy', 'min') == 'min' else z_max)},
            'xz': {'x': lambda x: x, 'y': lambda y: np.full_like(y, y_min if self.shadow_positions.get('xz', 'min') == 'min' else y_max), 'z': lambda z: z},
            'yz': {'x': lambda x: np.full_like(x, x_min if self.shadow_positions.get('yz', 'min') == 'min' else x_max), 'y': lambda y: y, 'z': lambda z: z}
        }
        
        def prepare_shadow_kwargs(data):
            """Prepare kwargs for shadow plotting with proper color and alpha handling."""
            shadow_kwargs = data['kwargs'].copy()
            
            # Get the original alpha from the data
            original_alpha = data['kwargs'].get('alpha', 1.0)
            
            # Calculate shadow alpha using the ratio
            shadow_alpha_ratio = data['shadow_alpha_ratio'] if data['shadow_alpha_ratio'] is not None else self.shadow_alpha_ratio
            shadow_alpha = original_alpha * shadow_alpha_ratio
            
            shadow_kwargs['alpha'] = shadow_alpha
            
            # Handle color properly - remove 'c' if it exists and use 'color'
            if 'c' in shadow_kwargs:
                shadow_kwargs['color'] = shadow_kwargs.pop('c')
            else:
                shadow_kwargs['color'] = shadow_kwargs.get('color', 'gray')
            return shadow_kwargs
        
        def plot_shadow_for_data(data, plot_func):
            """Plot shadows for a single data item."""
            shadow_kwargs = prepare_shadow_kwargs(data)
            
            for plane in self.shadow_planes:
                if plane in plane_configs:
                    config = plane_configs[plane]
                    x_coords = config['x'](data['x'])
                    y_coords = config['y'](data['y'])
                    z_coords = config['z'](data['z'])
                    plot_func(x_coords, y_coords, z_coords, **shadow_kwargs)
        
        # Plot shadows for scatter data
        for data in self.scatter_data:
            plot_shadow_for_data(data, self.ax.scatter)
        
        # Plot shadows for plot data
        for data in self.plot_data:
            plot_shadow_for_data(data, self.ax.plot)
    
    def set_labels(self, xlabel='X', ylabel='Y', zlabel='Z'):
        """
        Set axis labels for the 3D plot.
        
        Parameters:
        -----------
        xlabel, ylabel, zlabel : str
            Labels for the respective axes
        """
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)
        self.ax.set_zlabel(zlabel)
    
    def set_title(self, title):
        """
        Set the title for the 3D plot.
        
        Parameters:
        -----------
        title : str
            Title for the plot
        """
        self.ax.set_title(title)
    
    def set_shadow_positions(self, shadow_positions):
        """
        Update shadow positions for each plane.
        
        Parameters:
        -----------
        shadow_positions : dict
            Dictionary specifying whether to project shadows at 'min' or 'max' 
            for each plane. Keys: 'xy', 'xz', 'yz'. Values: 'min' or 'max'
        """
        # Validate shadow positions
        valid_positions = ['min', 'max']
        for plane, position in shadow_positions.items():
            if position not in valid_positions:
                raise ValueError(f"Invalid shadow position '{position}' for plane '{plane}'. Must be one of {valid_positions}")
        
        self.shadow_positions.update(shadow_positions)

    def plot_axes(self, partial=1):
        """
        Plot the axes for the 3D plot.
        
        Parameters:
        -----------
        partial : float
            Fraction to shorten the axes by (default: 1)
        """
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()
        z_min, z_max = self.ax.get_zlim()
        
        # Define origin point and deviations
        origin = [x_min, y_min, z_min]
        x_dev = [partial * (x_max - x_min), 0, 0]
        y_dev = [0, partial * (y_max - y_min), 0] 
        z_dev = [0, 0, partial * (z_max - z_min)]
        
        # Plot the three axes from origin
        self.ax.plot([origin[0], origin[0] + x_dev[0]], 
                    [origin[1], origin[1] + x_dev[1]], 
                    [origin[2], origin[2] + x_dev[2]], color='black', linewidth=2)
        self.ax.plot([origin[0], origin[0] + y_dev[0]], 
                    [origin[1], origin[1] + y_dev[1]], 
                    [origin[2], origin[2] + y_dev[2]], color='black', linewidth=2)
        self.ax.plot([origin[0], origin[0] + z_dev[0]], 
                    [origin[1], origin[1] + z_dev[1]], 
                    [origin[2], origin[2] + z_dev[2]], color='black', linewidth=2)

    def plot_planes(self):
        """
        Plot the planes for the 3D plot.
        """
        # Plot plane at z_min
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()
        z_min, z_max = self.ax.get_zlim()
        
        xx, yy = np.meshgrid(np.array([x_min, x_max]), np.array([y_min, y_max]))
        zz = np.full_like(xx, z_min)
        self.ax.plot_surface(xx, yy, zz, alpha=0.1, color='gray')

        # Plot plane at x_min
        yy, zz = np.meshgrid(np.array([y_min, y_max]), np.array([z_min, z_max]))
        xx = np.full_like(yy, x_min)
        self.ax.plot_surface(xx, yy, zz, alpha=0.1, color='gray') 