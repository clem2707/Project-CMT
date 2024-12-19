import os
import pandas as pd
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
import sys

def predict_csv(file_path, date_str):
    """
    This function takes as input: a CSV file containing temperature records (since 2018 and every 3 hours) from a port on Lake Geneva, and a date for which we want to know the temperature across the lake.
    The goal of this function is to statistically predict lake temperatures at a specific location by training a model on the available data.
    
    It filters the input CSV to get all past data for the given day. Since we have multiple values per day, it averages the values by year (i.e., by day of a specific year).
    Then, it associates x with a list of years, which corresponds to y, a list of average temperatures for each year.
    Next, the function creates a linear regression model that it trains with our x as input and y as output.
    Finally, it uses the trained model to predict a temperature for the given date.
    """
    # Load and read the CSV of temperature records from a port
    df = pd.read_csv(file_path, quotechar='"')
    df.columns = df.columns.str.replace('`', '')

    # Convert to datetime: the 'date' column in the CSV and the given date parameter
    df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y %H:%M', errors='coerce')

    date = datetime.strptime(date_str, '%d/%m/%Y')

    # Isolate the target day and month to facilitate filtering the CSV
    target_day, target_month = date.day, date.month

    # Filter the data for the target day and month, and create an independent copy to avoid modifying the original CSV
    df_filtered = df[(df['date'].dt.day == target_day) & (df['date'].dt.month == target_month)].copy()

    # Keep only past years for training
    current_year = date.year
    df_filtered = df_filtered[df_filtered['date'].dt.year < current_year]  

    # Add the 'year' column
    df_filtered['year'] = df_filtered['date'].dt.year

    # Calculate the average temperature by year (for the requested day for each year)
    avg_temp = df_filtered.groupby('year')['temperature'].mean().reset_index()

    # Extract years (x) and average temperatures (y)
    x = avg_temp['year'].values.reshape(-1, 1)  # Reshape x to become a column. This formatting is essential for linear regression.
    y = avg_temp['temperature'].values

    # Linear regression model
    model = LinearRegression()
    model.fit(x, y)

    # Predict for the year of the given date
    predicted_temp = model.predict([[date.year]])

    return predicted_temp[0]


def predict_folder(folder_path, date_str, path_dest):
    """
    This function takes as input: a folder containing CSV files of temperature records from each port on Lake Geneva, a date and a location to store the CSV file.
    The goal of this function is to use the predict_csv function for each file in the folder and return the results as a CSV.
    This CSV will be used for lake visualization and interpolation.
    Fortunately, our folder is in an order that goes around the lake.
    Our output CSV will contain 5 columns: port name, date, predicted temperature, x coordinates, and y coordinates.
    Before predicting our temperatures, we will pre-fill our results list with parameters that do not change. These parameters are the x and y coordinates, and we put them in this CSV to facilitate the visualization step.
    """
    # Initialize an empty list
    results = []

    # Define the coordinates of the ports with measurements (in order)
    x_coords = [6.606, 6.857, 6.158, 6.172, 6.337, 6.323, 6.54, 6.499, 6.66, 6.241, 6.476, 6.92, 6.241, 6.686, 6.851]  
    y_coords = [46.403, 46.388, 46.208, 46.276, 46.451, 46.372, 46.506, 46.506, 46.405, 46.378, 46.376, 46.398, 46.301, 46.5, 46.456]

    # List all CSV files in the folder
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

    # Loop to iterate over each CSV
    for i, file_name in enumerate(csv_files):
        # Join the folder name with the CSV name to access it
        full_path = os.path.join(folder_path, file_name)
        # Use the function to define our predicted temperature for a CSV
        predicted_temp = predict_csv(full_path, date_str)

        # Link the predicted temperature to the correct x and y element
        x, y = x_coords[i], y_coords[i]
        
        # Add the results for each CSV:
        # the name is the CSV name because it contains the port name,
        # the date is the one given as an argument,
        # the predicted temperature using the predict_csv function,
        # the xy coordinates that match the port
        results.append({
            'file_name': file_name,
            'date': date_str,
            'temperature': predicted_temp,
            'x': x,
            'y': y
        })
    # Create a CSV by passing through a DataFrame to present it well with column names
    # path_dest represents where our CSV will be saved
    results_df = pd.DataFrame(results)
    results_df.to_csv(path_dest, index=False)
    

def predict_year(file_path, year, path_dest): 
    """
    This function takes as input: a CSV file of temperature records from a port on Lake Geneva and a year.
    It uses the predict_csv function and inputs a CSV and a day of the year that iterates over 1 year (365 days).
    The predict_csv function will return a predicted temperature for a day of the year.
    Since the day iterates from January 1st to December 31st of the entered year, we will end up with a CSV of size 365.
    The goal is to later use this CSV to plot on a graph to compare our predictions (statistical and physical).
    """
    # Initialize the start date to January 1st (beginning of the year)
    # The year varies according to our needs
    start_date_str = f"01/01/{year}"
    # Convert to datetime format to be usable
    start_date = datetime.strptime(start_date_str, '%d/%m/%Y')

    # Initialize our results list
    all_results = []
    
    # Loop that iterates over all days of the year
    for i in range(365):
        # Update the new date and convert to str because the function takes the date as an argument in this form
        current_date = start_date + timedelta(days=i)
        current_date_str = current_date.strftime('%d/%m/%Y')

        # Use the function to predict the temperature
        predicted_temp = predict_csv(file_path, current_date_str)
        
        # Add this result (temperature) with its date to our list
        all_results.append({
            'date': current_date_str,
            'temperature': predicted_temp
        })
    # Create a CSV by passing through a DataFrame to present it well with column names
    # This CSV contains the predicted values with the corresponding dates for a whole year
    annual_results_df = pd.DataFrame(all_results)
    annual_results_df.to_csv(path_dest, index=False)


#predict_folder("datas/temperature_data", "01/01/2024", "internal/Lake_pred2024.csv")

if __name__ == "__main__":

    function_name = sys.argv[1]

    if function_name == "predict_csv":
        file_path = sys.argv[2]
        date_str = sys.argv[3]
        print(predict_csv(file_path, date_str))

    elif function_name == "predict_folder":
        folder_path = sys.argv[2]
        date_str = sys.argv[3]
        path_dest = sys.argv[4]
        predict_folder(folder_path, date_str, path_dest)

    elif function_name == "predict_year":
        file_path = sys.argv[2]
        year = sys.argv[3]
        path_dest = sys.argv[4]
        predict_year(file_path, year, path_dest)