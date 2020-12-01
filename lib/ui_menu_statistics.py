from lib.ui_base import prompt_continue
from lib.ui_utilities import inform_if_data_unavailable
from lib.statistics import print_statistics


def display_statistics(state):
    """
    Show statistics on aggregated data
    Does not continue if there is no data available.
    """
    #If no data is unavailable, inform user and return
    if inform_if_data_unavailable(state.aggregated_zones):
        return


    #Calculate and print statistics on aggregated data
    print_statistics(*state.aggregated_data)
    
    #Print aggregation mode and measurement unit
    for s in state.status:
        print(s)


    #Prompt user to continue once ready
    prompt_continue(start_newline=True)
