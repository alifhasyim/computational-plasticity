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
        Plot the processed data and export it as a PNG image.
        """
        # Set font sizes and styles (for easy resizing)
        plt.rcParams.update({
            'font.family': 'Times New Roman',  # fallback (won't work directly)
            'font.size': 16,
            'axes.titleweight': 'bold',
            'axes.labelsize': 16,
            'xtick.labelsize': 16,
            'ytick.labelsize': 16,
            'legend.fontsize': 16,
            'legend.title_fontsize': 18
        })

        # Load Times New Roman manually via full path
        font_path = "/usr/share/fonts/truetype/msttcorefonts/times.ttf"
        font_size = plt.rcParams['font.size']
        font_prop = FontProperties(fname=font_path, size=font_size)

        plt.figure(figsize=(12, 8))
        line_formats = ['-o', '--x', '-.^', '-']
        for i, data in enumerate(self.datasets):
            fmt = line_formats[i % len(line_formats)]
            plt.plot(data["strain"], data["stress"], fmt, label=data["label"])

        plt.title("Exercise 2: Stress-Strain Curve from Tensile Test", fontproperties=font_prop)
        plt.xlabel("Engineering Strain", fontproperties=font_prop)
        plt.ylabel("Stress (MPa)", fontproperties=font_prop)
        plt.legend(loc='lower right', title="Material Type", prop=font_prop, title_fontproperties=font_prop)
        plt.xticks(fontproperties=font_prop)
        plt.yticks(fontproperties=font_prop)
        plt.grid(True)

        self.output_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure output directory exists
        plt.savefig(self.output_path)
        print(f"Plot saved to: {self.output_path}")
        plt.show()


def main():
    # Go 2 levels up from /src/ to project root
    
    project_root = Path(__file__).resolve().parents[2]

    input_directory = project_root / "visualize_tensileGraph" / "resources"
    output_plot_path = project_root / "visualize_tensileGraph" / "res" / "comparison_direct_calculated.png"
    
    file_names = {
        "Direct Stress-Strain Extraction": "Direct_PlaneStress.dat",
        "Calculated Force-Displacement": "Calculated_PlaneStress.dat"
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
        
        
        
        