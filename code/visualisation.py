import matplotlib.pyplot as plt
import csv
import numpy as np
import sys


# File paths for the CSV files

# Csv Geneva 2024

#csv_physic_model_eaux_vives_2024 = "internal/physic_pred_Geneva_2024.csv"  # Physic csv file for Geneva in 2024
#csv_stat_model_eaux_vives_2024 = "internal/stat_pred_gva_2024.csv" # Statistic csv file  for Geneva in 2024
#csv_data_eaux_vives_2024 = "datas/temperature_data/geneve.csv"  # Data csv file for Geneva in 2024

# Csv Morges 2024

#csv_physic_model_morges_2024 = "internal/physic_pred_Morges_2024.csv"  # Physic csv file for Morges in 2024
#csv_stat_model_morges_2024 = "internal/stat_pred_morges_2024.csv" # Statistic csv file  for Morges in 2024
#csv_data_morges_2024 = "datas/temperature_data/morges.csv"  # Data csv file for Morges in 2024

# Csv Geneva 2050

#csv_physic_model_eaux_vives_2050 = "internal/physic_pred_Geneva_2050.csv"  # Physic csv file for Geneva in 2050
#csv_stat_model_eaux_vives_2050 = "internal/stat_pred_gva_2050.csv" # Statistic csv file  for Geneva in 2050

# Csv Morges 2050

#csv_physic_model_morges_2050 = "internal/physic_pred_Morges_2050.csv"  # Physic csv file for Morges in 2050
#csv_stat_model_morges_2050= "internal/stat_pred_morges_2050.csv" # Statistic csv file  for Morges in 2050


# The function use physic and statistic model and acutal datas to plot the temperature in 2024
  
def plot_2024(csv_physic, csv_statistic, csv_data, place, year):

    """ This function takes three csv files and the place and year of interest as parameters (e.g. 2024). One csv contains the temperature computed with the physic model,
        one with the temperature computed with the statistic model and one with the measured temperature at the place. The two first are already in a good format to be plot and the last one needs some adjustements.
        It finally saves the plot in the 'results' folder."""
    

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

    x_model = np.arange(1, 366)    # X-axis for the physic and statistic model (1 to 365)
    x_data = np.arange(1, 327)  # X-axis for the data list (1 to 326)


    # Plot the models as curves

    plt.plot(x_model, physic_temp, label="Physic prediction", color='b')
    plt.plot(x_model, stat_temp, label="Statistic prediction", color='r')

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

    # Clear the plot

    plt.clf()




# The function use physic and statistic model to plot the temperature in 2050

def plot_2050(csv_physic, csv_statistic, place, year):

    """ This function takes two csv files and the place and year of interest as parameters (e.g. 2050). One csv contains the temperature computed with the physic model,
        one with the temperature computed with the statistic model, this time there is of course no measured temperatures for 2050. The same way as in the function 'plot_2024' we plot the temperatures.
        It finally saves the plot in the 'results' folder."""

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


    # Create X axes for the lists

    x = np.arange(1, 366)    # X-axis for the physic and statistic model (1 to 365)


    # Plot the models as curves

    plt.plot(x, physic_temp, label="Physic prediction", color='b')
    plt.plot(x, stat_temp, label="Statistic prediction", color='r')

    # Add labels and title

    plt.xlabel("Day of the year")
    plt.ylabel("Temperature")
    plt.title(f"Temperature of the surface of Lake Geneva near {place} in {year}")

    # Add a legend

    plt.legend()

    # Save the plot

    plt.savefig(f"results/Plot temperature in {place} in {year}")

    # Clear the plot

    plt.clf()



def plot_2024_vs_2050(csv_physic_2024, csv_physic_2050, place):

    """ This function takes two csv files and the place of interest as parameters. One csv contains the temperature computed with the physic model in 2024,
        the other one contains the temperature computed with the physical model in 2050. The same way as in the two other functions we plot the temperatures.
        It finally saves the plot in the 'results' folder."""

    # Initialize lists to store the data

    physic_temp_2024 = []
    physic_temp_2050 = []


    # Reading the CSV file for the physical model predictions

    with open(csv_physic_2024, mode='r', encoding='utf-8') as file:

        reader = csv.reader(file)
        headers = next(reader)  # Read the first line (headers)
    
        for row in reader:

            # Extract the columns
            physic_temp_2024.append(float(row[5]))  # Sixth column: temperatures with the physical model with all the parameters


    # Reading the CSV file for the physical model predictions

    with open(csv_physic_2050, mode='r', encoding='utf-8') as file:

        reader = csv.reader(file)
        headers = next(reader)  # Read the first line (headers)
    
        for row in reader:

            # Extract the columns
            physic_temp_2050.append(float(row[5]))  # Sixth column: temperatures with the physical model with all the parameters


    # Create X axe

    x = np.arange(1, 366)    # X-axis for the physic model (1 to 365)

    # Plot the models as curves

    plt.plot(x, physic_temp_2024, label="Physic prediction for 2024", color='b')
    plt.plot(x, physic_temp_2050, label="Physic prediction for 2050", color='r')

    # Add labels and title

    plt.xlabel("Day of the year")
    plt.ylabel("Temperature")
    plt.title(f"Temperature of the surface of Lake Geneva near {place} in 2024 and 2050")

    # Add a legend

    plt.legend()

    # Save the plot

    plt.savefig(f"results/Plot temperature in {place} in 2024 and 2050")

    # Clear the plot

    plt.clf()

# Call the functions
#Geneva_2024 = plot_2024(csv_physic_model_eaux_vives_2024, csv_stat_model_eaux_vives_2024, csv_data_eaux_vives_2024, "Geneva", 2024)

#Morges_2024 = plot_2024(csv_physic_model_morges_2024, csv_stat_model_morges_2024, csv_data_morges_2024, "Morges", 2024)

#Geneva_2050 = plot_2050(csv_physic_model_eaux_vives_2050, csv_stat_model_eaux_vives_2050, "Geneva", 2050)

#Morges_2050 = plot_2050(csv_physic_model_morges_2050, csv_stat_model_morges_2050, "Morges", 2050)

#Geneva_2024_2050 = plot_2024_vs_2050(csv_physic_model_eaux_vives_2024, csv_physic_model_eaux_vives_2050, "Geneva")

#Morges_2024_2050 = plot_2024_vs_2050(csv_physic_model_morges_2024, csv_physic_model_morges_2050, "Morges")


if __name__ == "__main__":

    function_name = sys.argv[1]

    if function_name == "plot_2024":
        print(plot_2024(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]))

    elif function_name == "plot_2050":
        plot_2050(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    elif function_name == "plot_2024_vs_2050":
        plot_2024_vs_2050(sys.argv[2], sys.argv[3], sys.argv[4])
