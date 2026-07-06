"""
FatiguePostProcessor - Main Entry Point

This is the main startup file for the Fatigue Post Processor application.
It processes fatigue data files and performs analysis.
"""

import os
import csv
from ReadHistogram import (
    read_fatigue_data,
    calculate_N,
    calculate_fatigue,
    calculate_total_fatigue,
    calculate_lifespan
)

# Input folder path
input_folder = "Input"

# Design life
design_life = 20  # years

# Create output folder if it doesn't exist
output_folder = "Output"
os.makedirs(output_folder, exist_ok=True)

# Create output CSV file path
output_filepath = os.path.join(output_folder, "fatigue_results.csv")

# Prepare list to store results
results = []

# Process all files in the input folder
if os.path.exists(input_folder):
    files = sorted([f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))])

    for filename in files:
        filepath = os.path.join(input_folder, filename)

        try:
            # Read the data
            data = read_fatigue_data(filepath)

            # Calculate N values
            N_values = calculate_N(data)

            # Calculate fatigue values
            fatigue = calculate_fatigue(data, N_values)

            # Calculate total fatigue
            total_fatigue = calculate_total_fatigue(fatigue)

            # Calculate lifespan
            lifespan = calculate_lifespan(design_life, total_fatigue)

            # Store results
            results.append({
                'Input_File': filename,
                'Total_Fatigue': total_fatigue,
                'Lifespan_Years': lifespan
            })

        except Exception as e:
            # If file processing fails, record error
            results.append({
                'Input_File': filename,
                'Total_Fatigue': f'ERROR: {str(e)}',
                'Lifespan_Years': 'ERROR'
            })

# Write results to CSV file
with open(output_filepath, 'w', newline='') as csvfile:
    fieldnames = ['Input_File', 'Total_Fatigue', 'Lifespan_Years']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(results)
