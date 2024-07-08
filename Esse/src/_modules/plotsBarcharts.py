from all_imports import *

from .helper import print_log_separator
from .plotUtils import interpolate_colors

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap, Normalize
from matplotlib.dates import DateFormatter
from typing import List, Union

#TODO Adjust all plots to this standard
def TLStandardClosedStackedBarchart(ax, df: pd.DataFrame, title: str, subtitle: str, xlabel: str, ylabel: str, colors: List[str], ymax: Union[str, int], legend: bool = True, yticks=None):
    # Create the stacked bar chart
    df.plot(kind='bar', stacked=False, color=colors, alpha=1, linewidth=1, edgecolor='white', width=0.99, ax=ax)
    
    # Add title and labels
    ax.set_title(title, fontsize=11, pad=34, loc='left', fontweight='bold')
    ax.set_xlabel(xlabel, loc='center', labelpad=10, fontsize=7)
    ax.set_ylabel(ylabel, loc='center', labelpad=10, fontsize=7)
    ax.text(0.0, 1.045, subtitle, ha='left', va='center', transform=ax.transAxes, fontsize=7)
    
    # Customize legend
    if legend:
        ax.legend(title='Metrics', title_fontsize='small', borderpad=0, edgecolor='white', bbox_to_anchor=(1.06, 0.0), loc='lower left', fontsize=7)
    
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha='center', fontsize=7)

    # Customize ticks
    if yticks is not None:
        ax.set_yticks(yticks[0])
        ax.set_yticklabels(yticks[1], fontsize=7)
    else:
        ax.set_yticks(ax.get_yticks())
        ax.set_yticklabels(ax.get_yticklabels(), fontsize=7)
    
    # Customize grid and spines
    ax.grid(axis='y', linestyle=(0, (1, 2)), alpha=0.5, color='#DDE2E6')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Set y-axis limit if ymax is provided
    if ymax is not None:
        ax.set_ylim(0, ymax)