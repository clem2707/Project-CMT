import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

def display_stat(predicted_data_path, interior_points_path, path_results):
    """
    Visualization of Lake Geneva
    This function takes as input: the paths of the predicted temperatures made in step 2 and the interior points of the lake made in step 1 and a location to save the map.
    The goals of this function are: to display our temperature prediction results and to go further by performing interpolation.

    First, we load our 2 CSVs, extract the data we need: coordinates and predicted temperatures.
    Then, we start the interpolation by building a k-d tree. This will allow us to quickly find the nearest neighbors of a given point.
    Next, we estimate a temperature for each point contained in the lake using an interpolation based on a weighted average of the nearest neighbors of the points.
    Finally, we adjust a temperature scale so that the visualization is correct.
    We end by displaying our results on the map.
    """

    # Load and read the CSV data created previously (predicted temperatures + points inside the lake)
    predicted_data = pd.read_csv(predicted_data_path)
    interior_points = pd.read_csv(interior_points_path)

    # Extract coordinates and temperatures from predicted data
    predicted_points = predicted_data[['x', 'y']].values
    temperatures = predicted_data['predicted_temperature'].values

    # Build a k-d tree for the predicted points
    tree = cKDTree(predicted_points)

    # Define a maximum distance for interpolation
    max_distance = 0.2  # It considers neighbors of the point up to 2km

    # Initialize an array to store interpolated temperatures
    interior_temperatures = []

    # Loop to calculate interpolated temperatures for each interior point
    for x, y in interior_points[['x', 'y']].values:
        # Perform neighbor search using the k-d tree
        distances, indices = tree.query([x, y], k=len(temperatures), distance_upper_bound=max_distance)
        valid = distances < max_distance
        weights = 1 / distances[valid]
        interpolated_temp = np.sum(weights * temperatures[indices[valid]]) / np.sum(weights)
        
        # Add the interpolated temperature to the array
        interior_temperatures.append(interpolated_temp)

    # Convert the list of interpolated temperatures to a numpy array
    interior_temperatures = np.array(interior_temperatures)

    # Add interpolated temperatures to interior points
    interior_points['interpolated_temperature'] = interior_temperatures

    # Define temperature scale limits (min and max temperatures)
    vmin = min(temperatures.min(), interior_temperatures.min())
    vmax = max(temperatures.max(), interior_temperatures.max())
    # Expand the temperature scale by increasing the range by 10%
    range_diff = vmax - vmin
    vmin -= 0.05 * range_diff  # reduce lower limit by 5%
    vmax += 0.05 * range_diff  # increase upper limit by 5%

    # XY Graph
    # Predicted points
    sc_predicted = plt.scatter(predicted_data['x'], predicted_data['y'], c=temperatures, cmap='coolwarm', edgecolors='white', s=100, label='Predicted Data Points')

    # Interior points
    sc_interior = plt.scatter(interior_points['x'], interior_points['y'], c=interior_points['interpolated_temperature'], cmap='coolwarm', s=10, label="Interior Points")

    # Color scale
    plt.colorbar(sc_interior, label='Temperature (°C)', extend='both')
    sc_predicted.set_clim(vmin, vmax)
    sc_interior.set_clim(vmin, vmax)

    plt.xlabel('Longitude (x)')
    plt.ylabel('Latitude (y)')
    plt.title('Interpolated Temperature Map for Interior Points of Lake Geneva')
    plt.legend()

# Example usage of the function
display_stat("internal/Lake_pred2024.csv", "internal/interior_points.csv", "results/Lake_pred2024.png")
display_stat("internal/Lake_reel2024.csv", "internal/interior_points.csv", "results/Lake_reel2024.png")