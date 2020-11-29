from lib.ui_base import prompt_continue
from lib.data import file_exists, dataLoad

from os import getcwd, path


def display_load_data_menu(state):
    """
    Prompt user to input a file path and then loads the contents into the program state.
    If unable to load the file, program state is not changed.
    """
    
    #Prompt for file path
    print("Input data file path:")
    data_path = input(getcwd() + path.sep)
    
    #If file exists, load data
    if file_exists(data_path):
        #Load data
        print("Loading data...")
        state.raw_data = dataLoad(data_path)
        
        #Filter data using the active filters
        print("Loaded data")
        state.filtered_data = state.filters.apply(state.raw_data)

        #Prompt user to contiue
        prompt_continue()
    #Else, inform user of failure, prompt to continue
    else:
        prompt_continue("Path does not lead to a file - press enter to continue...", start_newline=True)
