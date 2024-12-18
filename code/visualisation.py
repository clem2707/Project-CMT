import matplotlib.pyplot as plt
import csv

# Chemin vers le fichier CSV
csv_morges_2024 = "internal/Morges_temperatures_2024.csv"

# Initialiser les listes pour stocker les données
days = []
temp_warming = []
temp_warming_noise = []
temp_warming_noise_extreme = []
temp_warming_noise_extreme_inertia = []
temp_warming_noise_extreme_inertia_currents = []

# Lecture du fichier CSV
with open(csv_morges_2024, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    headers = next(reader)  # Lire la première ligne (en-têtes)
    
    for row in reader:
        # Extraire les colonnes
        days.append(int(row[0]))  # Première colonne : jours
        temp_warming.append(float(row[1]))  # Deuxième colonne : temp_warming
        temp_warming_noise.append(float(row[2]))  # Troisième colonne : temp_warming_noise
        temp_warming_noise_extreme.append(float(row[3]))  # Quatrième colonne : temp_warming_noise_extreme
        temp_warming_noise_extreme_inertia.append(float(row[4]))  # Cinquième colonne : temp_warming_noise_extreme_inertia
        temp_warming_noise_extreme_inertia_currents.append(float(row[5]))  # Sixième colonne : temp_warming_noise_extreme_inertia_currents

# Tracer les températures en fonction des jours
plt.figure(figsize=(10, 6))

plt.plot(days, temp_warming, label="Temp Warming")
plt.plot(days, temp_warming_noise, label="Temp Warming + Noise")
plt.plot(days, temp_warming_noise_extreme, label="Temp Warming + Noise + Extreme Events")
plt.plot(days, temp_warming_noise_extreme_inertia, label="Temp Warming + Noise + Extreme + Inertia")
plt.plot(days, temp_warming_noise_extreme_inertia_currents, label="Temp Warming + Noise + Extreme + Inertia + Currents")

# Ajouter des légendes et des titres
plt.title("Températures à Morges en 2024")
plt.xlabel("Jour")
plt.ylabel("Température (°C)")
plt.legend()
plt.grid(True)

# Afficher le graphique
plt.show()
