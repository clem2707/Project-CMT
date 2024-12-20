import os
import pandas as pd
from datetime import datetime
import sys

def real_temp(folder_path, date_str, path_dest):
    """
    This function is inspired by those in "code/predictions_stat.py". It takes as input: a folder containing CSV files of temperature records from each port on Lake Geneva, a date, and a path to store the results.
    The goal of this function is to extract data for a specific date from each CSV file in the folder.
    The aim is to obtain a CSV similar to the one returned by the predict_folder function.
    We will use the two CSVs to compare with the actual values to analyze the reliability of our predictions.
    Our output CSV will contain 5 columns: port name, date, real temperature, x coordinates, and y coordinates.
    Before extracting our temperatures, we will pre-fill our results list with parameters that do not change. These parameters are the x and y coordinates, and we include them in this CSV to facilitate the visualization step.
    """
    # Initialize an empty list to store the results
    results = []

    # Define the coordinates of the ports with measurements (in order)
    x_coords = [6.606, 6.857, 6.158, 6.172, 6.337, 6.323, 6.54, 6.499, 6.66, 6.241, 6.476, 6.92, 6.241, 6.686, 6.851]  
    y_coords = [46.403, 46.388, 46.208, 46.276, 46.451, 46.372, 46.506, 46.506, 46.405, 46.378, 46.376, 46.398, 46.301, 46.5, 46.456]

    # Iterate over each file in the folder
    for i, file_name in enumerate(os.listdir(folder_path)):
        if file_name.endswith('.csv'):
            # Construct the full path of the file
            file_path = os.path.join(folder_path, file_name)
            
            # Read the CSV file into a DataFrame 
            df = pd.read_csv(file_path, quotechar='"')
            df.columns = df.columns.str.replace('`', '')
            
            # Convert to datetime: the 'date' column in the CSV and the given date parameter
            df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', errors='coerce')
            date = datetime.strptime(date_str, '%d/%m/%Y')

            # Isolate the target day and month to facilitate filtering the CSV
            target_day, target_month, target_year = date.day, date.month, date.year

            # Filter the data for the target day and month and create an independent copy to avoid modifying the original CSV
            df_filtered = df[(df['date'].dt.day == target_day) & (df['date'].dt.month == target_month) & (df['date'].dt.year == target_year)].copy()

            # Calculate the average temperature for the given date
            temperature = df_filtered['temperature'].mean()

            x = x_coords[i-1]
            y = y_coords[i-1]

            # Add the result to the list
            results.append({
                'file_name': file_name,
                'date': date_str,
                'temperature': temperature,
                'x': x,
                'y': y
            })

    # Create a CSV by passing through a DataFrame to present it well with column names
    # path_dest represents where our CSV will be saved
    results_df = pd.DataFrame(results)
    results_df.to_csv(path_dest, index=False)


if __name__ == "__main__":
    real_temp(sys.argv[1], sys.argv[2], sys.argv[3])