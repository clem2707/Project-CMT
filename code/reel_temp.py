import os
import pandas as pd
from datetime import datetime, timedelta

def reel_temp(folder_path, date_str, path_dest):
    """
    Cette fonction est une fonction inspirée de celles dans "code/predictions_stat.py", elle prend en input : un dossier contenant des fichiers CSV d'archives de températures de chacun des ports du Geneva Lake, une date et un chemin pour stocker ses resultats.
    Le but de cette fonction est d'extraire les données pour une date précise de chaque csv du dossier. 
    Dans le but d'obtenir un csv similaire à celui retourné par la fonction predict_folder.
    Nous allons utiliser les deux csv pour pouvoir comparer avec les vraies valeurs pour analyser la fiabilité de nos prédictions.
    Notre CSV de sortie, contiendra 5 colonnes : nom du port, date, réelle température, coordonnées x et coordonnées y. 
    Avant d'extraire nos températures, nous allons préremplir notre liste de résultats avec les paramètres qui ne changent pas. Ces paramètres sont les coordonnées x et y et on les met sur ce csv afin de faciliter l'étape de la visualisation.
    """
    # Initialiser une liste vide pour stocker les résultats
    results = []

    # On définit déjà les coordonnées des ports qui ont des mesures (dans l'ordre)
    x_values = [6.606, 6.857,  6.158, 6.172, 6.337, 6.323, 6.54, 6.499, 6.66, 6.241, 6.476, 6.92, 6.241, 6.686, 6.851]  
    y_values = [46.403, 46.388, 46.208, 46.276, 46.451, 46.372, 46.506, 46.506, 46.405, 46.378, 46.376, 46.398, 46.301, 46.5, 46.456]

    # Parcourir chaque fichier dans le dossier
    for i, file_name in enumerate(os.listdir(folder_path)):
        if file_name.endswith('.csv'):
            # Construire le chemin complet du fichier
            file_path = os.path.join(folder_path, file_name)
            
            # Lire le fichier CSV dans un DataFrame en utilisant l'encodage ISO-8859-1 pour éviter les erreurs UnicodeDecodeError
            df = pd.read_csv(file_path, encoding='ISO-8859-1')
            df.columns = df.columns.str.replace('`', '')
            
            # Conversion en datetime : la colonne 'date' du csv et la date donnée en paramètre
            df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', errors='coerce')
            date = datetime.strptime(date_str, '%d/%m/%Y')

            # On isole le jour et le mois recherchés afin de faciliter le filtrage du csv
            jour_cible, mois_cible, annee_cible = date.day, date.month, date.year

            # Filtrer les données pour le jour et le mois cible, et créer une copie indépendante afin de ne pas modifier le csv original
            df_flt = df[(df['date'].dt.day == jour_cible) & (df['date'].dt.month == mois_cible) & (df['date'].dt.year == annee_cible)].copy()

            # Calculer la température moyenne pour la date donnée
            temperature = df_flt['temperature'].mean()

            x = x_values[i]
            y = y_values[i]

            # Ajouter le résultat à la liste
            results.append({
                'file_name': file_name,
                'date': date_str,
                'predicted_temperature': temperature,
                'x': x,
                'y': y
            })

    # Création d'un csv, en passant par un dataframe afin que ce soit bien présenté avec le nom des colonness
    # path_dest représente l'endroit ou sera répertorié notre csv
    results_df = pd.DataFrame(results)
    results_df.to_csv(path_dest, index=False)

