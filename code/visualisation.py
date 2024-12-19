import matplotlib.pyplot as plt
import csv
import numpy as np

# File paths for the CSV files

# Csv Geneva 2024

csv_physic_model_eaux_vives_2024 = "internal/Eaux-vives_temperatures_2024.csv"  # Physic csv file for Geneva in 2024
csv_stat_model_eaux_vives_2024 = "internal/annual_predictions_2025.csv" # Statistic csv file  for Geneva in 2024
csv_data_eaux_vives_2024 = "datas/temperature_data/geneve.csv"  # Data csv file for Geneva in 2024

# Csv Morges 2024

csv_physic_model_morges_2024 = "internal/Morges_temperatures_2024.csv"  # Physic csv file for Morges in 2024
csv_stat_model_morges_2024 = "internal/annual_predictions_2025.csv" # Statistic csv file  for Morges in 2024
csv_data_morges_2024 = "datas/temperature_data/morges.csv"  # Data csv file for Morges in 2024

# Csv Geneva 2050

csv_physic_model_eaux_vives_2050 = "internal/Eaux-vives_temperatures_2050.csv"  # Physic csv file for Geneva in 2050
csv_stat_model_eaux_vives_2050 = "internal/annual_predictions_2025.csv" # Statistic csv file  for Geneva in 2050

# Csv Morges 2050

csv_physic_model_morges_2050 = "internal/Morges_temperatures_2024.csv"  # Physic csv file for Morges in 2050
csv_stat_model_morges_2050= "internal/annual_predictions_2025.csv" # Statistic csv file  for Morges in 2050


# The function use physic and statistic model and acutal datas to plot the temperature in 2024
  
def plot_2024(csv_physic, csv_statistic, csv_data, place, year):


    # Initialize lists to store the data

    physic_temp = []
    stat_temp = []
    filtered_data = []


    # Reading the CSV file for the physical model predictions

    with open(csv_physic, mode='r', encoding='utf-8') as file:

        reader = csv.reader(file)
        headers = next(reader)  # Read the first line (headers)
    
        for row in reader:

            # Extract the columns
            physic_temp.append(float(row[5]))  # Sixth column: temperatures with the physical model with all the parameters



    # Reading the CSV file for the statistical model predictions

    with open(csv_statistic, mode='r', encoding='utf-8') as file:

        reader = csv.reader(file)
        headers = next(reader)
    
        for row in reader:
        
            # Extract the columns
            stat_temp.append(float(row[1]))  # Second column: temperatures with the statistical model predictions



    # Reading the CSV file for the actual temperature data

    with open(csv_data, mode='r', encoding='utf-8') as file:

        reader = csv.reader(file)
        headers = next(reader)
    
        for row in reader:
            if '2024' in row[1]:
                filtered_data.append(row)  # Extract the data for 2024


    # Extracting the data temperatures values for 2024

    data_temperature_2024 = [row[3] for row in filtered_data]


    # Convert temperatures to float

    float_data_temperature_2024 = [float(temp) for temp in data_temperature_2024]


    # Calculate the day temperature average (with 8 mesures per day)

    i = 0   # Iterartion counter
    sum_temp = 0.0  # Day temperature sum (built on the 8 temperature mesures per day)
    avg_list = []   # Initialization of the average temperature per day list
    length = len(float_data_temperature_2024)   # Number of day (326, not 366 because 2024 wasn't finish when the datas where imported)

    for t in range(length):

        if i % 8 != 0 and t != 0:

            sum_temp += float_data_temperature_2024[t]

        else:

            avg = sum_temp / 8
            avg_list.append(avg)
            sum_temp = float_data_temperature_2024[t]

        i += 1



    # Adjust the list for plotting

    avg_list_adjusted = avg_list[1:]  # remove the first 

    # Create X axes for each list

    x_physic = np.arange(1, 366)    # X-axis for the physic model (1 to 365)
    x_statistic = np.arange(1, 366)    # X-axis for the statistic model (1 to 365)
    x_data = np.arange(1, 327)  # X-axis for the data list (1 to 326)


    # Plot the models as curves

    plt.plot(x_physic, physic_temp, label="Physic prediction", color='b')
    plt.plot(x_statistic, stat_temp, label="Statistic prediction", color='r')

    # Plot the datas as points

    plt.scatter(x_data, avg_list_adjusted, label="Actual data", color='g')

    # Add labels and title

    plt.xlabel("Day of the year")
    plt.ylabel("Temperature")
    plt.title(f"Temperature of the surface of Lake Geneva near {place} in 2024")

    # Add a legend

    plt.legend()

    # Save the plot

    plt.savefig(f"results/Plot temperature in {place} in {year}")





# The function use physic and statistic model to plot the temperature in 2050

def plot_2050(csv_physic, csv_statistic, place, year):


    # Initialize lists to store the data

    physic_temp = []
    stat_temp = []


    # Reading the CSV file for the physical model predictions

    with open(csv_physic, mode='r', encoding='utf-8') as file:

        reader = csv.reader(file)
        headers = next(reader)  # Read the first line (headers)
    
        for row in reader:

            # Extract the columns
            physic_temp.append(float(row[5]))  # Sixth column: temperatures with the physical model with all the parameters



    # Reading the CSV file for the statistical model predictions

    with open(csv_statistic, mode='r', encoding='utf-8') as file:

        reader = csv.reader(file)
        headers = next(reader)
    
        for row in reader:
        
            # Extract the columns
            stat_temp.append(float(row[1]))  # Second column: temperatures with the statistical model predictions


    # Create X axes for each list

    x_physic = np.arange(1, 366)    # X-axis for the physic model (1 to 365)
    x_statistic = np.arange(1, 366)    # X-axis for the statistic model (1 to 365)


    # Plot the models as curves

    plt.plot(x_physic, physic_temp, label="Physic prediction", color='b')
    plt.plot(x_statistic, stat_temp, label="Statistic prediction", color='r')

    # Add labels and title

    plt.xlabel("Day of the year")
    plt.ylabel("Temperature")
    plt.title(f"Temperature of the surface of Lake Geneva near {place} in 2024")

    # Add a legend

    plt.legend()

    # Save the plot

    plt.savefig(f"results/Plot temperature in {place} in {year}")


# Call the functions

Geneva_2024 = plot_2024(csv_physic_model_eaux_vives_2024, csv_stat_model_eaux_vives_2024, csv_data_eaux_vives_2024, "Geneva", 2024)

Morges_2024 = plot_2024(csv_physic_model_morges_2024, csv_stat_model_morges_2024, csv_data_morges_2024, "Morges", 2024)

Geneva_2050 = plot_2050(csv_physic_model_eaux_vives_2050, csv_stat_model_eaux_vives_2050, "Geneva", 2050)

Morges_2050 = plot_2050(csv_physic_model_morges_2050, csv_stat_model_morges_2050, "Morges", 2050)