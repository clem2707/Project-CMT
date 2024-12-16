import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, Polygon

# Charger les données depuis le CSV 
file_harbor = "port copie.csv" 
data = pd.read_csv(file_harbor, sep=';')  # Spécifier le délimiteur

# Converssion : str to float 
data["X_GPS"] = data["X_GPS"].str.replace(',', '.').astype(float)
data["Y_GPS"] = data["Y_GPS"].str.replace(',', '.').astype(float)

# Extraire une liste des valeurs des coordonnées (un x et un y pour chaque port)
harbor_coord = data[["X_GPS", "Y_GPS"]].values

# Par chance, notre liste est dans l'ordre donc nous utilisons la fonction Polygon() pour relier nos ports
lake_polygon = Polygon(harbor_coord)

# Créer des indices qui parcourent les points à l'intérrieur du lac
x_min, y_min, x_max, y_max = lake_polygon.bounds 
x_range = np.arange(x_min, x_max, 0.01) #indice pour les coordonnées de x qui vont de x_min jusqu'à x_max 
y_range = np.arange(y_min, y_max, 0.01)
# nous avons choisi un pas de 100 mètres car notre modèle n'est pas très précis, donc ça ne sert pas d'avoir plus de valeurs

#on veut remplir le lac de points afin de pouvoir calculer pas la suite leur température 
#on va crée des objets de type points avec chaque point dans notre lac
# le but est de pouvoir checker s'ils sont bien contenus dasns notre polygone (lac Leman)
interior_points = []
for x in x_range:
    for y in y_range:
        point = Point(x, y)
        if lake_polygon.contains(point):
            interior_points.append((x, y))

# création du graphique xy 
plt.figure(figsize=(10, 6)) # on définit la taille, afin que l'affichage soit beau
# affichage des ports avec des points rouges
plt.scatter(harbor_coord[:, 0], harbor_coord[:, 1], color="red", label="Harbor")
#affichage des bords du lac
x, y = lake_polygon.exterior.xy
plt.plot(x, y, color="blue", label="Lac Léman")
#harbor_coord_closed = np.append(harbor_coord, [harbor_coord[0]], axis=0)
#plt.plot(harbor_coord_closed[:, 0], harbor_coord_closed[:, 1], color="blue", label="Lac Léman")
# Relier chaque point au suivant dans l'ordre
#for i in range(len(harbor_coord) - 1):
#    plt.plot([harbor_coord[i, 0], harbor_coord[i + 1, 0]], 
#             [harbor_coord[i, 1], harbor_coord[i + 1, 1]], 
#             color="blue")

# Relier le dernier point au premier pour fermer le polygone
#plt.plot([harbor_coord[-1, 0], harbor_coord[0, 0]], 
#         [harbor_coord[-1, 1], harbor_coord[0, 1]], 
#         color="blue")

# Tracer les points à l'intérieur du lac Léman pour visualiser notre pas
interior_points = np.array(interior_points)
plt.scatter(interior_points[:, 0], interior_points[:, 1], color="green", s=1, label="Points à l'intérieur du lac")

# Configurations du graphique
plt.xlabel("Longitude (x)")
plt.ylabel("Latitude (y)")
plt.legend()
plt.grid(True)
plt.show()

# Nombre de points à l'intérieur du polygone
num_points_in_polygon = len(interior_points)
print(f"Nombre de points à l'intérieur du polygone : {num_points_in_polygon}")

# Créer un DataFrame avec les points intérieurs
interior_points_df = pd.DataFrame(interior_points, columns=['x', 'y'])

# Enregistrer le DataFrame dans un fichier CSV
interior_points_df.to_csv('interior_points.csv', index=False)

print("Le fichier 'interior_points.csv' a été créé avec succès.")