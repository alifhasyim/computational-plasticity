# -*- coding: utf-8 -*-
"""
Created on Sun May  4 14:30:52 2025

@author: Bagus Alifah Hasyim
"""
import matplotlib.font_manager as fm
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pathlib import Path



class TensileTestVisualization:
    def __init__(self, input_directory: Path, output_path: Path, data_names: dict,
                 gauge_length: float, cross_section_area: float):
        """
        Initialize the visualization with filenames and physical parameters.
        """
        self.input_directory = input_directory
        self.output_path = output_path
        self.data_names = data_names
        self.gauge_length = gauge_length
        self.cross_section_area = cross_section_area
        self.datasets = []

    def read_input_data(self):
        """
        Read the input data and convert it into stress-strain data sets.
        """
        for label, filename in self.data_names.items():
            file_path = self.input_directory / filename
            if not file_path.exists():
                raise FileNotFoundError(f"Missing file: {file_path}")
            
            print(f"Reading: {file_path}")
            df = pd.read_csv(file_path, delim_whitespace=True, header=None)
            df.columns = ['elongation_mm', 'force_mm']

            df["strain"] = df["elongation_mm"] / self.gauge_length
            df["stress"] = df["force_mm"] / self.cross_section_area

            self.datasets.append({
                "label": label,
                "strain": df["strain"],
                "stress": df["stress"]
            })

    def plot_and_export(self):
        """
        Plot the stress-strain curves and export the figure.
        """
        plt.rcParams['font.family'] = 'Times New Roman'
        plt.rcParams.update({
            'font.size': 16,
            'axes.titleweight': 'bold',
            'axes.labelsize': 16,
            'xtick.labelsize': 16,
            'ytick.labelsize': 16,
            'legend.fontsize': 16,
            'legend.title_fontsize': 24
        })

        plt.figure(figsize=(12, 8))
        line_formats = ['-o', '--x', '-.^', '-']
        for i, data in enumerate(self.datasets):
            fmt = line_formats[i % len(line_formats)]
            plt.plot(data["strain"], data["stress"], fmt, label=data["label"])

        plt.title("Stress-Strain Curve for Plane Stress and Plane Strai Condition")
        plt.xlabel("Engineering Strain")
        plt.ylabel("Stress (MPa)")

        # Add label on maximum value for each graph
        for data in self.datasets:
            max_idx = data["stress"].idxmax()
            max_stress = data["stress"].iloc[max_idx]
            stress_unit = "MPa"  # Change this as needed
            # Place the label below the max point
            plt.annotate(
            f"Max: {max_stress:.1f} {stress_unit}",
            xy=(data["strain"].iloc[max_idx], max_stress),
            xytext=(data["strain"].iloc[max_idx], max_stress - 0.1 * max_stress),
            arrowprops=dict(arrowstyle="->", color="black"),
            fontsize=14,
            ha='right',
            va='top'
            )
        plt.legend(loc='lower right', title="Method of Curve Extraction")
        plt.grid(True, which='both', linestyle='--', linewidth=0.7, alpha=0.7)
        plt.minorticks_on()

        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(self.output_path)
        print(f"Plot saved to: {self.output_path}")


def main():
    # Go 2 levels up from /src/ to project root
    
    project_root = Path(__file__).resolve().parents[2]

    input_directory = project_root / "visualize_tensileGraph" / "resources"
    output_plot_path = project_root / "visualize_tensileGraph" / "res" / "comparison_planeStress_planeStrain.png"
    
    file_names = {
        "Plane Stress": "Calculated_PlaneStress.dat",
        "Plane Strain": "Calculated_PlaneStrain.dat"
    }

    cross_section_mm2 = 1 
    specimen_length_mm = 1

    proc = TensileTestVisualization(input_directory,
                                    output_plot_path,
                                    file_names,
                                    specimen_length_mm,
                                    cross_section_mm2)
    proc.read_input_data()
    proc.plot_and_export()

if __name__ == "__main__":
    main()
    print("Successfully completed the tensile test visualization.")
        
        
        
        