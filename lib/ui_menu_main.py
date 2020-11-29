from lib.ui_base import prompt_options


def display_main_menu(state, menu):
    """
    Enters the main menu of the program.
    """
    
    #Always show main menu
    try:
        while True:
            prompt_options(menu, state.filters.as_descriptions())
    #Except break out when the user wants to close the program
    except SystemExit:
        pass
