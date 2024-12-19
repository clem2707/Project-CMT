import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

def linear_regression(file_name, path_results):
    df = pd.read_csv(file_name, quotechar='"')

    # Nettoyer les noms de colonnes (supprimer les espaces et les guillemets)
    df.columns = df.columns.str.strip().str.replace('`', '')

    # Convertir la colonne 'date' en datetime
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', errors='coerce')

    # Convertir la colonne 'temperature' en float
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')

    # Extraire l'année, le jour du mois, et l'heure de la date
    df['year'] = df['date'].dt.year
    df['day_of_year'] = df['date'].dt.dayofyear

    # Calculer la température moyenne par jour (en moyenne sur chaque jour)
    daily_avg = df.groupby(['year', 'day_of_year'])['temperature'].mean().reset_index()

    # Créer un modèle de régression polynomiale
    degree = 4  # Degré du polynôme (ex : 3 pour un polynôme de degré 3)

    # Tracer les régressions pour chaque année
    plt.figure(figsize=(12, 8))

    # Pour chaque année, effectuer une régression polynomiale sur les moyennes quotidiennes
    for year in daily_avg['year'].unique():
        # Filtrer les données pour l'année donnée
        df_year = daily_avg[daily_avg['year'] == year]

        # Préparer les données pour la régression (jour de l'année comme X, température comme y)
        X = df_year['day_of_year'].values.reshape(-1, 1)
        y = df_year['temperature'].values

        # Appliquer la régression polynomiale
        poly = PolynomialFeatures(degree=degree)
        X_poly = poly.fit_transform(X)  # Transformation des jours en polynôme
        model = LinearRegression()
        model.fit(X_poly, y)  # Ajustement du modèle

        # Prédire les valeurs de température pour l'année en question
        y_pred = model.predict(X_poly)

        # Tracer les résultats (régression polynomiale)
        plt.plot(df_year['day_of_year'], y_pred, label=f'Régression {year}')

        # Tracer les points réels pour l'année (température moyenne quotidienne)
        #plt.scatter(df_year['day_of_year'], df_year['temperature'], label=f'Données réelles {year}', alpha=0.5)

    # Ajouter des labels et un titre
    plt.xlabel('Jour de l\'année')
    plt.ylabel('Température (°C)')
    plt.title(f'Regression polynomiale des températures moyennes quotidiennes pour chaque année')
    plt.legend()
    plt.grid(True)
    plt.savefig(path_results)
    plt.close()

file = "datas/temperature_data/geneve.csv"  
path_results = "results/graph_linear_regression_geneve"
linear_regression(file, path_results)