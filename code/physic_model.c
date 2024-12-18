#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#define YEARS 100       // Can be changed if we want to see the results on a larger scale
#define PERIOD 365       // 1 year
#define PI 3.141592653589793


// Definition of the structure to store location data

typedef struct {
    char location[50];    // Name of the location
    double latitude;      // Latitude of the location
    double altitude;      // Altitude in meters
    double continentality; // Continentality factor
    double temperature;    // Temperature value (to be calculated)
} Location;


int random_sign() {

    /**
 * Generates a random sign (+1 or -1).
 * This function is used to determine whether a temperature wave will increase or decrease the temperature.
 * */
    
    return (rand() % 2) * 2 - 1;
}


double random_normal(double mean, double stddev) {

    /**
 * Generates a random number from a normal distribution using the Box-Muller method.
 *
 * param mean: The mean of the normal distribution.
 * param stddev: The standard deviation of the normal distribution.
 * return double: A random value from the normal distribution.
 */
    
    // Variables for the Box-Muller method
    double u1, u2, z0;

    // Generate random values u1 and u2 in the range [0, 1]
    u1 = (rand() + 1.0) / (RAND_MAX + 1.0);
    u2 = (rand() + 1.0) / (RAND_MAX + 1.0);

    // Apply the Box-Muller transform
    z0 = sqrt(-2.0 * log(u1)) * cos(2.0 * PI * u2);

    // Return the generated number adjusted by mean and standard deviation
    return mean + z0 * stddev;
}


double random_uniform(double min, double max) {

    /**
 * Generates a random uniform number between two specified bounds.
 *
 * param min: The minimum bound.
 * param max: The maximum bound.
 * return double: A random number between min and max.
 */

    return min + (max - min) * ((double)rand() / RAND_MAX);
}


double MAET(Location* location) {

    /**
 * Calculates the Mean Annual Epilimnion Temperature (MAET) based on location parameters.
 * Uses the equation by Ottosson and Abrahamsson to calculate the temperature.
 *
 * param location: A pointer to a Location structure containing latitude, altitude, and continentality data.
 * return double: The calculated MAET for the given location, rounded to 5 decimal places.
 */

    // Ottosson and Abrahamsson equation
    double part1 = pow((750 / (90 - pow(location->latitude, 0.85))), 1.29);
    double part2 = 0.1 * pow(location->altitude, 0.5);
    double part3 = 0.25 * pow((pow(location->continentality, 0.9) + 500), 0.52);

    // Compute MAET and round it to 5 decimal places
    double maet = 44 - part1 - part2 - part3;
    location->temperature = round(maet * 100000) / 100000;

    return location->temperature;
}


double deltaT(int day) {

    /**
 * Calculates the temperature variation (deltaT) for a specific day of the year.
 * Models seasonal variations using a cosine function.
 *
 * param day: The day of the year (1–365).
 * return double: The temperature variation for the given day.
 */

    double max_delta_T = 13.0;  // Maximum temperature variation
    double min_delta_T = 4.0;   // Minimum temperature variation
    int peak_day = 172;         // Day of maximum variation (e.g., midsummer)

    // Compute delta_T using a cosine function to model seasonal variations
    double delta_T = (max_delta_T + min_delta_T) / 2.0 +
                     (max_delta_T - min_delta_T) / 2.0 *
                     cos((2.0 * PI / 365.0) * (day - peak_day) - PI / 6.0);

    return delta_T;
}


double Ts(double initial_T0, double rate, double delta_T, double period, double phase, int day, int year) {

    /**
 * Calculates the surface temperature for a given day and year based on a sinusoidal model.
 * Accounts for initial temperature, warming rate, seasonal variations, and day/year.
 *
 * param initial_T0: The initial temperature.
 * param rate: The warming rate per year.
 * param delta_T: The daily temperature variation.
 * param period: The period of the seasonal cycle (e.g., 365 days).
 * param phase: The phase offset in radians.
 * param day: The day of the year.
 * param year: The year number (e.g., 0 for the initial year (e.g. 2024)).
 * return double: The calculated temperature for the given day and year.
 */

    return initial_T0 + delta_T * sin((2 * PI / period) * day + phase) + rate * year;
}


