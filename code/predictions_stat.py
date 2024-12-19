import os
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

def predict_csv(file_path, date_str):
    """
    Cette fonction prend en input : un fichier CSV contenant des archives de températures (depuis 2018 et toutes les 3 heures) d'un port du Geneva Lake, et une date pour laquelle on peut savoir la température sur tout le lac.
    Le but de cette fonction est de prédire statistiquement des températures du lac à un endroit précis, c'est-à-dire en entraînant un modèle sur les données à disposition.
    
    Elle filtre le csv entré afin d'avoir toutes les données passée du jour donné. Etant donné qu'on a plusieurs valeurs par jour, elle va faire une moyenne des valeurs par année (donc par jour d'une année précise). 
    Ensuite, elle associe à x, une liste des années, qui corresspondent à un y, une liste de températures moyenne pour chaque année.
    Ensuite, la fonction fait un model de régression linéaire qu'elle entraine avec nos x en entrée et y en sortie.
    Et pour finir, utilise le model entrainé afin de prédire une température pour la date demandé.

    """
    # Charger et lire le CSV des archives de températures d'un port
    df = pd.read_csv(file_path, quotechar='"')
    df.columns = df.columns.str.replace('`', '')

    # Convertion en datetime : la colonne 'date' du csv et la date donnée en paramètre
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', errors='coerce')

    date = datetime.strptime(date_str, '%d/%m/%Y')

    # On isole le jour et le mois recherché afin de faciliter le filtrage du csv
    jour_cible, mois_cible = date.day, date.month

    # Filtrer les données pour le jour et le mois cible, et créer une copie indépendante afin de ne pas modifier le csv original
    df_flt = df[(df['date'].dt.day == jour_cible) & (df['date'].dt.month == mois_cible)].copy()

    # Ne garder que les années passées pour l'entraînement
    current_year = date.year
    df_flt = df_flt[df_flt['date'].dt.year < current_year]  

    # Ajouter la colonne 'année'
    df_flt['année'] = df_flt['date'].dt.year

    # Calculer la température moyenne par année (par jour demandé pour chaque année)
    temp_moyenne = df_flt.groupby('année')['temperature'].mean().reset_index()

    # Extraire les années (x) et les températures moyennes (y)
    x = temp_moyenne['année'].values.reshape(-1, 1) # La fonction reshape met en forme x afin qu'il devienne une colonne. Cette mise en forme est essentielle pour la regression linéaire.
    y = temp_moyenne['temperature'].values

    # Modèle de régression linéaire
    model = LinearRegression()
    model.fit(x, y)

    # Prédire pour l'année de la date donnée
    temperature_pred = model.predict([[date.year]])

    return temperature_pred[0]


def predict_folder(folder_path, date_str, path_dest):
    """
    Cette fonction prend en input : un dossier contenant des fichiers CSV d'archives de températures de chacun des ports du Geneva Lake, et une date.
    Le but de cette fonction est d'utiliser la fonction predict_csv pour chaque fichier dans le dossier et retourner les résultats sous forme de CSV. 
    Ce csv nous servira pour la visualisation du lac et l'interpolation.
    Par chance, notre dossier est dans un ordre qui fait le tour du lac.
    Notre CSV de sortie, contiendra 5 colonnes : nom du port, date, température prédite, coordonnées x et coordonnées y. 
    Avant de prédire nos températures, nous allons préremplir notre liste de résultats avec les paramètres qui ne changent pas. Ces paramètres sont les coordonnées x et y et on les met sur ce csv afin de faciliter l'étape de la visualisation.
    """

    # Initialisation d'une liste vide
    results = []

    # On définit déjà les coordonnées des ports qui ont des mesures (dans l'ordre)
    x_values = [6.606, 6.857,  6.158, 6.172, 6.337, 6.323, 6.54, 6.499, 6.66, 6.241, 6.476, 6.92, 6.241, 6.686, 6.851]  
    y_values = [46.403, 46.388, 46.208, 46.276, 46.451, 46.372, 46.506, 46.506, 46.405, 46.378, 46.376, 46.398, 46.301, 46.5, 46.456]

    # Lister tous les fichiers CSV dans le dossier
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Boucle afin d'itérer sur chaque csv
    for i, path_data in enumerate(csv_files):
        # Joindre le nom du dossier avec le nom du csv pour pouvoir y acceder 
        full_path = os.path.join(folder_path, path_data)
        # Utilisation de la fonction pour définir notre température prédite pour un csv
        temperature_pred = predict_csv(full_path, date_str)

        # Relier la température prédite au bon élément de x et y.
        x, y = x_values[i], y_values[i]
        
        # Ajouter les résultats pour chaque csv :
        # le nom est le nom du csv car il contient le nom du port, 
        # la date est celle donnée en argument, 
        # la température prédite grace a la fonction predict_csv, 
        # les coordonnées xy qui coincident avec celle du port
        results.append({
            'file_name': path_data,
            'date': date_str,
            'predicted_temperature': temperature_pred,
            'x': x,
            'y': y
        })
    # Création d'un csv, en passant par un dataframe afin que ce soit bien présenté avec le nom des colonness
    # path_dest représente l'endroit ou sera répertorié notre csv
    results_df = pd.DataFrame(results)
    results_df.to_csv(path_dest, index=False)
    


def predict_year(file_path, year): 
    """
    Cette fonction prend en input : un fichier CSV d'archives de températures d'un port du lac Léman et une année.
    Elle utilise la fontion predict_csv et elle rentre en argument un csv et un jour de l'année qui va itérer sur 1 an (365 jours).
    La fonction utilisée predict_csv va retourner une température prédite pour un jour de l'année.
    Etant donnée que le jour itère du 1er janvier au 31 décembre de l'année rentrer, on va finir avec un csv d'une taille de 365.
    Le but est de pouvoir par la suite utiliser ce csv afin de plot sur un graphique pour pouvoir comparer nos prédictions (statistique et physique).
    
    """
    # Initialise la date de départ au 1er janvier (début de l'année)
    # L'année varie en fonction de nos besoins
    start_date_str = f"01/01/{year}"
    # On converti en format datetime afin qu'elle soit utilisable
    start_date = datetime.strptime(start_date_str, '%d/%m/%Y')

    # Initialisation de notre liste de résultats
    all_results = []
    
    # Boucle qui itère sur tout les jours de l'année
    for i in range(365):
        # Mise à jour de la nouvelle date et convertion en str car la fonction prend la date en argument sous cette forme
        current_date = start_date + timedelta(days=i)
        current_date_str = current_date.strftime('%d/%m/%Y')

        # Utilisation de la fonction pour prédire la température
        temperature_pred = predict_csv(file_path, current_date_str)
        
        # Ajouter ce resultat (température) avec sa date à notre liste
        all_results.append({
            'date': current_date_str,
            'predicted_temperature': temperature_pred
        })
    # Création d'un csv, en passant par un dataframe afin que ce soit bien présenté avec le nom des colonness
    # Ce csv contient donc les valeurs prédites avec les dates correspondant pour toute une année 
    annual_results_df = pd.DataFrame(all_results)
    annual_results_df.to_csv(f"internal/annual_predictions_{year}.csv", index=False)


predict_folder("datas/temperature_data", "01/01/2024", "internal/Lake_pred2024.csv")

