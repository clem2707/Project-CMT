import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error


# Lire le fichier CSV
file_name = "temperature_data/geneve.csv"  # Remplacez par le chemin vers votre fichier
df = pd.read_csv(file_name, quotechar='"')

# Renommer les colonnes pour enlever les guillemets inversés
df.columns = df.columns.str.replace('`', '')

# Vérifier les noms des colonnes après la modification
print(df.columns)

# Convertir la colonne 'date' au format datetime
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', errors='coerce')

# Convertir la colonne 'temperature' en float
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')

# Ajouter une colonne 'week_of_year' pour grouper par semaine
df['week_of_year'] = df['date'].dt.isocalendar().week
df['year'] = df['date'].dt.year  # Extraire l'année

# Calculer la moyenne hebdomadaire pour chaque année
weekly_avg = df.groupby(['year', 'week_of_year'])['temperature'].mean().reset_index()

# Masquer les données de 2024 pour évaluer le modèle
train_data = weekly_avg[weekly_avg['year'] != 2024]
test_data = weekly_avg[weekly_avg['year'] == 2024]

# Entraîner le modèle sur les données d'entraînement (sans 2024)
weeks_train = train_data['week_of_year'].values.reshape(-1, 1)  # X (semaine)
temps_train = train_data['temperature'].values  # y (température)

# Régression polynomiale : ajuster un modèle polynomial de degré 3
poly = PolynomialFeatures(degree=3)  # Degree 3 pour une courbe plus souple
weeks_train_poly = poly.fit_transform(weeks_train)  # Transformer les semaines en polynôme
model = LinearRegression()
model.fit(weeks_train_poly, temps_train)

# Prédire les températures pour l'année 2024 (test set)
weeks_test = test_data['week_of_year'].values.reshape(-1, 1)  # Semaines de 2024
weeks_test_poly = poly.transform(weeks_test)  # Transformer les semaines en polynôme
predicted_test = model.predict(weeks_test_poly)

# Comparer les prédictions avec les vraies données de 2024
true_values = test_data['temperature'].values

# Calculer l'erreur quadratique moyenne (MSE) et l'erreur absolue moyenne (MAE)
mse = mean_squared_error(true_values, predicted_test)
mae = mean_absolute_error(true_values, predicted_test)

# Afficher les résultats
print(f"Erreur quadratique moyenne (MSE) : {mse}")
print(f"Erreur absolue moyenne (MAE) : {mae}")

# Tracer les résultats
plt.figure(figsize=(10, 6))
plt.plot(weeks_test, true_values, 'o', label="Données réelles 2024")
plt.plot(weeks_test, predicted_test, '-', label="Prédictions 2024 (régression polynomiale)")
plt.xlabel("Semaine de l'année")
plt.ylabel("Température (°C)")
plt.title("Prédictions vs Réelles pour 2024")
plt.legend()
plt.grid(True)
plt.show()