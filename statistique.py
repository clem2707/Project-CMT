from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error

# Lire le fichier CSV
file_name = "geneve_copie.csv"  # Remplacez par le chemin vers votre fichier
df = pd.read_csv(file_name, quotechar='"')

# Nettoyer les noms de colonnes
df.columns = df.columns.str.strip().str.replace('`', '')

# Convertir la colonne 'date' au format datetime
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', errors='coerce')

# Convertir la colonne 'temperature' en float
df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')

# Supprimer les lignes où la température ou la date est NaN
df = df.dropna(subset=['temperature', 'date'])

# Ajouter une colonne 'week_of_year' pour grouper par semaine
df['week_of_year'] = df['date'].dt.isocalendar().week
df['year'] = df['date'].dt.year

# Calculer la moyenne hebdomadaire pour chaque année
weekly_avg = df.groupby(['year', 'week_of_year'])['temperature'].mean().reset_index()

# Définir les périodes (été et hiver)
summer_weeks = list(range(22, 40))  # Semaines d'été
winter_weeks = list(range(1, 22)) + list(range(40, 53))  # Semaines d'hiver

# Régression polynomiale de degré 10
degree = 10
poly = PolynomialFeatures(degree=degree)

def plot_season(data, weeks_filter, title):
    plt.figure(figsize=(14, 8))
    for year in data['year'].unique():
        year_data = data[(data['year'] == year) & (data['week_of_year'].isin(weeks_filter))]
        weeks = year_data['week_of_year'].values.reshape(-1, 1)  # X (semaine)
        temps = year_data['temperature'].values  # y (température)

        if len(weeks) > 0:  # Vérifier qu'il y a des données
            # Transformer les semaines en termes polynomiaux
            weeks_poly = poly.fit_transform(weeks)

            # Ajuster le modèle de régression polynomiale
            model = LinearRegression()
            model.fit(weeks_poly, temps)
            predicted = model.predict(weeks_poly)

            # Calculer l'erreur pour évaluer la précision
            mse = mean_squared_error(temps, predicted)

            # Tracer les données réelles et la courbe de régression
            plt.scatter(weeks, temps, label=f"Données {year}", alpha=0.7)
            plt.plot(
                weeks,
                predicted,
                '-',
                label=f"Régression {year}, degré {degree} (MSE: {mse:.2f})",
                alpha=0.7,
            )

    # Ajouter des labels et un titre
    plt.xlabel("Semaine de l'année")
    plt.ylabel("Température moyenne (°C)")
    plt.title(title)
    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), title="Légende")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# 1. Graphe pour toutes les semaines
plot_season(weekly_avg, range(1, 53), "Régression polynomiale (degré 10) : Toutes les semaines")

# 2. Graphe pour l'été
plot_season(weekly_avg, summer_weeks, "Régression polynomiale (degré 10) : Été (semaines 22 à 39)")

# 3. Graphe pour l'hiver
plot_season(weekly_avg, winter_weeks, "Régression polynomiale (degré 10) : Hiver (semaines 1-21 et 40-52)")
