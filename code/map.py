import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, Polygon

def map(path_data, path_dest, path_results):
    """
    décrire ce que fait la fonction ici
    """
    print("** #1. Map of GVA Lake **")

    # Charger les données depuis le CSV 
    data = pd.read_csv(path_data, sep=';')  # Spécifier le délimiteur

    # Convertion : str to float 
    data["X_GPS"] = data["X_GPS"].str.replace(',', '.').astype(float)
    data["Y_GPS"] = data["Y_GPS"].str.replace(',', '.').astype(float)

    # Extraire une liste des valeurs des coordonnées (un x et un y pour chaque port)
    harbor_coord = data[["X_GPS", "Y_GPS"]].values

    # Par chance, notre liste est dans l'ordre donc nous utilisons la fonction Polygon() pour relier nos ports
    lake_polygon = Polygon(harbor_coord)

    # Créer des indices qui parcourent les points à l'intérrieur du lac
    x_min, y_min, x_max, y_max = lake_polygon.bounds 
    x_range = np.arange(x_min, x_max, 0.01) # Indice pour les coordonnées de x qui vont de x_min jusqu'à x_max 
    y_range = np.arange(y_min, y_max, 0.01)
    # Nous avons choisi un pas de 100 mètres car notre modèle n'est pas très précis, donc ça ne sert pas d'avoir plus de valeurs

    # On veut remplir le lac de points afin de pouvoir calculer pas la suite leur température 
    # On va crée des objets de type points avec chaque point dans notre lac
    # le but est de pouvoir checker s'ils sont bien contenus dasns notre polygone (lac Leman)
    interior_points = []
    for x in x_range:
        for y in y_range:
            point = Point(x, y)
            if lake_polygon.contains(point):
                interior_points.append((x, y))

    # Création du graphique xy 
    plt.figure(figsize=(10, 6)) # On définit la taille, afin que l'affichage soit beau

    # Affichage des bords du lac
    x, y = lake_polygon.exterior.xy
    plt.plot(x, y, color="blue", label="Lac Léman")

    # Tracer les points à l'intérieur du lac Léman pour visualiser notre pas
    interior_points = np.array(interior_points)
    plt.scatter(interior_points[:, 0], interior_points[:, 1], color="green", s=50, label="Interior Points")

    # Affichage des ports avec des points rouges
    plt.scatter(harbor_coord[:, 0], harbor_coord[:, 1], color="red", label="Harbor") 
    # La colonne 0 représente les coordonnnées x et la colonne 1 les coordonnées y
    # La taille de chaque point est de 50, afin que le lac semble rempli

    # Configurations du graphique
    plt.xlabel("Longitude (x)")
    plt.ylabel("Latitude (y)")
    plt.legend()
    plt.savefig(path_results)
    plt.close()

    # Sauvegarder les points interieurs dans un fichier csv pour pouvoir l'utiliser par la suite
    interior_points_df = pd.DataFrame(interior_points, columns=['x', 'y'])
    print("Interior points of the lake")
    print(interior_points_df.head())
    interior_points_df.to_csv(path_dest, index=False)