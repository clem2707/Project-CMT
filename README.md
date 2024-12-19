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
    - "physic_pred_Geneva_2024.csv"
    - "physic_pred_Morges_2024.csv"
    - "physic_pred_Geneva_2050.csv"
    - "physic_pred_Morges_2050.csv"
  - 4 csv files of temperature datas from the statistic model
    - "stat_pred_gva_2024.csv"
    - "stat_pred_morges_2024.csv"
    - "stat_pred_gva_2050.csv"
    - "stat_pred_morges_2050.csv"
  - "interior_poinst.csv" a csv file containing x and y values of the ports
3. Plot differents graphes with both models, and a statistically based temperature map of lake Geneva

## Project structure

- "*data/*" contains input data
- "*internal/*" contains csv files used for passing information between C and Python. They are automatically
edited by the program and should not be manually modified.
- "*results/*" contains saved .png files of plotted results
- "*code/*" contains program code

### Inputs and outputs

Inputs:
- "*datas/*temperature_data*" is a folder containing:
  - "*data/bouveret.csv" is a comma-delimted file.
  - "*data/evian.csv" is a comma-delimted file.
  - "*data/geneve.csv" is a comma-delimted file.
  - "*data/hermance.csv" is a comma-delimted file.
  - "*data/lugrin.csv" is a comma-delimted file.
  - "*data/lutry.csv" is a comma-delimted file.
  - "*data/morges.csv" is a comma-delimted file.
  - "*data/nyon.csv" is a comma-delimted file.
  - "*data/rolle.csv" is a comma-delimted file.
  - "*data/saint-sulpice" is a comma-delimted file.
  - "*data/thonon.csv" is a comma-delimted file.
  - "*data/versoix.csv" is a comma-delimted file.
  - "*data/vevey.csv" is a comma-delimted file.
  - "*data/villeneuve.csv" is a comma-delimted file.
  - "*data/yvoire.csv" is a comma-delimted file.
- "*datas/harbor.csv" is a semicolon-delimited file.

Internal files:
  - "*internal/interior_points.csv" is a comma-delimted file.
  - "*internal/physic_pred_Geneva_2024.csv" is a comma-delimted file.
  - "*internal/physic_pred_Morges_2024.csv" is a comma-delimted file.
  - "*internal/physic_pred_Geneva_2050.csv" is a comma-delimted file.
  - "*internal/physic_pred_Morges_2050.csv" is a comma-delimted file.
  - "*internal/stat_pred_gva_2024.csv" is a comma-delimted file.
  - "*internal/stat_pred_morges_2024.csv" is a comma-delimted file.
  - "*internal/stat_pred_gva_2050.csv" is a comma-delimted file.
  - "*internal/stat_pred_morges_2050.csv" is a comma-delimted file.


Outputs:
- "*results/Plot temperature in Geneva in 2024.png" is a png file.
- "*results/Plot temperature in Morges in 2024.png" is a png file.
- "*results/Plot temperature in Geneva in 2050.png" is a png file.
- "*results/Plot temperature in Morges in 2050.png" is a png file.
- "*results/Plot temperature in Geneva in 2024 and 2050.png" is a png file.
- "*results/Plot temperature in Morges in 2024 and 2050.png" is a png file.
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
- "*physic_model.exe*" which simply allows the compilation of "*physic_model.c"
CLEM FUNCTIONS
- "*visualisation.py"
  - Imports the 8 created csv files and 2 csv files coming from "*datas/*"
  - Plots differents graphes based on the csv files
  - Save the graphes in the "*results/*" folder


## Instructions

To reproduce results in the report, X steps should be followed. It's important to notice that the physic model contains some random module so the exact reproduction isn't possible, but the differences is implemented on purpose because the wheater isn't an exact science and the yearly temperature doesn't reproduce exactly for each year.

A COMPLETER

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