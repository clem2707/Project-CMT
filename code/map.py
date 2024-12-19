import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, Polygon

def map(path_data, path_dest, path_results):
    """
    ** #1. Map of GVA Lake **

    La fontion prend en input : un csv contenant une liste de ports ordonnée avec leurs coordonnées xy, un endroit pour stocker sous forme csv les points interrieurs du lac et un endroit pour stocker notre carte.
    Le but est de crée une carte du lac afin de pouvoir aller plus loin dans nos prédictions et pouvoir faire une interpolation pour prédire à n'importe quel endroit la température.
    Nous avons essayé beaucoup de manière de faire cette carte, mais le moyen le plus simple a été de prendre une liste de port ordonnée. 
    Nous affichons ces coordonnées une par une sur un graphe xy puis relions chaque port jusqu'à avoir un lac fermé.
    Enfin, pour faciliter la suite, nous en extraiyons en output une liste de point contenu dans ce lac avec un pas prédéfini.
    
    """

    # Charger et lire les données depuis le CSV 
    data = pd.read_csv(path_data, sep=';')  # Les colonne de notre csv sont délimitées par un ";", il est essentiel de le spécifier

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
    # Nous avons choisi un pas pas trop grand car notre modèle n'est pas très précis, donc ça ne sert pas d'avoir plus de valeurs

    # On veut remplir le lac de points afin de pouvoir calculer pas la suite leur température 
    # On va crée des objets de type points avec chaque point dans notre lac
    # le but est de pouvoir vérifier s'ils sont bien contenus dasns notre polygone (lac Leman)
    interior_points = []
    for x in x_range:
        for y in y_range:
            point = Point(x, y)
            if lake_polygon.contains(point):
                interior_points.append((x, y))

    # Graphique xy 
    # Affichage des bords du lac
    x, y = lake_polygon.exterior.xy
    plt.plot(x, y, color="blue", label="Geneva Lake")

    # Tracer les points à l'intérieur du lac Léman pour visualiser notre pas
    interior_points = np.array(interior_points)
    plt.scatter(interior_points[:, 0], interior_points[:, 1], color="green", s=2, label="Interior Points")

    # Affichage des ports avec des points rouges
    plt.scatter(harbor_coord[:, 0], harbor_coord[:, 1], color="red", label="Harbors") 
    # La colonne 0 représente les coordonnnées x et la colonne 1 les coordonnées y
    # La taille de chaque point est de 50, afin que le lac semble rempli

    # Configurations du graphique
    plt.xlabel("Longitude (x)")
    plt.ylabel("Latitude (y)")
    plt.legend()
    plt.savefig(path_results)

    # Sauvegarder les points interieurs dans un fichier csv pour pouvoir l'utiliser par la suite
    interior_points_df = pd.DataFrame(interior_points, columns=['x', 'y'])
    interior_points_df.to_csv(path_dest, index=False)
map("datas/harbor.csv", "internal/int_points.csv", "results/lake_vide.png")