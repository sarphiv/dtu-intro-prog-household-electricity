from lib.ui_base import prompt_continue, prompt_options
from lib.data import file_exists, load_measurements
from lib.aggregate import aggregate_sort_data

from os import getcwd, path


def data_loader_action(state, path, fmode):
    """
    Informs user data is being loaded and then loads raw data into program state with the specified fill mode.
    """
    return lambda: print("Loading data...") or state.set_raw_data(load_measurements(path, fmode))


def display_load_data_menu(state):
    """
    Prompt user to input a file path and then loads the contents into the program state.
    If unable to load the file, program state is not changed.
    """
    
    #Prompt for file path
    print("Input data file path:")
    data_path = input(getcwd() + path.sep)

    #Print empty line for readability
    print()


    #If file exists, load data
    if file_exists(data_path):
        #Create helper function to load data with different fill modes
        dl_action = lambda fmode: data_loader_action(state, data_path, fmode)
        
        #Create fill mode menu
        fill_mode_menu = [
            ("Fill corrupted with latest valid", dl_action("forward fill")),
            ("Fill corrupted with next valid",   dl_action("backward fill")),
            ("Drop corrupted",                   dl_action("drop"))
        ]

        #Prompt for fill mode and load data
        prompt_options(fill_mode_menu)

        #Finished loading data
        print("Loaded data", end="\n\n")

        #Aggregate data
        aggregate_sort_data(state)


        #Prompt user to contiue
        prompt_continue()
    #Else, inform user of failure, prompt to continue
    else:
        prompt_continue("Path does not lead to a file - press enter to continue...", start_newline=True)
