import os
import pandas as pd
from datetime import datetime
from sklearn.linear_model import LinearRegression


def pred(folder_path, date_str, path_dest):
    """
    Cette fontion prend en input : un dossier qui contient des archives de températures de chacun des ports du lac leman depuis 2018, une date et un endroit pour stocker sous forme csv les predictions pour chacun des ports.
    Le but de cette fonction est de prédire statistiquement des températures du lac à un endroit précis, c'est à dire en entrainant un model sur les données à disposition.
    La fonction va procédé fichier par fichier, c'est à dire port par port. 

    Elle filtre le csv afin d'avoir toutes les données passée du jour donné. Etant donné qu'on a plusieurs valeurs par jour, elle va faire une moyenne des valeurs par année donc par jour d'une année précise. 
    Ensuite, elle associe à x, une liste des années, qui corresspondent à un y, une liste de températures moyenne pour chaque année.
    Ensuite, la fonction fait un model de régression linéaire qu'elle entraine avec nos x en entrée et y en sortie.
    Et pour finir, utilise le model entrainé afin de prédire une température pour la date demandé.

    La démarche est répétée pour chaque pour et sort un csv final qui contient le nom des ports (nom de leur csv), leurs coordonnées xy (prédéfinis car ils ne changeent pas) et leurs températures prédites.

    """
    print("** #2. Predicitons **")

    # Liste pour stocker les résultats
    results = []

    # On définit déja les coordonnées des coordonnées de la liste de port qui ont des mesures (dans l'ordre)
    x_values = [6.606, 6.857,  6.158, 6.172, 6.337, 6.323, 6.54, 6.499, 6.66, 6.241, 6.476, 6.92, 6.241, 6.686, 6.851]  
    y_values =[46.403, 46.388, 46.208, 46.276, 46.451, 46.372, 46.506, 46.506, 46.405, 46.378, 46.376, 46.398, 46.301, 46.5, 46.456]

    # Lister tous les fichiers CSV dans le dossier
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    for i, path_data in enumerate(csv_files):

        # Charger le CSV
        full_path = os.path.join(folder_path, path_data)
        df = pd.read_csv(full_path, quotechar='"')
        df.columns = df.columns.str.replace('`', '')

        # Convertir la colonne 'date' en datetime
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', errors='coerce')

        # Convertir la date donnée en paramètre en datetime
        date = datetime.strptime(date_str, '%d/%m/%Y')
        jour_cible, mois_cible = date.day, date.month

        # Filtrer les données pour le jour et le mois cible, et créer une copie indépendante
        df_flt = df[(df['date'].dt.day == jour_cible) & (df['date'].dt.month == mois_cible)].copy()

        # Ne garder que les années passées pour l'entraînement
        current_year = date.year
        df_flt = df_flt[df_flt['date'].dt.year < current_year]  # Garde seulement les années avant la date cible

        # Ajouter la colonne 'année'
        df_flt['année'] = df_flt['date'].dt.year

        # Calculer la température moyenne par année
        temp_moyenne = df_flt.groupby('année')['temperature'].mean().reset_index()

        # Extraire les années (x) et les températures moyennes (y)
        x = temp_moyenne['année'].values.reshape(-1, 1)
        y = temp_moyenne['temperature'].values

        # Affichage des valeurs de x et y
        print("x (années):", x.flatten())  # Affiche les années sous forme d'une liste
        print("y (températures):", y)  # Affiche les températures correspondantes

        # Modèle de régression linéaire
        model = LinearRegression()
        model.fit(x, y)

        # Prédire pour l'année de la date donnée
        temperature_pred = model.predict([[date.year]])

        x = x_values[i % len(x_values)]
        y = y_values[i % len(y_values)]
        
        # Ajouter les résultats pour chaque fichier
        results.append({
            'file_name': path_data, 
            'date': date_str, 
            'predicted_temperature': temperature_pred[0], 
            'x': x,  # Valeur de 'x'
            'y': y   # Valeur de 'y'
            })

    results_df = pd.DataFrame(results)
    results_df.to_csv(path_dest, index=False)


folder = "/Users/clemencechansel/Desktop/ECOLE/Epfl/CMT/Project-CMT/datas/temperature_data"
date_str = "27/07/2023"
result = pred(folder, date_str, './internal/predicted_temperature.csv')
