import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import sys

def polynomial_regression(file_name, path_results):
    """
    ** Visualization of polynomial regressions of temperatures since 2018, by year, at a given location **

    The function takes as input: a CSV file containing temperature records (since 2018 and every 3 hours) from a port of the Geneva Lake, a path to store the graph as a PNG.
    The goal is to create a graph that approximates temperature variations throughout the year at a given port.
    This is to better visualize temperature variations from year to year.
    """
    # Open, read the csv and convert it to be usable
    df = pd.read_csv(file_name, quotechar='"')
    df.columns = df.columns.str.strip().str.replace('`', '')

    # Conversion: 'date' to datetime and temperature to float
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', errors='coerce')
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')

    # Extract the year, day of the year, and hour from the date
    df['year'] = df['date'].dt.year
    df['day_of_year'] = df['date'].dt.dayofyear

    # Average temperatures per day
    daily_avg = df.groupby(['year', 'day_of_year'])['temperature'].mean().reset_index()

    # XY graph
    plt.figure(figsize=(12, 8))

    # Polynomial regression on daily averages for each year
    for year in daily_avg['year'].unique():
        # Filter data for one year
        df_year = daily_avg[daily_avg['year'] == year]

        # Prepare data for regression (x: day, y: temperature)
        x = df_year['day_of_year'].values.reshape(-1, 1)
        y = df_year['temperature'].values

        # Apply polynomial regression
        poly = PolynomialFeatures(degree=4)
        x_poly = poly.fit_transform(x)  # Transform days into polynomial
        model = LinearRegression()
        model.fit(x_poly, y)  # Train the model

        # Plot the polynomial regression curve for one year
        # Use the predict function to plot the curve, but it doesn't generate new data
        plt.plot(df_year['day_of_year'], model.predict(x_poly), label=f'Polynomial Regression {year}')

    plt.xlabel('Day of the Year')
    plt.ylabel('Temperature (°C)')
    plt.title('Polynomial Regression of Daily Average Temperatures for Each Year')
    plt.legend()
    plt.savefig(path_results)


if __name__ == "__main__":
    polynomial_regression(sys.argv[1], sys.argv[2])