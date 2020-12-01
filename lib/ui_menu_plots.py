from lib.ui_base import prompt_options
from lib.ui_utilities import inform_if_data_unavailable
from lib.plot import show_plot


def display_plots_menu(state):
    """
    Opens a GUI to show the aggregated data with plots.
    Does not continue if there is no data available.
    """

    #If no data is unavailable, inform user and return
    if inform_if_data_unavailable(state.aggregated_zones):
        return
    
    
    plots_menu = [
        ("Zone usage",     lambda: show_plot(*state.aggregated_data, combined=False, labels=state.status)),
        ("Combined usage", lambda: show_plot(*state.aggregated_data, combined=True,  labels=state.status))
    ]
    
    prompt_options(plots_menu, state.status)
