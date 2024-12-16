import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Lire le fichier CSV
file_name = "temperature_data/geneve.csv"  # Remplacez par le chemin vers votre fichier

df = pd.read_csv(file_name, quotechar='"')

# Nettoyer les noms de colonnes (supprimer les espaces et les guillemets)
df.columns = df.columns.str.strip().str.replace('`', '')

# Convertir la colonne 'date' au format datetime
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M')

# Convertir la colonne 'temperature' en float
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')

# Ajouter une colonne 'day_of_year' pour grouper par jour
df['day_of_year'] = df['date'].dt.dayofyear
df['year'] = df['date'].dt.year  # Extraire l'année

# Séparer les données en deux ensembles : avant 2024 et 2024
df_before_2024 = df[df['year'] < 2024]
df_2024 = df[df['year'] == 2024]

# Calculer la moyenne journalière pour chaque année avant 2024
daily_avg_before_2024 = df_before_2024.groupby(['year', 'day_of_year'])['temperature'].mean().reset_index()

# Régression polynomiale : ajuster un modèle polynomial de degré 3 (par exemple)
poly = PolynomialFeatures(degree=4)  # Degree 3 pour une courbe plus souple

# Prédictions pour l'année 2024
future_year = 2024
days_future = np.arange(1, 366).reshape(-1, 1)  # Jours 1 à 365 pour l'année future (année non bissextile)
poly_future = poly.fit_transform(days_future)

# Prédire les températures pour l'année 2024 en utilisant les données avant 2024
model = LinearRegression()
model.fit(poly.fit_transform(daily_avg_before_2024['day_of_year'].values.reshape(-1, 1)), daily_avg_before_2024['temperature'])
predicted_future = model.predict(poly_future)

# Tracer les prédictions pour l'année future
plt.figure(figsize=(10, 6))
plt.plot(days_future, predicted_future, label=f"Prédictions {future_year}")

# Calculer la moyenne journalière pour l'année 2024 (vraies valeurs)
daily_avg_2024 = df_2024.groupby(['year', 'day_of_year'])['temperature'].mean().reset_index()

# Tracer les vraies valeurs pour l'année 2024
days_2024 = daily_avg_2024['day_of_year'].values.reshape(-1, 1)
temps_2024 = daily_avg_2024['temperature'].values

plt.plot(days_2024, temps_2024, 'o', label=f"Vraies valeurs {future_year}")

# Régression polynomiale sur les vraies valeurs de 2024
days_poly_2024 = poly.fit_transform(days_2024)
model_2024 = LinearRegression()
model_2024.fit(days_poly_2024, temps_2024)
predicted_poly_2024 = model_2024.predict(days_poly_2024)

plt.plot(days_2024, predicted_poly_2024, '-', label=f"Régression polynomiale {future_year}")

# Ajouter des labels et un titre
plt.xlabel("Jour de l'année")
plt.ylabel("Température moyenne (°C)")
plt.title("Prédiction et régression polynomiale des températures moyennes journalières pour 2024")
plt.legend()
plt.grid(True)
plt.show()