void generate_waves(int* waves, int num_waves, int wave_duration, int max_days) {


/**
 * Generates non-overlapping random start days for temperature waves.
 * Ensures that the generated wave periods do not overlap.
 *
 * param waves: An array to store the start days of the waves.
 * param num_waves: The number of waves to generate.
 * param wave_duration: The duration of each wave in days.
 * param max_days: The maximum number of days in the period (e.g., 365 for one year).
 */

    for (int i = 0; i < num_waves; i++) {
        
        int day;
        int unique;
        do {
        
            unique = 1;
            day = rand() % (max_days - wave_duration);  // Generate a random day
        
            // Check for overlap with previously generated waves
            for (int j = 0; j < i; j++) {
        
                if (abs(day - waves[j]) < wave_duration) {
        
                    unique = 0;
                    break;
                }
            }
        } while (!unique);
        waves[i] = day;
    }
}


// Apply a temperature wave to the temperature on the given day

void apply_waves(int* waves, int num_waves, int wave_duration, int day, double* temperature, double min_amplitude, double max_amplitude) {

    /**
 * Applies temperature adjustments due to extreme temperature waves on a given day.
 * Adjusts the temperature value if the current day falls within the range of a wave.
 *
 * param waves: An array containing the start days of the waves.
 * param num_waves: The number of waves to consider.
 * param wave_duration: The duration of each wave in days.
 * param day: The current day of the year.
 * param temperature: A pointer to the temperature to adjust.
 * param min_amplitude: The minimum amplitude of the wave.
 * param max_amplitude: The maximum amplitude of the wave.
 */

    for (int i = 0; i < num_waves; i++) {

        // Cold or warm wave
        int sign = random_sign();

        // If the current day falls within a wave period
        if (day >= waves[i] && day < waves[i] + wave_duration) {
        
            double amplitude = random_uniform(min_amplitude, max_amplitude);
            *temperature += amplitude * sign;  // Adjust the temperature
            break;
        }
    }
}


double thermal_inertia(double initial_temp, double mean_temp, double inertia_factor) {

    /**
 * Applies thermal inertia to adjust the temperature towards the mean temperature.
 * This models the lag effect in temperature changes due to thermal inertia.
 *
 * param initial_temp: The initial temperature.
 * param mean_temp: The mean temperature.
 * param inertia_factor: The factor that determines the strength of inertia (between 0 and 1).
 * return double: The adjusted temperature after applying thermal inertia.
 */

    return initial_temp * (1 - inertia_factor) + inertia_factor * mean_temp;
}


double marine_currents(double initial_temp, double current_factor) {

    /**
 * Adjusts the temperature based on marine current effects.
 * This introduces random adjustments influenced by marine currents.
 *
 * param initial_temp:  The initial temperature.
 * param current_factor: The factor that determines the strength of the current's effect.
 * return double: The adjusted temperature after accounting for marine currents.
 */

    double adjustment = random_uniform(-0.5, 0.5) * current_factor;

    return initial_temp + adjustment;
}


