from lib.ui_utilities import inform_if_data_unavailable
from lib.plot import dataPlot


def display_plots(state):
    """
    Opens a GUI to show the filtered data with plots.
    Does not continue if there is no data available.
    """

    #If no data is unavailable, inform user and return
    if inform_if_data_unavailable(state.filtered_data):
        return

    #Show GUI with plots
    print("Close plots window to continue...", end="\n\n")
    dataPlot(state.filtered_data)
