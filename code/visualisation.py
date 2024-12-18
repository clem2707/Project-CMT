import matplotlib.pyplot as plt
import csv
import numpy as np

# File paths for the CSV files

csv_physic_model_eaux_vives_2024 = "internal/Eaux-vives_temperatures_2024.csv"  # Physic csv file
csv_stat_model_eaux_vives_2024 = "internal/annual_predictions_2025.csv" # Statistic csv file
csv_data_eaux_vives_2024 = "datas/temperature_data/geneve.csv"  # Data csv file

# Initialize lists to store the data
physic_temp = []
stat_temp = []
filtered_data = []


# Reading the CSV file for the physical model predictions
with open(csv_physic_model_eaux_vives_2024, mode='r', encoding='utf-8') as file:

    reader = csv.reader(file)
    headers = next(reader)  # Read the first line (headers)
    
    for row in reader:

        # Extract the columns
        physic_temp.append(float(row[5]))  # Sixth column: temperature with all the parameters



# Reading the CSV file for the statistical model predictions
with open(csv_stat_model_eaux_vives_2024, mode='r', encoding='utf-8') as file:

    reader = csv.reader(file)
    headers = next(reader)
    
    for row in reader:
        
        # Extract the columns
        stat_temp.append(float(row[1]))  # Second column: statistical model predictions

# Reading the CSV file for the actual temperature data
with open(csv_data_eaux_vives_2024, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    headers = next(reader)  # Read the first line (headers)
    
    for row in reader:
        if '2024' in row[1]:
            filtered_data.append(row)  # Extract the data for 2024

# Extracting the temperature values for 2024
temp = [row[3] for row in filtered_data]
print(temp)

# Convert temperatures to float
float_temperatures = [float(tempe) for tempe in temp]

# Display the list of temperatures as floats
print(float_temperatures)

# Calculate the 8-day moving average
i = 0
sum_temp = 0.0
moving_avg_list = []
length = len(float_temperatures)
for t in range(length):
    if i % 8 != 0:
        sum_temp += float_temperatures[t]
        i += 1
    else:
        avg = sum_temp / 8
        moving_avg_list.append(avg)
        print(avg, t / 8)
        sum_temp = float_temperatures[t]
        i += 1

# Adjust the list for plotting
moving_avg_adjusted = moving_avg_list[1:]

# Create X axes for each list
x1 = np.arange(1, 366)  # X-axis for the first two lists (1 to 365)
x2 = np.arange(1, 366)
x3 = np.arange(1, 327)  # X-axis for the third list (1 to 325)

# Plot the first two lists as curves
plt.plot(x1, temp_warming_noise_extreme_inertia_currents, label="Physic prediction", color='b')
plt.plot(x2, temp_predic_stat, label="Statistic prediction", color='r')

# Plot the third list as points
plt.scatter(x3, moving_avg_adjusted, label="Actual data", color='g')

# Add labels and title
plt.xlabel("Day of the year")
plt.ylabel("Temperature")
plt.title("Temperature of the surface of Lake Geneva in 2024")

# Add a legend
plt.legend()

# Display the plot
plt.show()