int main() {

    /**
 * The main function initializes random seed, defines locations, and simulates temperatures.
 * Generates CSV files containing daily temperature data for each location over a specified period.
 * Models the effects of warming rates, noise, extreme temperature waves, thermal inertia, and marine currents.
 *
 * return int: Returns 0 if the program executes successfully.
 */

    srand(time(NULL));  // Initialize random number generator


    // Define locations
    Location morges = {"Morges", 46.503533903991766, 371.90, 0.01570};      // At the surface (0.2m depth), near the shore
    Location geneva = {"Geneva", 46.2110157511242656, 371.90, 0.14770};     // At the surface (0.2m depth), near the shore
    
    // List of locations
    Location locations[] = {morges, geneva};
    int num_locations = sizeof(locations) / sizeof(locations[0]);  // Number of locations


    // Model parameters
    double rate_of_warming = 0.05;          // Annual temperature increase rate (°C/year)
    double phase = 4*PI/3;              // Initial phase (in radians) adjusted to have the hooter day ≈ 1 august
    double daily_noise_factor = 0.5;        // Daily noise factor
    double year_noise_factor = 0.2;         // Yearly noise factor
    int num_short_waves = 24;          // Number of short extreme temperature waves
    int num_long_waves = 3;            // Number of long extreme temperature waves
    double short_wave_duration = 3;         // Duration of the short extreme temperature waves 
    double long_wave_durations = 4;         // Duration of the long extreme temperature wave
    double inertia_factor = 0.1;          // Inertia factor
    double current_factor = 0.4;          // Current factor


    // Loop through all locations and create a CSV file for each
    
    for (int i = 0; i < num_locations; i++) {
    
        Location *location = &locations[i];
        
        // Calculate the initial temperature for each location
        double initial_temp = MAET(location); // Initial mean annual temperature (°C)

        // Loop on the years

        for (int year = 0; year < YEARS; year++) {
            
            if (year == 0 || year == 26) {  // Choose 2024 and 2050

                double initial_noise_temp = initial_temp + random_normal(0, year_noise_factor);  // Initial mean annual temperature with noise (°C)

                // Create a CSV file for this location

                char filename[1000];
                snprintf(filename, sizeof(filename), "internal/physic_pred_%s_%d.csv", location->location, 2024 + year);
        
                FILE *file = fopen(filename, "w");
                if (file == NULL) {
                    printf("Error creating the CSV file for %s in %d.\n", location->location, 2024 + year);
                    continue;
                }

                // Generate the start days for temperature waves

                int short_waves[num_short_waves];
                int long_waves[num_long_waves];
                generate_waves(short_waves, num_short_waves, short_wave_duration, PERIOD);
                generate_waves(long_waves, num_long_waves, long_wave_durations, PERIOD);

                // Write the header to the CSV file
                
                fprintf(file, "day%d,temp_warming,temp_warming_noise,temp_warming_noise_extreme,temp_warming_noise_extreme_inertia,temp_warming_noise_extreme_inertia_currents\n", 2024 + year);
                
                // Loop on each day

                for (int t = 0; t < PERIOD; t++) { 
                
                    double dT = deltaT(t);  // Temperature variation (°C)

                    double temp_warming = Ts(initial_temp, rate_of_warming, dT, PERIOD, phase, t, year); // Temperature with climate change (°C)
                    
                    double daily_noise = random_normal(0, daily_noise_factor);  // Daily noise factor
                    
                    double temp_warming_noise = Ts(initial_noise_temp, rate_of_warming, dT, PERIOD, phase, t, year) + daily_noise; // Temperature with climate change and daily and yearly noise (°C)
                    
                    double temp_warming_noise_extreme = temp_warming_noise; // Temperature with warming, both noises and extremes events (after going trough the functions) (°C)

                    apply_waves(short_waves, num_short_waves, 3, t, &temp_warming_noise_extreme, 1.0, 3.0); // Apply the short temperature waves
                    apply_waves(long_waves, num_long_waves, 4, t, &temp_warming_noise_extreme, 3.0, 5.0);  // Apply the long temperature waves

                    double temp_warming_noise_extreme_inertia = thermal_inertia(temp_warming_noise_extreme, initial_noise_temp, inertia_factor);  // Temperature with warming, both noises, extremes events and inertia (°C)
                    
                    double temp_warming_noise_extreme_inertia_current = marine_currents(temp_warming_noise_extreme_inertia, current_factor);  // Temperature with warming, both noises, extremes events, inertia and currents (°C)

                    // Write data for each day into the CSV file

                    fprintf(file, "%d,%.5f,%.5f,%.5f,%.5f,%.5f\n", t + 1, temp_warming, temp_warming_noise, temp_warming_noise_extreme, temp_warming_noise_extreme_inertia, temp_warming_noise_extreme_inertia_current);
                }

                // Close the file

                fclose(file);

                printf("The data for %s in %d has been saved to '%s'.\n", location->location, 2024 + year, filename);
            }
        }
    }

    return 0;
}
