from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


#Define axis label style for subplots
axis_label_style = { "fontsize": 12, "fontweight": "bold" }

#Define size of plot GUI
plot_size = (16, 7)

#Define time formats
hour_format = "{:02d}:{:02d}"
date_format = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}"


def times_to_axis(times):
    """
    Convert times to a format usable as axis tick labels.
    If times are in hour format, converts to 24-hour strings.
    Else converts to "datetime" objects.
    
    Returns a tuple "(axis_times, hour_mode)".
    """
    #Hour mode if there are 24 times and no date information
    hour_mode = len(times) == 24 and np.all(times[:, 0:3] == 0)
    
    #If hour mode, convert to 24-hour strings
    if hour_mode:
        axis_times = [hour_format.format(*time[3:5])
                      for time in times]
    #Else, convert times to "datetime" objects
    else:
        axis_times = [datetime.strptime(date_format.format(*time), 
                                        "%Y-%m-%dT%H:%M:%S")
                      for time in times]

    #Return converted times and whether times are in hour mode
    return (axis_times, hour_mode)


def set_axis_labels(fig, x_label, y_label):
    """
    Set axis labels
    """
    fig.set_xlabel(x_label, **axis_label_style)
    fig.set_ylabel(y_label, **axis_label_style)

def style_x_labels(fig):
    """
    Rotate x-axis tick labels to prevent overlap and set font size.
    """
    for label in fig.get_xticklabels():
        label.set_rotation(36)
        label.set_fontsize(9)



def draw_bar_plot(fig, x, y, labels):
    """
    Draw a bar plot based off of the given data.
    """

    #Convert times to a displayable format
    (x_times, hour_mode) = times_to_axis(x)


    #Draw horizontal grid lines behind data
    fig.yaxis.grid(zorder=0)

    #Draw plot
    fig.bar(x_times, y, zorder=2)


    #If necessary, enable processing of "datetime" objects on the x-axis
    if not hour_mode:
        fig.xaxis_date()


    #Label and style plot
    set_axis_labels(fig, *labels)
    style_x_labels(fig)


def draw_line_plot(fig, x, y, labels):
    """
    Draw a line plot based off of the given data.
    """

    #Convert times to a displayable format
    (x_times, hour_mode) = times_to_axis(x)


    #Draw grid lines
    fig.grid(zorder=0)

    #Draw plot
    fig.plot(x_times, y, "-", label=None, zorder=2)
    
    
    #If necessary, enable processing of "datetime" objects on the x-axis
    if not hour_mode:
        fig.xaxis_date()


    #Label and style plot
    set_axis_labels(fig, *labels)
    style_x_labels(fig)



def draw_zones(times, zones, plot_drawer, labels):
    """
    Divide plot into four subplots and draw plots for usage in each zone.
    """
    #Divide into four subplots
    fig, (fig_zones) = plt.subplots(2, 2)
    #Set size and spacing
    fig.subplots_adjust(bottom=0.18, hspace=1.1)
    fig.set_size_inches(*plot_size)
    
    #For each zone, draw its associated plot and title
    for i, fig_zone in enumerate(fig_zones.reshape(-1)):
        #Set title of plot for zone
        fig_zone.set_title(f"Zone {i+1} energy usage by time", **axis_label_style)
        #Draw plot for zone
        plot_drawer(fig_zone, times, zones[:, i], labels)


def draw_combined(times, zones, plot_drawer, labels):
    """
    Draw one big plot for the combined usage of the zones
    """
    #Create one big plot area
    fig, (fig_combined) = plt.subplots(1, 1)
    #Set size and spacing
    fig.subplots_adjust(bottom=0.24)
    fig.set_size_inches(*plot_size)
    
    #Set title of plot
    fig_combined.set_title("Combined energy usage by time", **axis_label_style)
    #Draw plot of combined usage
    plot_drawer(fig_combined, times, zones.sum(axis=1), labels)



def show_plot(times, zones, combined, labels):
    """
    Shows a GUI of the energy usage. 
    If "combined" is "False" each zone will be shown in their own plots,
    else, the combined usage will be plotted.
    If there are less than 25 measurements, bar plots will be used instead of line plots.
    NOTE: Blocks thread while the GUI is open.
    """

    #Inform user of current action
    print("Loading plots...")

    #If less than 25 aggregated data points, draw bar plots
    if len(times) < 25:
        plot_drawer = draw_bar_plot
    #Else, draw line plots
    else:
        plot_drawer = draw_line_plot

    #If zone energy usage should be shown combined, draw combined plot
    if combined:
        draw_combined(times, zones, plot_drawer, labels)
    #Else, draw plots for each zone
    else:
        draw_zones(times, zones, plot_drawer, labels)


    #Print instructions for how to continue
    print("Close plots window to continue...", end="\n\n")


    #Show finished plot
    #NOTE: Blocks thread until GUI is closed
    plt.show()
