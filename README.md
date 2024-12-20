# SIE Computational Methods and Tools - Project : Temperature modelisation of Lake geneva

## Project Description

This program will compute temperature of the surface of lake Geneva with two models.
One statistical model based on datas and one physical model based on the place of interest of the lake, differents parameters and a sinusoidal equation.
Finally it computes a 2D map of lake geneva and attributes temperatures at the surface on a chosen day on a certain area of the lake. 

This program wil:
1. Read in inputs
  - datas found in "*datas/temperature_data*" folder containing 15 temperature datas csv files of 15 places around the lake, and a csv file "*datas/harbor.csv*" containing a high number of coordonates of harbors around the lake .
2. Generate
  - 4 csv files of temperature datas from the physical model
    - "*physic_pred_Geneva_2024.csv*"
    - "*physic_pred_Morges_2024.csv*"
    - "*physic_pred_Geneva_2050.csv*"
    - "*physic_pred_Morges_2050.csv*"
  - 4 csv files of temperature datas from the statistic model
    - "*stat_pred_gva_2024.csv*"
    - "*stat_pred_morges_2024.csv*"
    - "*stat_pred_gva_2050.csv*"
    - "*stat_pred_morges_2050.csv*"
  - "*interior_poinst.csv*" a csv file containing x and y values of the harbors
3. Plot differents graphes with both models, and a statistically and measured based temperature map of lake Geneva

## Project structure

- "*data/*" contains input data
- "*internal/*" contains csv files used for passing information between C and Python. They are automatically
edited by the program and should not be manually modified.
- "*results/*" contains saved .png files of plotted results
- "*code/*" contains program code

### Inputs and outputs

Inputs:
- "*datas/temperature_data*" is a folder containing:
  - "*datas/temperature_data/bouveret.csv*" is a comma-delimted file.
  - "*datas/temperature_data/evian.csv*" is a comma-delimted file.
  - "*datas/temperature_data/geneve.csv*" is a comma-delimted file.
  - "*datas/temperature_data/hermance.csv*" is a comma-delimted file.
  - "*datas/temperature_data/lugrin.csv*" is a comma-delimted file.
  - "*datas/temperature_data/lutry.csv*" is a comma-delimted file.
  - "*datas/temperature_data/morges.csv*" is a comma-delimted file.
  - "*datas/temperature_data/nyon.csv*" is a comma-delimted file.
  - "*datas/temperature_data/rolle.csv*" is a comma-delimted file.
  - "*datas/temperature_data/saint-sulpice.csv*" is a comma-delimted file.
  - "*datas/temperature_data/thonon.csv*" is a comma-delimted file.
  - "*datas/temperature_data/versoix.csv*" is a comma-delimted file.
  - "*datas/temperature_data/vevey.csv*" is a comma-delimted file.
  - "*datas/temperature_data/villeneuve.csv*" is a comma-delimted file.
  - "*datas/temperature_data/yvoire.csv*" is a comma-delimted file.
- "*datas/harbor.csv*" is a semicolon-delimited file.

Internal files:
  - "*internal/interior_points.csv*" is a comma-delimted file.
  - "*internal/physic_pred_Geneva_2024.csv*" is a comma-delimted file.
  - "*internal/physic_pred_Morges_2024.csv*" is a comma-delimted file.
  - "*internal/physic_pred_Geneva_2050.csv*" is a comma-delimted file.
  - "*internal/physic_pred_Morges_2050.csv*" is a comma-delimted file.
  - "*internal/stat_pred_gva_2024.csv*" is a comma-delimted file.
  - "*internal/stat_pred_morges_2024.csv*" is a comma-delimted file.
  - "*internal/stat_pred_gva_2050.csv*" is a comma-delimted file.
  - "*internal/stat_pred_morges_2050.csv*" is a comma-delimted file.
  - "*internal/temp_pred_01_01_2024.csv*" is a comma-delimted file.
  - "*internal/temp_real_01_01_2024*" is a comma-delimted file.


Outputs:
- "*results/Temperature_Geneva_2024.png*" is a png file.
- "*results/Temperature_Morges_2024.png*" is a png file.
- "*results/Temperature_Geneva_2050.png*" is a png file.
- "*results/Temperature_Morges_2050.png*" is a png file.
- "*results/Temperature_Geneva_2024_2050.png*" is a png file.
- "*results/Temperature_Morges_2024_2050.png*" is a png file.
- "*results/Lake_template.png*" is a png file.
- "*results/Lake_prediction_01_01_2024.csv*" is a png file.
- "*results/Lake_measure_01_01_2024.png*" is a png file.
You are free to save or delete them after the execution

## Implementation details

**Overview**
- Both Python and C create csv files, on the base of the parameters of "*datas/*" folder and implemented
parameters in the function such as the locations.
- Python reads the created csv files in "*internal/*" and compute the visualisation part adding the plots in the "*results/*" folder.

