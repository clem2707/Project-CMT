import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# Lire le fichier CSV
file_name = "temperature_data/geneve.csv"  # Remplacez par le chemin vers votre fichier
df = pd.read_csv(file_name, quotechar='"')

# Renommer les colonnes pour enlever les guillemets inversés
df.columns = df.columns.str.replace('`', '')

# Convertir la colonne 'date' au format datetime
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', errors='coerce')

# Convertir la colonne 'temperature' en float
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')

# Ajouter des colonnes pour la semaine de l'année et l'heure
df['week_of_year'] = df['date'].dt.isocalendar().week
df['hour'] = df['date'].dt.hour
df['year'] = df['date'].dt.year  # Extraire l'année

# Calculer la moyenne hebdomadaire pour chaque année
weekly_avg = df.groupby(['year', 'week_of_year', 'hour'])['temperature'].mean().reset_index()

# Entraîner le modèle sur les données d'entraînement (sans 2024)
train_data = weekly_avg[weekly_avg['year'] != 2024]
weeks_train = train_data[['week_of_year', 'hour']].values  # X (semaine et heure)
temps_train = train_data['temperature'].values  # y (température)

# Régression polynomiale : ajuster un modèle polynomial de degré 4
poly = PolynomialFeatures(degree=4)  # Degree 4 pour une courbe plus souple
weeks_train_poly = poly.fit_transform(weeks_train)  # Transformer les semaines et heures en polynôme
model = LinearRegression()
model.fit(weeks_train_poly, temps_train)

def predict_temperature(date_str):
    # Convertir la date en datetime
    date = pd.to_datetime(date_str, format='%d/%m/%Y %H:%M', errors='coerce')
    if date is pd.NaT:
        return None
    
    # Extraire la semaine de l'année et l'heure de la date
    week_of_year = date.isocalendar().week
    hour = date.hour
    
    # Transformer la semaine et l'heure en polynôme
    week_hour_poly = poly.transform(np.array([[week_of_year, hour]]))
    
    # Prédire la température
    predicted_temp = model.predict(week_hour_poly)
    
    return predicted_temp[0]

# Prédire la température pour la date "15/07/2024 14:00"
date_future = "15/09/2024 03:00"
predicted_temp_future = predict_temperature(date_future)

if predicted_temp_future is not None:
    print(f"La température prédite pour le {date_future} est de {predicted_temp_future:.2f}°C")
else:
    print("Date invalide. Veuillez entrer une date au format 'dd/mm/yyyy HH:MM'.")

# Comparer avec la vraie valeur et calculer les erreurs

# Filtrer les données pour obtenir la vraie valeur de température pour "15/07/2024 14:00"
true_temp_future_data = df[(df['date'] == pd.to_datetime(date_future, format='%d/%m/%Y %H:%M'))]

if not true_temp_future_data.empty:
    true_temp_future = true_temp_future_data['temperature'].values[0]

    # Convertir les valeurs en numériques explicitement pour éviter l'erreur de type 'numeric' incompatible avec les tableaux de bytes/strings.
    true_temp_future_numeric = np.array([true_temp_future], dtype=np.float64)
    predicted_temp_future_numeric = np.array([predicted_temp_future], dtype=np.float64)

    # Calculer les erreurs MSE et MAE pour cette prédiction unique
    mse_future = mean_squared_error(true_temp_future_numeric, predicted_temp_future_numeric)
    mae_future = mean_absolute_error(true_temp_future_numeric, predicted_temp_future_numeric)

    print(f"Température réelle pour le {date_future} : {true_temp_future:.2f}°C")
    print(f"Erreur quadratique moyenne (MSE) pour la prédiction : {mse_future:.2f}")
    print(f"Erreur absolue moyenne (MAE) pour la prédiction : {mae_future:.2f}")
else:
    print(f"Aucune donnée réelle disponible pour le {date_future}.")