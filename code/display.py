import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

# Charger les données des CSV des températures prédites et des points à l'intérieur du lac
predicted_data = pd.read_csv("predicted_temperatures.csv")
interior_points = pd.read_csv("interior_points.csv")

# Vérifier et nettoyer les données de température PAS OBLIGATOIRE
#predicted_data.dropna(subset=['predicted_temperature'], inplace=True)
#interior_points.dropna(subset=['x', 'y'], inplace=True)

# Vérifier que les colonnes nécessaires sont présentes PAS OBLIGATOIRE
#required_columns = ['x', 'y', 'predicted_temperature']
#for col in required_columns:
#    if col not in predicted_data.columns:
#        raise ValueError(f"La colonne '{col}' est manquante dans les données prédites.")

# Extraire les coordonnées et les températures des données prédites
predicted_points = predicted_data[['x', 'y']].values
temperatures = predicted_data['predicted_temperature'].values

# Définir une distance maximale pour l'interpolation
max_distance = 0.1  # Ajustez cette valeur selon vos besoins

# Construire un arbre k-d pour les points prédits
tree = cKDTree(predicted_points)

# Fonction pour l'interpolation pondérée par la distance inverse
def idw_interpolation(x, y, tree, temperatures, max_distance):
    distances, indices = tree.query([x, y], k=len(temperatures), distance_upper_bound=max_distance)
    valid = distances < max_distance
    if np.any(valid):
        weights = 1 / distances[valid]
        return np.sum(weights * temperatures[indices[valid]]) / np.sum(weights)
    else:
        return np.nan

# Interpoler les températures pour les points intérieurs
interior_temperatures = np.array([idw_interpolation(x, y, tree, temperatures, max_distance) for x, y in interior_points[['x', 'y']].values])

# Ajouter les températures interpolées aux points intérieurs
interior_points['interpolated_temperature'] = interior_temperatures

# Définir les limites de l'échelle de température
vmin = min(temperatures.min(), interior_temperatures.min())
vmax = max(temperatures.max(), interior_temperatures.max())

# Afficher la carte des températures interpolées avec les points prédits et les points intérieurs du lac Léman
plt.figure(figsize=(10, 6))
sc_predicted = plt.scatter(predicted_data['x'], predicted_data['y'], c=temperatures, cmap='coolwarm', edgecolors='white', s=100, label='Predicted Data Points')
sc_interior = plt.scatter(interior_points['x'], interior_points['y'], c=interior_points['interpolated_temperature'], cmap='coolwarm', s=10, label="Points à l'intérieur du lac")
plt.colorbar(sc_interior, label='Temperature (°C)', extend='both')
sc_predicted.set_clim(vmin, vmax)
sc_interior.set_clim(vmin, vmax)
plt.xlabel('Longitude (x)')
plt.ylabel('Latitude (y)')
plt.title('Interpolated Temperature Map for Interior Points of Lake Léman')
plt.legend()
plt.show()