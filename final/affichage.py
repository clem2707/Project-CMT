import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

# Charger les données de températures prédites
predicted_data = pd.read_csv("predicted_temperatures.csv")

# Charger les points intérieurs du lac Léman
interior_points = pd.read_csv("interior_points.csv")

# Extraire les coordonnées et les températures des données prédites
predicted_points = predicted_data[['x', 'y']].values
temperatures = predicted_data['predicted_temperature'].values

# Définir la grille pour l'interpolation
grid_x, grid_y = np.mgrid[min(interior_points['x']):max(interior_points['x']):100j, min(interior_points['y']):max(interior_points['y']):100j]

# Effectuer l'interpolation linéaire sur la grille
grid_z = griddata(predicted_points, temperatures, (grid_x, grid_y), method='linear')

# Interpoler les températures pour les points intérieurs
interior_temperatures = griddata(predicted_points, temperatures, (interior_points['x'], interior_points['y']), method='linear')

# Afficher la carte des températures interpolées avec les points prédits et les points intérieurs du lac Léman
plt.figure(figsize=(12, 10))
plt.imshow(grid_z.T, extent=(min(interior_points['x']), max(interior_points['x']), min(interior_points['y']), max(interior_points['y'])), origin='lower', cmap='coolwarm', alpha=0.6)
plt.colorbar(label='Temperature (°C)')
plt.scatter(predicted_data['x'], predicted_data['y'], c=temperatures, cmap='coolwarm', edgecolors='white', s=100, label='Predicted Data Points')
plt.scatter(interior_points['x'], interior_points['y'], c=interior_temperatures, cmap='coolwarm', s=10, label="Points à l'intérieur du lac")
plt.xlabel('Longitude (x)')
plt.ylabel('Latitude (y)')
plt.title('Interpolated Temperature Map with Lake Léman Points')
plt.legend()
plt.show()

