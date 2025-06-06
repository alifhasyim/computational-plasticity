# -*- coding: utf-8 -*-
"""
Created on Sun May  4 14:30:52 2025

@author: Bagus Alifah Hasyim
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

class TensileTestVisualization:
    def __init__(self, input_directory:str, output_directory:str, data_names:dict, gauge_length:float,
                 cross_section_area:float):
        """
        Initialize the visualization with filenames and physical parameters.
        All files located in '../resources' directory.
        """
        # Define all of the utilized directories
        self.input_directory = input_directory
        self.output_directory = output_directory
        
        # Set the file names list
        self.data_names = data_names
        
        # Define the experiment parameter
        self.gauge_length = gauge_length
        self.cross_section_area = cross_section_area
        
        # Initialize empty data
        self.datasets = [] 
    
    def read_input_data(self):
        """
        Read the input data and converts into stress-strain data sets.
        """
        # iterate all of the filename with the labeling of each tensile test variations
        for label, filename in self.data_names.items():
            file_path = os.path.join(self.input_directory, filename)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Missing file: {file_path}")
                
            # Read the input data and rename the axis
            print(f"Reading: {file_path}")
            df = pd.read_csv(file_path, delim_whitespace=True, header=None)
            df.columns = ['elongation_mm', 'force_mm'] # for x, y axis
            
            # Create new processed data frame
            df["strain"] = df["elongation_mm"] / self.gauge_length
            df["stress"] = df["force_mm"] / self.cross_section_area
            
            # Append all of the data points into the datasets container for each variation
            self.datasets.append({
                "label": label,
                "strain": df["strain"],
                "stress": df["stress"]
                })
                  
    def plot_and_export(self,output_path:str):
        """
        Plot all of the processed data and export to the '../res' directory as png format.
        """
        # Set global font properties
        plt.rcParams.update({
        'font.family': 'Times new roman',        # Choose your desired font family 
        'font.size': 16,                         # Set font size for all elements
        'axes.titleweight': 'bold',              # Set title weight (e.g., 'bold')
        'axes.labelsize': 16,                    # Set xlabel and ylabel font size
        'xtick.labelsize': 16,                   # Set x-axis tick label size
        'ytick.labelsize': 16,                   # Set y-axis tick label size
        'legend.fontsize': 16,                   # Set legend font size
        'legend.title_fontsize': 18              # Set legend title font size
            })
        
        plt.figure(figsize=(12,8))
        line_formats = ['-o', '--x', '-.^', '-']
        for i, data in enumerate(self.datasets): #there will be 4 dataset in total
            formats = line_formats[i % len(line_formats)]
            plt.plot(data["strain"], data["stress"], formats, label=data["label"])
        
        plt.title("Exercise 2: Stress-Strain Curve from Tensile Test")
        plt.xlabel("Engineering Strain")
        plt.ylabel("Stress (MPa)")
        plt.legend(loc='lower right', title="Material Type")
        plt.grid(True)
        
        plt.savefig(output_path)
        print(f"Plot saved to: {output_path}")
        plt.show()  # Show the plot window

def main():
    # File names (relative to ../resources/)
    file_names = {
        "Direct Stress-Strain Extraction": "Direct_PlaneStress.dat",
        "Calculated Force-Displacement": "Calculated_PlaneStress.dat"
    }

    # Physical properties
    cross_section_mm2 = 1 * 20
    specimen_length_mm = 20
    input_directory = "../resources/"
    output_plot_path = "../visualized_tensileGraph/res/comparison_direct_calculated.png"

    # Run Visualization process
    proc = TensileTestVisualization(input_directory, 
                                    output_plot_path, 
                                    file_names, 
                                    specimen_length_mm, 
                                    cross_section_mm2)
    proc.read_input_data()
    proc.plot_and_export(output_plot_path)

if __name__ == "__main__":
    main()
        
        
        
        