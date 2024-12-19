import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, Polygon

def map_lake(path_data, path_dest, path_results):
    """
    ** Map of Lake Geneva **

    The function takes as input: a CSV file containing an ordered list of ports with their xy coordinates, a location to store the interior points of the lake as a CSV file, and a location to save the map.
    The goal is to create a map of the lake to further our predictions and be able to interpolate to predict the temperature at any location.
    We tried many ways to create this map, but the simplest way was to take an ordered list of ports.
    We display these coordinates one by one on an xy graph and then connect each port until we have a closed lake.
    Finally, to facilitate the next steps, we output a list of points contained within this lake with a predefined step size.
    """

    # Load and read the data from the CSV
    data = pd.read_csv(path_data, sep=';')  # The columns in our CSV are separated by ";", so it's essential to specify this

    # Convert: str to float
    data["X_GPS"] = data["X_GPS"].str.replace(',', '.').astype(float)
    data["Y_GPS"] = data["Y_GPS"].str.replace(',', '.').astype(float)

    # Extract a list of coordinate values (one x and one y for each port)
    harbor_coords = data[["X_GPS", "Y_GPS"]].values

    # Fortunately, our list is in order, so we use the Polygon() function to connect our ports
    lake_polygon = Polygon(harbor_coords)

    # Create indices that traverse the points inside the lake
    x_min, y_min, x_max, y_max = lake_polygon.bounds 
    x_range = np.arange(x_min, x_max, 0.01)  # Indices for x coordinates ranging from x_min to x_max
    y_range = np.arange(y_min, y_max, 0.01)
    # We chose a step size that is not too large because our model is not very precise, so there's no need for more values

    # We want to fill the lake with points to later calculate their temperature
    # We will create Point objects with each point in our lake
    # The goal is to verify if they are contained within our polygon (Lake Geneva)
    interior_points = []
    for x in x_range:
        for y in y_range:
            point = Point(x, y)
            if lake_polygon.contains(point):
                interior_points.append((x, y))

    # XY Graph
    # Display the lake borders
    x, y = lake_polygon.exterior.xy
    plt.plot(x, y, color="blue", label="Lake Geneva")

    # Plot the points inside Lake Geneva to visualize our step size
    interior_points = np.array(interior_points)
    plt.scatter(interior_points[:, 0], interior_points[:, 1], color="green", s=2, label="Interior Points")

    # Display the ports with red points
    plt.scatter(harbor_coords[:, 0], harbor_coords[:, 1], color="red", label="Harbors") 
    # Column 0 represents x coordinates and column 1 represents y coordinates
    # The size of each point is 50, so the lake appears filled

    # Graph configurations
    plt.xlabel("Longitude (x)")
    plt.ylabel("Latitude (y)")
    plt.legend()
    plt.savefig(path_results)

    # Save the interior points to a CSV file for later use
    interior_points_df = pd.DataFrame(interior_points, columns=['x', 'y'])
    interior_points_df.to_csv(path_dest, index=False)

# Example usage of the function
map_lake("datas/harbor.csv", "internal/int_points.csv", "results/lake_vide.png")