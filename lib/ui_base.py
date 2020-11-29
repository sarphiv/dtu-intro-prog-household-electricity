from lib.utilities import parse_float, parse_int


def coalesce_default_msg(msg, default_msg, start_newline=True):
    """
    Does null coalescence on the provided message with the default message.
    """
    return ('\n' if start_newline else '') + (default_msg if msg == None else msg)

def coalesce_inline_msg(inline_msg, start_newline=False):
    """
    Does null coalescence on the provided inline mesage.
    """
    return coalesce_default_msg(inline_msg, "> ", start_newline=start_newline)



def print_status(status = []):
    """
    Prints the active status strings on individual lines.
    """
    #If there are active statuses, show them
    if (len(status) != 0):
        #Print status heading
        print("STATUS", end="\n  ")
        #Print each status on a new line
        print("\n  ".join(status))


def prompt_continue(msg = None, start_newline=False, end_newline=True):
    """
    Prompts user to press enter to continue.
    Prompt message can optionally be changed.
    The other optional parameters allow adding additional new lines before and after the prompt.
    """
    #If new line at start should be printed, print it
    if start_newline:
        print()

    #Prompt user to press enter to continue
    input(coalesce_default_msg(msg, "Press enter to continue...", start_newline=False))

    #If new line at end should be printed, print it
    if end_newline:
        print()


def prompt_options(options, status = [], msg = None, inline_msg = None):
    """
    Prompts user to choose between the provided options given as [(str, function), ...], where function has arity 0.
    Active statuses can optionally be provided as a string array [str, ...].
    The prompt message and inline prompt message can optionally be set.
    """
    
    #Attempt input until input is valid
    while True:
        #Show active statuses
        print_status(status)

        #Prompt and show 1-indexed options
        #NOTE: Prints an extra empty line at the start if there are status messages
        print(coalesce_default_msg(msg, "Choose an option:", start_newline=len(status) > 0))
        for i, option in enumerate(options):
            print(f"  {i + 1}) {option[0]}")

        #Ask user for input
        raw_input = input(coalesce_inline_msg(inline_msg, start_newline=True))
        #Print empty line for readability
        print()

        #Parse input
        #Attempt parsing raw input to int
        parsed_input = parse_int(raw_input)
    
        #If input is a valid option, break out of loop
        #NOTE: Not an off by one error, input is shifted by one
        if (parsed_input is not None) and (0 < parsed_input <= len(options)):
            #Shift parsed input back by one to be zero-indexed
            parsed_input -= 1
            break
        
        #Input was invalid, output error and reattempt input
        prompt_continue("Invalid option - press enter to try again...")


    #Valid option was chosen, call option function
    #NOTE: Increases height of call stack quite a bit if menus become deep.
    # But it is 2020 so we have way more than enough space.
    options[parsed_input][1]()


def prompt_range(status = [], msg = None, inline_msg = None):
    while True:
        #Show active statuses
        print_status(status)

        #Prompt for minimum value
        #NOTE: Prints an extra empty line at the start if there are status messages
        print(coalesce_default_msg(msg, "Input minimum (inclusive) value:", start_newline=len(status) > 0))
        raw_min = input(coalesce_inline_msg(inline_msg))
        
        #Attempt parsing minimum value
        parsed_min = parse_float(raw_min)
        #If failed, reattempt input from the start
        if parsed_min is None:
            prompt_continue("Invalid minimum value - press enter to try again...")
            continue

        #Prompt for maximum value
        print(coalesce_default_msg(msg, "Input maximum (exclusive) value:"))
        raw_max = input(coalesce_inline_msg(inline_msg))
        
        #Attempt parsing maximum value
        parsed_max = parse_float(raw_max)
        #If failed, reattempt input from the start
        if parsed_max is None:
            prompt_continue("Invalid maximum value - press enter to try again...")
            continue


        #If range is empty, reattempt input from the start
        if parsed_min >= parsed_max:
            prompt_continue("Maximum value must be greater than minimum value - press enter to try again...")
            continue


        #Return value range end points
        return (parsed_min, parsed_max)
