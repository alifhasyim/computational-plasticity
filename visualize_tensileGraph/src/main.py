# -*- coding: utf-8 -*-
"""
Created on Sun May  4 13:45:45 2025

@author: Bagus Alifah Hasyim
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

class TensileTestProcessor:
    def __init__(self, file_names: dict, cross_section_mm2: float, specimen_length_mm: float):
        """
        Initializes the processor with filenames and physical parameters.
        Assumes all files are in the '../resources/' directory relative to the script.
        """
        self.resource_dir = os.path.join("..", "resources")
        self.file_names = file_names
        self.cross_section_mm2 = cross_section_mm2
        self.specimen_length_mm = specimen_length_mm
        self.datasets = []

    def read_and_process(self):
        """
        Reads all input files and converts them to stress-strain datasets.
        """
        for label, filename in self.file_names.items():
            file_path = os.path.join(self.resource_dir, filename)
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Missing file: {file_path}")

            print(f"Reading: {file_path}")
            df = pd.read_csv(file_path, delim_whitespace=True, header=None)
            df.columns = ['elongation_mm', 'force_N']

            df["strain"] = df["elongation_mm"] / self.specimen_length_mm
            df["stress"] = df["force_N"] / self.cross_section_mm2

            self.datasets.append({
                "label": label,
                "strain": df["strain"],
                "stress": df["stress"]
            })

    def plot_and_export(self, output_path: str):
        """
        Plots the stress-strain curves, displays them, and saves the result as a PNG.
        """
        plt.figure(figsize=(10, 6))
        line_formats = ['-o', '--x', '-.^', '-']
        for i, data in enumerate(self.datasets):
            fmt = line_formats[i % len(line_formats)]
            plt.plot(data["strain"], data["stress"], fmt, label=data["label"])

        plt.title("Exercise 2: Stress-Strain Curve from Tensile Test")
        plt.xlabel("Engineering Strain")
        plt.ylabel("Stress (MPa)")
        plt.legend()
        plt.grid(True)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        plt.savefig(output_path)
        print(f"Plot saved to: {output_path}")
        
        plt.show()  # Show the plot window

def main():
    # File names (relative to ../resources/)
    file_names = {
        "Anisotropic 0°": "Anisotropic_0.dat",
        "Anisotropic 45°": "Anisotropic_45.dat",
        "Anisotropic 90°": "Anisotropic_90.dat",
        "Isotropic": "isotropic_tensile.dat"
    }

    # Physical properties
    cross_section_mm2 = 10 * 40
    specimen_length_mm = 200
    output_plot_path = "../res/"

    # Run processor
    processor = TensileTestProcessor(file_names, cross_section_mm2, specimen_length_mm)
    processor.read_and_process()
    processor.plot_and_export(output_plot_path)

if __name__ == "__main__":
    main()


