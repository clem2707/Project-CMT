import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Définition de la fonction pour prédire la température à partir d'une date donnée au format 'dd/mm/yyyy HH:MM'
def predict_temperature(date_str, model, poly):
    # Utile ????
    # Convertir la date en datetime
    date = pd.to_datetime(date_str, format='%d/%m/%Y %H:%M', errors='coerce')
    #est ce que je laisse ou pas ??
    if date is pd.NaT:
        return "Date invalide. Veuillez entrer une date au format 'dd/mm/yyyy HH:MM'."
    
    # Extraire la semaine de l'année et l'heure de la date
    week_of_year = date.isocalendar().week
    hour = date.hour
    
    # Pourquoi semaine???
    # Transformer la semaine et l'heure en polynôme
    week_hour_poly = poly.transform(np.array([[week_of_year, hour]]))
    
    # Prédire la température
    predicted_temp = model.predict(week_hour_poly)
    
    return predicted_temp[0]

# Dossier contenant les fichiers CSV à traiter avec les data des températures du lac depuis 2018
folder_path = "final/temperature_data"  

# Liste pour stocker les résultats
results = []

# On définit déja les coordonnées des coordonnées de la liste de port qui ont des mesures (dans l'ordre)
x_values = [6.606, 6.857,  6.158, 6.172, 6.337, 6.323, 6.54, 6.499, 6.66, 6.241, 6.476, 6.92, 6.241, 6.686, 6.851]  
y_values =[46.403, 46.388, 46.208, 46.276, 46.451, 46.372, 46.506, 46.506, 46.405, 46.378, 46.376, 46.398, 46.301, 46.5, 46.456]

# Parcourir tous les fichiers CSV dans le dossier
for i, file in enumerate(os.listdir(folder_path)):
    #utile le if  ???
    if file.endswith(".csv"):
        file_path = os.path.join(folder_path, file)
        
        # Lire le CSV
        df_csv = pd.read_csv(file_path, quotechar='"')
        
        # On converti dans un format exploitable 
        # Donc en renomant les colonnes pour enlever les guillemets inversés
        df_csv.columns = df_csv.columns.str.replace('`', '')
        
        if 'date' in df_csv.columns:
            # Convertir la colonne 'date' au format datetime
            df_csv['date'] = pd.to_datetime(df_csv['date'], format='%d/%m/%Y %H:%M', errors='coerce')
            
            # Ajouter des colonnes pour la semaine de l'année et l'heure
            df_csv['week_of_year'] = df_csv['date'].dt.isocalendar().week
            df_csv['hour'] = df_csv['date'].dt.hour
            
            # Calculer la moyenne hebdomadaire pour chaque fichier
            weekly_avg_csv = df_csv.groupby(['week_of_year', 'hour'])['temperature'].mean().reset_index()
            
            # Entraîner un modèle spécifique pour chaque fichier
            weeks_train = weekly_avg_csv[['week_of_year', 'hour']].values  # X (semaine et heure)
            temps_train = weekly_avg_csv['temperature'].values  # y (température)
            
            poly = PolynomialFeatures(degree=4)  # Degree 4 pour une courbe plus souple
            weeks_train_poly = poly.fit_transform(weeks_train)  # Transformer les semaines et heures en polynôme
            model = LinearRegression()
            model.fit(weeks_train_poly, temps_train)
            
            # Prédire la température pour la date et heure spécifiques
            predicted_temp = predict_temperature("15/01/2024 14:00", model, poly)
            
            # Sélectionner une paire de coordonnées unique pour chaque fichier
            x = x_values[i % len(x_values)]
            y = y_values[i % len(y_values)]
            
            # Ajouter les résultats pour chaque fichier
            results.append({
                'file_name': file, 
                'date': "15/01/2024 14:00", 
                'predicted_temperature': predicted_temp, 
                'x': x,  # Valeur de 'x'
                'y': y   # Valeur de 'y'
            })
        else:
            print(f"Le fichier {file} ne contient pas de colonne 'date'.")

# Créer un DataFrame à partir des résultats et l'enregistrer dans un nouveau fichier CSV
results_df = pd.DataFrame(results)
results_df.to_csv("predicted_temperatures.csv", index=False)

print("Les températures prédites ont été enregistrées dans le fichier 'predicted_temperatures.csv'.")