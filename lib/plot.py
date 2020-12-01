from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import date2num, datestr2num
import numpy as np


#Define axis label style for subplots
axis_label_style = { "fontsize": 12, "fontweight": "bold" }

#Define size of plot GUI
plot_size = (16, 7)


clock_format = "{:02d}:{:02d}:{:02d}"
date_format = "{:04d}-{:02d}-{:02d}"


def times_to_axis(times):
    hour_mode = len(times) == 24 and np.all(times[:, 0:3] == 0)
    
    if hour_mode:
        axis_times = [clock_format.format(*time[3:])
                      for time in times]
    else:
        axis_times = [datetime.strptime(f"{date_format}T{clock_format}"
                                        .format(*time), 
                                        "%Y-%m-%dT%H:%M:%S")
                      for time in times]


    return (axis_times, not hour_mode)


def set_axis_labels(fig, x_label, y_label):
    #Set axis labels
    fig.set_xlabel(x_label, **axis_label_style)
    fig.set_ylabel(y_label, **axis_label_style)
    
def style_x_labels(fig):
    #Rotate x-axis tick labels and set font size
    #NOTE: Rotating because else some labels may overlap
    for label in fig.get_xticklabels():
        label.set_rotation(28)
        label.set_fontsize(9)


def draw_bar_plot(fig, x, y, labels):
    """
    Draw a bar plot with rotated x-labels and a grid
    """

    #Draw horizontal grid lines behind data
    fig.yaxis.grid(zorder=0)
    
    #Draw bar graph for input data
    #NOTE: matplotlib requires input to be a list
    (x_times, date_style) = times_to_axis(x)
    if date_style:
        fig.xaxis_date()
    fig.bar(x_times, y, zorder=2)
    

    set_axis_labels(fig, *labels)
    style_x_labels(fig)


def draw_line_graph(fig, x, y, labels):
    """
    Draw a combined point and dashed line graph based on the given points.
    """
    
    #Draw grid lines
    fig.grid(zorder=0)
    
    #Draw points and grey lines
    (x_times, date_style) = times_to_axis(x)
    if date_style:
        fig.xaxis_date()

    fig.plot(x_times, y, "-",  label=None, zorder=2)

    set_axis_labels(fig, *labels)
    style_x_labels(fig)


def draw_zones(times, zones, plot_drawer, labels):
    fig, (fig_zones) = plt.subplots(2, 2)
    fig.subplots_adjust(bottom=0.18, hspace=1.1)
    fig.set_size_inches(*plot_size)
    
    for i, fig_zone in enumerate(fig_zones.reshape(-1)):
        fig_zone.set_title(f"Zone {i+1} energy usage by time", **axis_label_style)
        plot_drawer(fig_zone, times, zones[:, i], labels)


def draw_combined(times, zones, plot_drawer, labels):
    fig, (fig_combined) = plt.subplots(1, 1)
    fig.subplots_adjust(bottom=0.24)
    fig.set_size_inches(*plot_size)
    
    fig_combined.set_title("Combined energy usage by time", **axis_label_style)
    plot_drawer(fig_combined, times, zones.sum(axis=1), labels)
    

def show_plot(times, zones, combined, labels):
    """
    Shows a GUI with number of entries for each species and a growth-temperature plot for each species.
    NOTE: Blocks thread while the GUI is open.
    """
    
    print("Loading plots...")

    if len(times) < 25:
        plot_drawer = draw_bar_plot
    else:
        plot_drawer = draw_line_graph

    if combined:
        draw_combined(times, zones, plot_drawer, labels)
    else:
        draw_zones(times, zones, plot_drawer, labels)


    print("Close plots window to continue...", end="\n\n")

    #Show finished plot
    #NOTE: Blocks thread until GUI is closed
    plt.show()
