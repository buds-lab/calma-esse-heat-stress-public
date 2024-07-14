from all_imports import *

from .helper import print_log_separator
from .plotUtils import interpolate_colors

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap, Normalize
from matplotlib.dates import DateFormatter
from typing import List, Union

def StandartHeatmap(
    df: pd.DataFrame, 
    vmax: Union[float, int], 
    step_size: int = 5, 
    cmap: Union[List[str], ListedColormap] = ['#FFFFFF', '#000000'], 
    cbar_labels: List[Union[str, int]] = [],
    title: str = '', 
    subtitle: str = '', 
    xlabel: str = '', 
    ylabel: str = '',
    filepath: str = ''
):
    """
    Plot a heatmap with custom colors and other specified parameters.`
    
    Parameters:
    - df (pd.DataFrame): 2D DataFrame for heatmap data.
    - vmax (float or int): Maximum value for color intensity scaling.
    - step_size (int): Step size for color bar ticks.
    - cmap (list or ListedColormap): List of colors in hexadecimal format or a ListedColormap for custom colormap.
    - cbar_labels (list): List of labels for color bar ticks.
    - title (str): Title for the heatmap plot.
    - subtitle (str): Subtitle for additional information.
    - xlabel (str): Label for the x-axis.
    - ylabel (str): Label for the y-axis.
    """

    # if pd.api.types.is_datetime64_any_dtype(df.columns):
    #     df.columns = df.columns.strftime('%d.%m')

    if isinstance(cmap, list):
        custom_cmap = ListedColormap(cmap)
    else:
        custom_cmap = cmap

    cbar_ticks = list(range(0, vmax + step_size, step_size))
    norm = Normalize(vmin=0, vmax=vmax)

    plt.figure(figsize=(14, 10))
    ax = sns.heatmap(df, cmap=custom_cmap, cbar=True, linewidths=0.1, square=True, 
                        cbar_kws={'shrink': 0.375, 'ticks': cbar_ticks}, norm=norm)
    
    if cbar_labels:
        colorbar = ax.collections[0].colorbar
        colorbar.set_ticks(cbar_ticks)
        colorbar.set_ticklabels(cbar_labels, fontsize=7)
    
    #ax.xaxis.set_major_formatter(DateFormatter('%d.%m'))

    plt.xticks(rotation=90, ha='center', fontsize=7)
    plt.yticks(fontsize=7)
    plt.title(title, fontsize=11, pad=30, loc='left', fontweight='bold')
    plt.text(0.0, 1.07, subtitle, ha='left', va='center', transform=plt.gca().transAxes, fontsize=7)
    plt.xlabel(xlabel, loc='center', labelpad=10, fontsize=7)
    plt.ylabel(ylabel, loc='center', labelpad=10, fontsize=7)

    if filepath != "":
        directory = os.path.dirname(filepath)
        
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        plt.savefig(filepath, bbox_inches='tight', pad_inches=0.1)
        print(f"Plot saved to {filepath}")

    plt.show()

    display(df)
