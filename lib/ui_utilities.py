from lib.ui_base import prompt_continue


def display_previous_menu():
    """
    Does nothing to allow a prompt to "fall-though".
    This will make the prompt fall-through to the previous menu.
    """
    pass


def check_data_unavailable(data):
    """
    Returns true if data is unavailable or empty, else returns false.
    """
    return data is None or len(data) == 0


def inform_if_data_unavailable(data):
    """
    Informs user of data unavailability if there is no data.
    Returns true if data is unavailable, else returns false.
    """
    
    #If data is unavailable, inform and prompt user to continue.
    if check_data_unavailable(data):
        prompt_continue("Unable to execute operation.\n\
No data available after application of filters.\n\
Either load in more data or change the filters.\n\n\
Press enter to continue...")
        return True
    else:
        return False
