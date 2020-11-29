from lib.ui_base import prompt_continue, prompt_options
from lib.ui_utilities import inform_if_data_unavailable
from lib.statistics import statistic_descriptions, dataStatistics


def display_statistics_menu(state, menu):
    """
    Enters a menu allowing the user to select which statistic
    to calculate on the filtered data.
    Does not continue if there is no data available.
    """
    #If no data is unavailable, inform user and return
    if inform_if_data_unavailable(state.filtered_data):
        return
    
    #Prompt user to choose which calculation to execute
    prompt_options(menu, state.filters.as_descriptions())


def display_statistic(state, statistics_menu, statistic):
    """
    Executes a statistical calculation on the filtered data,
    and outputs the results to the user.
    """
    #Get normalized name of the statistic to calculate
    stat_key = statistic.casefold()

    #Print description of statistic
    print(statistic_descriptions[stat_key])
    #Print result of the calculation of the statistic on the filtered data
    print(f"{statistic}: {dataStatistics(state.filtered_data, stat_key)}")

    #Prompt user to continue after having read the result
    prompt_continue(start_newline=True)

    #Go back to statistics menu
    display_statistics_menu(state, statistics_menu)