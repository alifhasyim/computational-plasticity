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
            'legend.fontsize': 18,
            'legend.title_fontsize': 18
        })

        plt.figure(figsize=(12, 8))
        line_formats = ['-o', '--x', '-.^', '-']
        for i, data in enumerate(self.datasets):
            fmt = line_formats[i % len(line_formats)]
            plt.plot(data["strain"], data["stress"], fmt, label=data["label"])

        plt.title("Stress-Strain Curve for Plane Stress Condition")
        plt.xlabel("Strain (mm/mm)")
        plt.ylabel("Stress (MPa)")

        # Annotate max points for each curve
        for i, data in enumerate(self.datasets):
            max_idx = data["stress"].idxmax()
            max_strain = data["strain"].iloc[max_idx]
            max_stress = data["stress"].iloc[max_idx]
            stress_unit = "MPa"
            # Place annotation inside the graph, slightly below and to the right of the max point
            xytext = (max_strain + 0.01, max_stress - 0.1 * abs(max_stress))
            va, ha = 'top', 'right'
            plt.annotate(
            f"Max: {max_stress:.1f} {stress_unit}",
            xy=(max_strain, max_stress),
            xytext=xytext,
            arrowprops=dict(arrowstyle="->", color="black"),
            fontsize=14,
            ha=ha,
            va=va
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
    output_plot_path = project_root / "visualize_tensileGraph" / "res" / "comparison_direct_calculated.png"
    
    file_names = {
        "Direct Stress-Strain Extraction": "Direct_PlaneStress.dat",
        "Calculated from Force-Diplacement ": "Calculated_PlaneStress.dat"
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
        
        
        
        