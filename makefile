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
#C_FILE = Code/Computations.c

# Specify the name of your Python files
MAP_FILE = code/map.py #path_data, path_dest, path_results
PREDICTION_FILE = code/predictions_stat.py #
REEL_FILE = code/reel_temp_stat.py #
DISPLAY_FILE = code/display.py #predicted_data_path, interior_points_path, path_results

### ------ Default target -> order in which you want the files to be run this is what will actually happen in your terminal ------ ###
all: run_first_python run_second_python run_third_python #run_4_python run_5_python run_6_python run_7_python run_8_python run_9_python clean 
#compile_c
# Arguments for map.py
MAP_ARGS = "datas/harbor.csv"  "internal/interior_points.csv" "results/map_template.png"
PREDICTION_winter_2025_ARGS = predict_folder "datas/temperature_data" "01/01/2025" 'internal/temp_predictions_winter2025.csv'
PREDICTION_summer_2025_ARGS = "datas/temperature_data" "27/07/2025" './internal/temp_predictions_summer2025.csv'
PREDICTION_2024_ARGS = "datas/temperature_data" "01/01/2025" './internal/temp_predictions_01_01_2024.csv'
REEL_ARGS = 'datas/temperature_data' '01/01/2024' 'internal/reel_temp_01_01_2024.csv'
DISPLAY_winter_ARGS = 'internal/temp_predictions_winter2025.csv' "internal/interior_points.csv" "results/lake_winter2025.png"
DISPLAY_summer_ARGS = './internal/temp_predictions_summer2025.csv' "internal/interior_points.csv" "./results/lake_summer2025.png"
DISPLAY_2024_ARGS = './internal/temp_predictions_01_01_2024.csv' "internal/interior_points.csv" "./results/lake_01_01_2024.png"
DISPLAY_reel_ARGS = 'internal/reel_temp_01_01_2024.csv' "internal/interior_points.csv" "./results/lake_reel_01_01_2024.png"

### --- Line command (target) to compile the C file --- ###
#compile_c: $(C_FILE)
#	$(CC) $(C_FILE) $(CFLAGS) $(LIBS) $(OUT) $(basename $(C_FILE))

### --- Target to run the Python files --- ###
run_first_python:
	$(PYTHON) $(MAP_FILE) $(MAP_ARGS)

run_second_python:
	$(PYTHON) $(PREDICTION_FILE) $(PREDICTION_winter_2025_ARGS)

run_third_python:
	$(PYTHON) $(DISPLAY_FILE) $(DISPLAY_winter_ARGS)

run_4_python:
	$(PYTHON) $(PREDICTION_FILE) $(PREDICTION_summer_2025_ARGS)

run_5_python:
	$(PYTHON) $(DISPLAY_FILE)$(DISPLAY_summer_ARGS)

run_6_python:
	$(PYTHON) $(PREDICTION_FILE)$(PREDICTION_2024_ARGS)

run_7_python:
	$(PYTHON) $(DISPLAY_FILE)$(DISPLAY_2024_ARGS)

run_8_python:
	$(PYTHON) $(REEL_FILE)$(REEL_ARGS)

run_9_python:
	$(PYTHON) $(DISPLAY_FILE)$(DISPLAY_2024_ARGS)


# Clean target to remove compiled files
clean:
	rm -f $(basename $(C_FILE))


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
