from lib.ui_base import prompt_options
from lib.ui_utilities import inform_if_data_unavailable
from lib.plot import show_plot


def plot_shower(state, combined_plot):
    """
    Returns a function that opens a plot based on the given state and options.
    If "combined_plot" is true, a combined plot is shown, else the four zones are shown.
    """
    return lambda: show_plot(*state.aggregated_data, combined=combined_plot, labels=state.status)


def display_plots_menu(state):
    """
    Opens a GUI to show the aggregated data with plots.
    Does not continue if there is no data available.
    """

    #If no data is unavailable, inform user and return
    if inform_if_data_unavailable(state.aggregated_zones):
        return

    #Create menu to prompt user for plot type
    plots_menu = [
        ("Zone usage",     plot_shower(state, combined_plot=False)),
        ("Combined usage", plot_shower(state, combined_plot=True))
    ]

    #Prompt user for plot type and show plot afterwards
    prompt_options(plots_menu, state.status)
