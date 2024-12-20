### ------ Setting up the compiling of C files ------ ###
# Specify the compiler for C files
CC = gcc

# Compiling flags
CFLAGS = -Wall -O2

# Libraries
LIBS = -lm 

# Output
OUT = -o

### ------ Setting up the compiling of Python files ------ ###
# Specify the Python interpreter - use your own. 
PYTHON = /opt/anaconda3/envs/cmt/bin/python

# Specify file names and their relative paths
PHYSIC_FILE = code/physic_model.c

# Specify the name of your Python files
MAP_LAKE_FILE = code/map_lake.py
TEMPERATURE_STAT_PREDICTION_FILE = code/temp_stat_predictions.py
REAL_TEMP_FILE = code/temp_real.py
DISPLAY_STAT_FILE = code/display_stat.py
VISUALISATION_FILE = code/visualisation.py
POLYNOMIAL_REGRESSION_FILE = code/polynomial_regression.py


### ------ Default target -> order in which you want the files to be run ------ ###
all: physic_compile physic_execute map_lake_python temp_prediction_python visualisation_temp_prediction_python real_temp_python visualisation_real_temp_python polynomial_regression_morges_python pred_temp_gva_2024_python visualisation_gva_2024_python pred_temp_gva_2050_python visualisation_gva_2050_python visualisation_finale_gva_python pred_temp_morges_2024_python visualisation_morges_2024_python pred_temp_morges_2050_python visualisation_morges_2050_python visualisation_finale_morges_python clean

# Arguments for python functions
MAP_ARGS ="datas/harbor.csv" "internal/interior_points.csv" "results/Lake_template.png"
PREDICTION_2024_ARGS = predict_folder "datas/temperature_data" "01/01/2024" "internal/temp_pred_01_01_2024.csv"
REAL_ARGS = "datas/temperature_data" "01/01/2024" "internal/temp_real_01_01_2024.csv"
DISPLAY_2024_ARGS = "internal/temp_pred_01_01_2024.csv" "internal/interior_points.csv" "results/Lake_prediction_01_01_2024.png"
DISPLAY_real_ARGS = "internal/temp_real_01_01_2024.csv" "internal/interior_points.csv" "results/Lake_measure_01_01_2024.png"

POLYNOMIAL_REGRESSION_MORGES_ARG = "datas/temperature_data/morges.csv" "results/Polynomial_Regression_Morges.png" 

TEMPERATURE_STAT_PREDICTION_GVA_2024_ARG = predict_year "datas/temperature_data/geneve.csv" "2024" "internal/stat_pred_gva_2024.csv"
TEMPERATURE_STAT_PREDICTION_GVA_2050_ARG = predict_year "datas/temperature_data/geneve.csv" "2050" "internal/stat_pred_gva_2050.csv"
TEMPERATURE_STAT_PREDICTION_MORGES_2024_ARG = predict_year "datas/temperature_data/morges.csv" "2024" "internal/stat_pred_morges_2024.csv"
TEMPERATURE_STAT_PREDICTION_MORGES_2050_ARG = predict_year "datas/temperature_data/morges.csv" "2050" "internal/stat_pred_morges_2050.csv"

VISUALISATION_GVA_2024_ARG = plot_2024 "internal/physic_pred_Geneva_2024.csv" "internal/stat_pred_gva_2024.csv" "datas/temperature_data/geneve.csv" "Geneva" 2024
VISUALISATION_GVA_2050_ARG = plot_2050 "internal/physic_pred_Geneva_2050.csv" "internal/stat_pred_gva_2050.csv" "Geneva" 2050
VISUALISATION_MORGES_2024_ARG = plot_2024 "internal/physic_pred_Morges_2024.csv" "internal/stat_pred_morges_2024.csv" "datas/temperature_data/morges.csv" "Morges" 2024
VISUALISATION_MORGES_2050_ARG = plot_2050 "internal/physic_pred_Morges_2050.csv" "internal/stat_pred_morges_2050.csv" "Morges" 2050
VISUALISATION_FINALE_GVA_ARG = plot_2024_vs_2050 "internal/physic_pred_Geneva_2024.csv" "internal/physic_pred_Geneva_2050.csv" "Geneva"
VISUALISATION_FINALE_MORGES_ARG = plot_2024_vs_2050 "internal/physic_pred_Morges_2024.csv" "internal/physic_pred_Morges_2050.csv" "Morges"

### --- Line command (target) to compile the C file --- ###
physic_compile: $(PHYSIC_FILE)
	$(CC) $(PHYSIC_FILE) $(CFLAGS) $(LIBS) $(OUT) $(basename $(PHYSIC_FILE))

physic_execute: 
	./$(basename $(PHYSIC_FILE))

### --- Targets to run the Python files --- ###
map_lake_python:
	$(PYTHON) $(MAP_LAKE_FILE) $(MAP_ARGS)

temp_prediction_python:
	$(PYTHON) $(TEMPERATURE_STAT_PREDICTION_FILE) $(PREDICTION_2024_ARGS)

visualisation_temp_prediction_python:
	$(PYTHON) $(DISPLAY_STAT_FILE) $(DISPLAY_2024_ARGS)

real_temp_python:
	$(PYTHON) $(REAL_TEMP_FILE) $(REAL_ARGS)

visualisation_real_temp_python:
	$(PYTHON) $(DISPLAY_STAT_FILE) $(DISPLAY_real_ARGS)

polynomial_regression_morges_python:
	$(PYTHON) $(POLYNOMIAL_REGRESSION_FILE) $(POLYNOMIAL_REGRESSION_MORGES_ARG)

pred_temp_gva_2024_python:
	$(PYTHON) $(TEMPERATURE_STAT_PREDICTION_FILE) $(TEMPERATURE_STAT_PREDICTION_GVA_2024_ARG)

visualisation_gva_2024_python:
	$(PYTHON) $(VISUALISATION_FILE) $(VISUALISATION_GVA_2024_ARG)

pred_temp_gva_2050_python:
	$(PYTHON) $(TEMPERATURE_STAT_PREDICTION_FILE) $(TEMPERATURE_STAT_PREDICTION_GVA_2050_ARG)

visualisation_gva_2050_python:
	$(PYTHON) $(VISUALISATION_FILE) $(VISUALISATION_GVA_2050_ARG)

visualisation_finale_gva_python:
	$(PYTHON) $(VISUALISATION_FILE) $(VISUALISATION_FINALE_GVA_ARG)

pred_temp_morges_2024_python:
	$(PYTHON) $(TEMPERATURE_STAT_PREDICTION_FILE) $(TEMPERATURE_STAT_PREDICTION_MORGES_2024_ARG)

visualisation_morges_2024_python:
	$(PYTHON) $(VISUALISATION_FILE) $(VISUALISATION_MORGES_2024_ARG)

pred_temp_morges_2050_python:
	$(PYTHON) $(TEMPERATURE_STAT_PREDICTION_FILE) $(TEMPERATURE_STAT_PREDICTION_MORGES_2050_ARG)

visualisation_morges_2050_python:
	$(PYTHON) $(VISUALISATION_FILE) $(VISUALISATION_MORGES_2050_ARG)

visualisation_finale_morges_python:
	$(PYTHON) $(VISUALISATION_FILE) $(VISUALISATION_FINALE_MORGES_ARG)

# Clean target to remove compiled files
clean:
	rm -f $(basename $(PHYSIC_FILE))

.PHONY: all clean


#vérifier et traduire poly reg + meillleurs nom
#pd.read ( quote = "") ???
