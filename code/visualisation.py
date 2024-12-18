import matplotlib.pyplot as plt
import csv
import numpy as np

# Chemin vers le fichier CSV
csv_eaux_vives_2024 = "internal/Eaux-vives_temperatures_2024.csv"
csv_predic_stat_eaux_vives_2024 = "internal/predicted_temperatures_annual_predictions.csv"
csv_data_eaux_vives_2024 = "datas/temperature_per_year/geneve.csv"

# Initialiser les listes pour stocker les données
days = []
temp_warming_noise_extreme_inertia_currents = []
temp_predic_stat = []
filtered_data = []

# Lecture du fichier CSV
with open(csv_eaux_vives_2024, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    headers = next(reader)  # Lire la première ligne (en-têtes)
    
    for row in reader:
        # Extraire les colonnes
        days.append(int(row[0]))  # Première colonne : jours
        temp_warming_noise_extreme_inertia_currents.append(float(row[5]))  # Sixième colonne : temp_warming_noise_extreme_inertia_currents

with open(csv_predic_stat_eaux_vives_2024, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    headers = next(reader)  # Lire la première ligne (en-têtes)
    
    for row in reader:
        # Extraire les colonnes
        temp_predic_stat.append(float(row[2]))  # Sixième colonne : temp_warming_noise_extreme_inertia_currents

with open(csv_data_eaux_vives_2024, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    headers = next(reader)  # Lire la première ligne (en-têtes)
    
    for row in reader:
        if '2024' in row[1]:
            filtered_data.append(row)        # Extraire les colonnes

temp = [row[3] for row in filtered_data]
print(temp)
# Conversion en float
float_temperatures = [float(tempe) for tempe in temp]

# Afficher la liste des températures en float
print(float_temperatures)

i = 0
somme = 0.0
liste_moy = []
longueur = len(float_temperatures)
for t in range(longueur):
        if i % 8 != 0:
            somme += float_temperatures[t]
            i += 1
        else:
            moy = somme / 8
            liste_moy.append(moy)
            print(moy,t/8)
            somme = float_temperatures[t]
            i += 1
print(liste_moy)
print(temp_warming_noise_extreme_inertia_currents)
print(temp_predic_stat)
liste_moy_adjust = liste_moy[1:]
print(liste_moy_adjust)
print(len(liste_moy_adjust))


# Création d'un axe X pour chaque liste
x1 = np.arange(1, 366)  # Axe X pour les deux premières listes (1 à 365)
x2 = np.arange(1, 367)
x3 = np.arange(1, 327)  # Axe X pour la troisième liste (1 à 325)

# Tracer les deux premières listes sous forme de courbes
plt.plot(x1, temp_warming_noise_extreme_inertia_currents, label="Liste 1 (365 valeurs)", color='b')
plt.plot(x2, temp_predic_stat, label="Liste 2 (366 valeurs)", color='r')

# Tracer la troisième liste sous forme de points
plt.scatter(x3, liste_moy_adjust, label="Liste 3 (325 valeurs)", color='g')

# Ajouter des étiquettes et un titre
plt.xlabel("Jour")
plt.ylabel("Valeur")
plt.title("Graphique des 3 listes (2 courbes et 1 scatter)")

# Ajouter une légende
plt.legend()

# Afficher le graphique
plt.show()
