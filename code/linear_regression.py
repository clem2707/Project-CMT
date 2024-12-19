import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

def linear_regression(file_name, path_results):
    """
    ** Visualisation des regressions polynomiales des températures depuis 2018, par année, à un endroit donné **

    La fonction prend en input : un fichier CSV contenant des archives de températures (depuis 2018 et toutes les 3 heures) d'un port du Geneva Lake, un chemin pour stocker sous forme de png le graphe.
    Le but est de créer un graphe qui approxime les variations des températures au cours de l'année dans un port donné.
    Cela afin de pouvoir analyser les variations des températures d'année en année.   
    """
    # Ouvrir, lire le csv et le convertir afin qu'il soit utilisable
    df = pd.read_csv(file_name, quotechar='"')
    df.columns = df.columns.str.strip().str.replace('`', '')

    # Conversion : 'date' en datetime et température en float
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', errors='coerce')
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')

    # Extraire l'année, le jour du mois, et l'heure de la date
    df['year'] = df['date'].dt.year
    df['day_of_year'] = df['date'].dt.dayofyear

    # Moyenne des températures par jour 
    daily_avg = df.groupby(['year', 'day_of_year'])['temperature'].mean().reset_index()

    # Graphe xy
    plt.figure(figsize=(12, 8))

    # Régression polynomiale sur les moyennes quotidiennes pour chaque année
    for year in daily_avg['year'].unique():
        # Filtrer les données pour une année 
        df_year = daily_avg[daily_avg['year'] == year]

        # Préparer les données pour la régression (x: jour , y: température)
        x = df_year['day_of_year'].values.reshape(-1, 1)
        y = df_year['temperature'].values

        # Appliquer la régression polynomiale
        poly = PolynomialFeatures(degree=4)
        x_poly = poly.fit_transform(x)  # Transformation des jours en polynôme
        model = LinearRegression()
        model.fit(x_poly, y) # Entrainer le model

        # Tracer la courbe de régression polynomiale d'une année
        # Utilisation de la fonction prédict pour tracer la courbe, mais génère pas de nouvelles données
        plt.plot(df_year['day_of_year'], model.predict(x_poly), label=f'Régression polynomiale {year}')

    plt.xlabel('Jour de l\'année')
    plt.ylabel('Température (°C)')
    plt.title(f'Regression polynomiale des températures moyennes quotidiennes pour chaque année')
    plt.legend()
    plt.savefig(path_results)

# Exemple d'utilisation de la fonction
file = "datas/temperature_data/geneve.csv"  
path_results = "results/graph_linear_regression_geneve.png"
linear_regression(file, path_results)