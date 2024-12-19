import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

def display_stat(predicted_data_path, interior_points_path, path_results):
    """
    #3. Visualization of GVA Lake
    Cette fontion prend en input : les chemins des températures prédites faites au point 2 et des points interrieurs du lac fait au point 1. 
    Les buts de cette fonction est : d'afficher nos résultats de prédictions de températures et d'aller plus loin en faisant une interpolation.

    Tout d'abord, on charge nos 2 csv, on extrait les données dont on va avoir besoin : les coordonnées et les températures prédites.
    Puis, on débute l'interpolation en construisant un arbre k-d. Celui-ci va permettre de retrouver rapidement les voisins les plus proches d'un point donné.
    Ensuite, nous estimons une température pour chaques point contenu dans le lac, grâce à une interpolation qui se base sur une moyenne pondérée des voisins les plus proches du points. 
    Pour finir, nous adaptons une échelle de température afin que la visualisation soit correcte.
    On finit par afficher nos résultats sur la carte. 
    
    """

    # Charger et lire les données les CSV crés précedemment (températures prédites +  points à l'intérieur du lac)
    predicted_data = pd.read_csv(predicted_data_path)
    interior_points = pd.read_csv(interior_points_path)

    # Extraire les coordonnées et les températures des données prédites
    predicted_points = predicted_data[['x', 'y']].values
    temperatures = predicted_data['predicted_temperature'].values

    # Construire un arbre k-d pour les points prédits
    tree = cKDTree(predicted_points)

    # Définir une distance maximale pour l'interpolation
    max_distance = 0.2 # Il prend en compte les voisins du points qui sont jusqu'à 2km

    # Initialiser un tableau pour stocker les températures interpolées
    interior_temperatures = []

    # Boucle pour calculer les températures interpolées pour chaque point intérieur
    for x, y in interior_points[['x', 'y']].values:
        # Effectuer la recherche des voisins à partir du k-d tree
        distances, indices = tree.query([x, y], k=len(temperatures), distance_upper_bound=max_distance)
        valid = distances < max_distance
        weights = 1 / distances[valid]
        interpolated_temp = np.sum(weights * temperatures[indices[valid]]) / np.sum(weights)
        
        # Ajouter la température interpolée au tableau
        interior_temperatures.append(interpolated_temp)

    # Convertir la liste des températures interpolées en tableau numpy
    interior_temperatures = np.array(interior_temperatures)

    # Ajouter les températures interpolées aux points intérieurs
    interior_points['interpolated_temperature'] = interior_temperatures

    # Définir les limites de l'échelle de température (min et max des températures)
    vmin = min(temperatures.min(), interior_temperatures.min())
    vmax = max(temperatures.max(), interior_temperatures.max())
    # Agrandir l'échelle de température en augmentant la plage de 10%
    range_diff = vmax - vmin
    vmin -= 0.05 * range_diff  # réduire la limite inférieure de 5%
    vmax += 0.05 * range_diff  # augmenter la limite supérieure de 5%

    # Graph xy
    # Points prédits
    sc_predicted = plt.scatter(predicted_data['x'], predicted_data['y'], c=temperatures, cmap='coolwarm', edgecolors='white', s=100, label='Predicted Data Points')

    # Points intérieurs
    sc_interior = plt.scatter(interior_points['x'], interior_points['y'], c=interior_points['interpolated_temperature'], cmap='coolwarm', s=10, label="Points à l'intérieur du lac")

    # Echelle de couleur
    plt.colorbar(sc_interior, label='Temperature (°C)', extend='both')
    sc_predicted.set_clim(vmin, vmax)
    sc_interior.set_clim(vmin, vmax)

    plt.xlabel('Longitude (x)')
    plt.ylabel('Latitude (y)')
    plt.title('Interpolated Temperature Map for Interior Points of Geneva Lake')
    plt.legend()


display_stat("internal/Lake_pred2024.csv", "internal/interior_points.csv", "results/Llake_pred2024.png")
display_stat("internal/Lake_reel2024.csv", "internal/interior_points.csv", "results/LAke_reel2024.png")