**Structure** In the directory "*code/*" are located:
- "*physic_model.c*"
  - Initialize the location of interest and its useful parameters.
  - Create 5 lists of daily temperature for a given year adding each time a new parameter to complexify the physic model.
  - Create a csv file for the two locations and years of interest containing these lists of temperatures.
- "*map_lake.py*" 
  - Creates a map of Lake Geneva from a list of harbors with their x, y coordinates and saves it in the "*results/*" folder. 
  - Draw a polygon linking the harbors, then generate indices to run through the points inside the polygon and export a csv file containing these points.
- "*temp_stat_predictions.py*"
  - This code is used to statistically predict temperatures in Lake Geneva based on historical data from harbors around the lake, it contains three main functions:
    - A function dedicated to predicte temperatures for a given date using linear regression based on historical data for one day over several years.
    - A function for processing a complete file by applying the first function to each data file.
    - A function that makes predictions over an entire year by running each day successively through the first function.
  - The results of the predictions are saved in CSV file in the "*internal/*" folder, making them easy to view and analyse.
- "*real_temp.py*"
  - This function retrieves the actual temperatures of lake Geneva for a given date from historical data recorded in the harbors around the lake.
  - It explores a folder containing csv files, filters the data to isolate those corresponding to the specified date, calculates the average temperature for each port since there are several values per day, and associates these values with the x, y coordinates of the ports.
  - The result is a csv file saved in the "*internal/*" folder and it is structured in 5 columns: port name, date, actual temperature, x and y coordinates. 
- "*display_stat.py*"
  - This function displays and interpolates lake Geneva temperatures from harbor and inland point datas.
    - Imports data from predicted temperatures and inland points.
    - Calculates inland point temperatures via a weighted average of nearest neighbours using a k-d tree.
    - Generates a map displaying predicted and interpolated points with a colour palette representing temperatures.
  - The result is a complete and accurate map of thermal variations over the surface of the lake save in the "*results/*" folder.
- "*linear_regression.py*"
  - This function generates a graph showing polynomial regressions of annual temperatures since 2018 in a specific harbor.
    - Reads a CSV file containing hourly temperature records and formats the columns.
    - Converts dates into years and days of the year, then calculates daily averages.
    - Fits a degree 4 polynomial model to the daily averages for each year.
    - Plots a smooth curve for each year, representing the annual variations in temperature.
    - The resulting graph highlights annual climate trends and is saved as a PNG file in the "*results/*" folder.
- "*visualisation.py*"
  - Imports the 8 created csv files and 2 csv files coming from "*datas/*".
  - Plots differents graphes based on the csv files.
  - Save the graphes in the "*results/*" folder.


## Instructions

To reproduce results in the report, 3 steps should be followed.
It's important to notice that the physic model contains some random module so the exact reproduction isn't possible, but the differences is implemented on purpose because the wheater isn't an exact science and the yearly temperature doesn't reproduce exactly for each year.

1. Download all the necessary libraries
  - numpy
    type
    ```
    pip install numpy
    ```
  - pandas
    type
    ```
    pip install pandas
    ```
  - matplotlib
    type
    ```
    pip install matplotlib
    ```
  - scikit-learn
    type
    ```
    pip install scikit-learn
    ```
  - scipy
    type
    ```
    pip install scipy
    ```
  - shapely
    type
    ```
    pip install shapely
    ```
  To verify the library is well installed
  Write the code
  ```
  import "name of the library"
  print("name of the library".__version__)
  ```
  And execute the code

2.
A COMPLETER
python interpreter et écrire make dans le terminal

## Requirements

Versions of Python and C used are as follows.
```
$ python --version
Python 3.12.2

$ gcc --version
Apple clang version 16.0.0
```
The python libraries used were the following
```
numpy 2.1.3

pandas 2.2.3

matplotlib 3.9.3

scikit-learn 1.5.2

scipy 1.14.1

shapely 2.0.6
```

## Credits

### Data

The temperature datas in "*datas/temperature_datas" have been send by Nicholas Lindt, who drives a website about the temperature at surface of lake Geneva in differents places, with his agreement to use it. Here is his [website](https://lake.lindt.one).

The data file "*harbor.csv" comes from [Carto Leman](https://www.arcgis.com/apps/webappviewer/index.html?id=efb2bdccfdcf4fc18814426a63b5f6fa&extent=672740.9389%2C5810352.5672%2C705608.861%2C5825506.208%2C102100).

### Formulae

The function that calculate the MAET (Mean Annual Epilimnetic Temperature) relies on the study of [Ottosson and Abrahamsson](https://www.sciencedirect.com/science/article/pii/S0304380098000672?via%3Dihub) published on [ScienceDirect](https://www.sciencedirect.com/).

The Complexified sinusoïdal equation of the temperatures over a year [found here](https://atlashydrologique.ch/downloads/01/content/Text_Tafel73.fr.pdf).