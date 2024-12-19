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
#PYTHON = /opt/anaconda3/envs/cmt/bin/python

# Specify file names and their relative paths
PHYSIC_FILE = code/physic_model.c

# Specify the name of your Python files
MAP_LAKE_FILE = code/map.py
TEMPERATURE_STAT_PREDICTION_FILE = code/predictions_stat.py
REEL_TEMP_FILE = code/reel_temp_stat.py
DISPLAY_STAT_FILE = code/display.py
VISUALISATION_FILE = code/visualisation.py

### ------ Default target -> order in which you want the files to be run ------ ###
all: physic clean #run_first_python run_second_python run_third_python run_4_python run_5_python run_6_python run_7_python run_8_python run_9_python clean 

# Arguments for map.py
MAP_ARGS = "data/harbor.csv" "internal/interior_points.csv" "results/map_template.png"
PREDICTION_winter_2025_ARGS = "datas/temperature_data" "01/01/2025" "./internal/temp_predictions_winter2025.csv"
PREDICTION_summer_2025_ARGS = "datas/temperature_data" "27/07/2025" "./internal/temp_predictions_summer2025.csv"
PREDICTION_2024_ARGS = "datas/temperature_data" "01/01/2024" "./internal/temp_predictions_01_01_2024.csv"
REEL_ARGS = "datas/temperature_data" "01/01/2024" "internal/reel_temp_01_01_2024.csv"
DISPLAY_winter_ARGS = "./internal/temp_predictions_winter2025.csv" "internal/interior_points.csv" "./results/lake_winter2025.png"
DISPLAY_summer_ARGS = "./internal/temp_predictions_summer2025.csv" "internal/interior_points.csv" "./results/lake_summer2025.png"
DISPLAY_2024_ARGS = "./internal/temp_predictions_01_01_2024.csv" "internal/interior_points.csv" "./results/lake_01_01_2024.png"
DISPLAY_reel_ARGS = "internal/reel_temp_01_01_2024.csv" "internal/interior_points.csv" "./results/lake_reel_01_01_2024.png"

### --- Line command (target) to compile the C file --- ###
physic: $(PHYSIC_FILE)
	$(CC) $(PHYSIC_FILE) $(CFLAGS) $(LIBS) $(OUT) $(basename $(PHYSIC_FILE))

### --- Targets to run the Python files --- ###
run_first_python:
	$(PYTHON) $(MAP_LAKE_FILE) $(MAP_ARGS)

run_second_python:
	$(PYTHON) $(TEMPERATURE_STAT_PREDICTION_FILE) $(PREDICTION_winter_2025_ARGS)

run_third_python:
	$(PYTHON) $(DISPLAY_STAT_FILE) $(DISPLAY_winter_ARGS)

run_4_python:
	$(PYTHON) $(TEMPERATURE_STAT_PREDICTION_FILE) $(PREDICTION_summer_2025_ARGS)

run_5_python:
	$(PYTHON) $(DISPLAY_STAT_FILE) $(DISPLAY_summer_ARGS)

run_6_python:
	$(PYTHON) $(TEMPERATURE_STAT_PREDICTION_FILE) $(PREDICTION_2024_ARGS)

run_7_python:
	$(PYTHON) $(DISPLAY_STAT_FILE) $(DISPLAY_2024_ARGS)

run_8_python:
	$(PYTHON) $(REEL_TEMP_FILE) $(REEL_ARGS)

run_9_python:
	$(PYTHON) $(DISPLAY_STAT_FILE) $(DISPLAY_reel_ARGS)

# Clean target to remove compiled files
clean:
	rm -f $(basename $(PHYSIC_FILE))

.PHONY: all clean


#ordre 
#1. map
#2. pred été
#3 affihcer lac été
#4 pred hiver
#5 afficher lac hiver


#faire pred stat sur 1 an : morges 2024, 2050 et ovz 2024 et 2050

#ajt regression poly dans result

#mieux 1 date : 27 juillet 2024 = carte stat et reel
#carte du lac en hiver 01/01/2024 et ete 27/07/2004

# terminer graph data stat vs physique --> result 

#english + commenter 
