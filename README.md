# SIE Computational Methods and Tools - Project : Temperature modelisation of Lake geneva

## Project Description

This program will compute temperature of the surface of lake Geneva with two models.
One statistical model based on datas and one physical model based on the place of interest of the lake, differents parameters and a sinusoidal equation.
Finally it computes a 2D map of lake geneva and attributes temperature at the surface on a chosen day on a certain area of the lake. 

This program wil:
1. Read in inputs
  - datas found in "*datas/temperature_data*" folder containing 15 temperature datas csv files of 15 places around the lake, and a csv file containing a high number of coordonates of ports around the lake .
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
  - "*interior_poinst.csv*" a csv file containing x and y values of the ports
3. Plot differents graphes with both models, and a statistically based temperature map of lake Geneva

## Project structure

- "*data/*" contains input data
- "*internal/*" contains csv files used for passing information between C and Python. They are automatically
edited by the program and should not be manually modified.
- "*results/*" contains saved .png files of plotted results
- "*code/*" contains program code
C:\Users\svenp\Documents\EPFL\CMT\Project-CMT\datas\temperature_data\bouveret.csv
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


Outputs:
- "*results/Plot temperature in Geneva in 2024.png*" is a png file.
- "*results/Plot temperature in Morges in 2024.png*" is a png file.
- "*results/Plot temperature in Geneva in 2050.png*" is a png file.
- "*results/Plot temperature in Morges in 2050.png*" is a png file.
- "*results/Plot temperature in Geneva in 2024 and 2050.png*" is a png file.
- "*results/Plot temperature in Morges in 2024 and 2050.png*" is a png file.
- REGRESSION LINEAIRE ET MAP
You are free to save or delete them after the execution

## Implementation details

**Overview**
- Both Python and C create csv files, on the base of the parameters of "*datas/*" folder and implemented
parameters in the function such as the locations.
- Python reads the created csv files and compute the visualisation part adding the plots in the "*results/" folder.

**Structure** In the directory "*code/" are located:
- "*physic_model.c*"
  - Initialize the location of interest and its useful parameters
  - Create 5 lists of daily temperature for a given year adding each time a new parameter to complexify the physic model.
  - Create a csv file for the two locations and years of interest containing these lists of temperature
- "*physic_model.exe*" which simply allows the compilation of "*physic_model.c*"
- "*map_lake.py*" 
  - creates a map of Lake Geneva from a list of ports with their xy coordinates and it is save in the "*results/*" folder. 
  - draw a polygon linking the harbours, then generate indices to traverse the points inside the polygon and export a CSV file containing these points.
- "*temp_stat_predictions.py*"
  - this code is used to statistically predict temperatures in Lake Geneva based on historical data from harbours around the lake, it comprises three main functions:
    - a function dedicated to predicting temperatures for a given date using linear regression based on historical data for one day over several years.
    - a function for processing a complete file by applying the first function to each data file.
    - a function that makes predictions over an entire year by running each day successively through the first function.
  - the results of the predictions are saved in CSV file in the "*internal/*" folder, making them easy to view and analyse.
- "*real_temp.py*"
  - this function retrieves the actual temperatures of Lake Geneva for a given date from historical data recorded in the ports around the lake
  - it explores a folder containing CSV files, filters the data to isolate those corresponding to the specified date, calculates the average temperature for each port since there are several values per day, and associates these values with the xy coordinates of the ports.
  - the result is a CSV file save in the "*internal/*" folder and it is structured in 5 columns: port name, date, actual temperature, x and y coordinates. 
- "*display_stat.py*"
  - this function displays and interpolates Lake Geneva temperatures from port and inland point data.
    - imports data from predicted temperatures and inland points.
    - calculates inland point temperatures via a weighted average of nearest neighbours using a k-d tree.
    - generates a map displaying predicted and interpolated points with a colour palette representing temperatures.
  - the result is a complete and accurate map of thermal variations over the surface of the lake save in the "*results/*" folder.
- "*linear_regression.py*"
  - this function generates a graph showing polynomial regressions of annual temperatures since 2018 in a specific port.
    - reads a CSV file containing hourly temperature records and formats the columns.
    - converts dates into years and days of the year, then calculates daily averages.
    - fits a degree 4 polynomial model to the daily averages for each year.
    - plots a smooth curve for each year, representing the annual variations in temperature.
    - the resulting graph highlights annual climate trends and is saved as a PNG file in the "*results/*" folder.
- "*visualisation.py*"
  - Imports the 8 created csv files and 2 csv files coming from "*datas/*"
  - Plots differents graphes based on the csv files
  - Save the graphes in the "*results/*" folder


## Instructions

To reproduce results in the report, X steps should be followed. It's important to notice that the physic model contains some random module so the exact reproduction isn't possible, but the differences is implemented on purpose because the wheater isn't an exact science and the yearly temperature doesn't reproduce exactly for each year.

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