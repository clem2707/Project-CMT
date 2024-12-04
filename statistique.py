from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error


# lecture fichier csv
file_name = "data/geneve.csv"  # faire passer le fichier de l'endroit qu'on veut 
df = pd.read_csv(file_name, quotechar='"')

# format des colonnes
df.columns = df.columns.str.strip().str.replace('`', '')

# convertion des colonnes qui nous interressent : date et température en format exploitable
df['date'] = df['date'].apply(lambda x: pd.Timestamp(x))

df['temperature'] = df['temperature'].astype(float)

# Ajouter une colonne 'week_of_year' pour grouper par semaine
df['week_of_year'] = df['date'].dt.isocalendar().week
df['year'] = df['date'].dt.year

# Calculer la moyenne hebdomadaire pour chaque année
weekly_avg = df.groupby(['year', 'week_of_year'])['temperature'].mean().reset_index()

# 1an = 57 semaine 
# périodes à analyser : été et hiver
summer_weeks = list(range(23, 35))  # semaine en été: début juin -> fin aout
winter_weeks = list(range(1, 9)) + list(range(49, 57))  # semaine en hiver: début décembre -> janvier -> fin fevrier

# Régression polynomiale 
degree = 10 # de degré 10
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
