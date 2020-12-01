from lib.state import State
from lib.ui_menu_main import display_main_menu
from lib.ui_menu_data import display_load_data_menu
from lib.ui_menu_aggregate import display_aggregate_menu
from lib.ui_menu_statistics import display_statistics
from lib.ui_menu_plots import display_plots_menu

from sys import exit


"""
This program heavily resuses code from the first project "Bacteria Data Analysis".
https://github.com/sarphiv/dtu-intro-prog-bacteria-analysis

Title: DTU - 02631 - Intro. to Prog. and Data Proc. - Bacteria Data Analysis
Author: sarphiv (me)
Submission date: 2020-11-12


This project's structure is a direct copy of the previous project's structure.
Some files such as "lib/ui_base.py", "lib/utilities.py", and "lib/ui_utilities" have been directly copied,
while other files like "lib/ui_menu_*" are very slightly modified adaptions for this project.
The comments in "main.py" are also mostly a carbon copy of the previous project.

The following files mostly (but not fully) contain new content:
    "lib/"
        "aggregate.py"
        "data_fill_processors.py"
        "data.py"
        "plot.py"
        "state.py"
        "statistics.py"


This project and the first project both have a lot of overlap,
so the first project was written with code reuse in mind.
"""



"""
NOTE: Errors, warnings, and notes are output to stderr as usual so make sure you can read stderr.
NOTE: Function docstrings attempt adherence to PEP-257 (although, not the best attempt).
      Function signature is therefore not reiterated as it is deemed un-pythonic and a bad habit.
"""


"""
The program consists of a UI layer based off of CLI menus.
Choosing an option in a menu, executes the option's associated code.
This code may show another menu, change program state, or process and output the data.

The vast majority of the program code is found in the "lib" folder.
    The "load_measurements" function is in "lib/data.py"
    The "print_statistics" function is in "lib/statistics.py"
    The "aggregate_measurements" function is near the bottom in "lib/aggregate.py"


This file is the entrypoint of the program.
Here the main menu and the associated options' functionalities are defined.
Once the program state and main menu has been defined, the main menu is shown.

Choosing an option then calls various functions in the "lib" folder.
The files prefixed with "ui_" do not deal with business logic.
They merely handle the coupling of the UI code with the business logic.

The project is structured this way as it decouples the UI from the business logic.
This allows the base UI code to be fully reused for future projects.
It also allows the UI to easily be defined and changed as shown in this file.

The code makes heavy use of functions as first class citizens.
Being comfortable with functional programming is therefore recommended.

The business logic is mostly decoupled from each other.
This makes the program less fragile to modifications as a change one place,
is less likely to mess up something somewhere else.
It is advised to explore the program by following the call stack of executing one feature.
An IDE that can automatically show docstrings as a pop up on hover is strongly recommended,
as the documentation has been written with this in mind.


No author for the different files have been specified as there is only one.
"""



"""
The program state consists of:
    Raw data loaded in
    Aggregated data of the raw data
    Aggregation mode (period)
    Status messages
"""
#Initialize state of program
state = State()


"""
The following section defines the main menu of the program.
Menus are defined as lists of tuples,
where the first element in the tuple is the menu option text,
while the second element in the tuple is the function to call if the option is selected.

The state of the program is passed into each menu option function, 
except the "Quit" option as it does not need the program state.
"""

#Define main menu of the program. This is where the program starts.
main_menu = [
    #Parameter is program state
    ("Load data",                         lambda: display_load_data_menu(state)),
    ("Aggregate data",                    lambda: display_aggregate_menu(state)),
    ("Display statistics",                lambda: display_statistics(state)),
    ("Visualize electricity consumption", lambda: display_plots_menu(state)),
    #Option to close the program
    ("Quit",                              exit),
]


#At this point, the program state and main menu has been initialized

#Show the main menu
display_main_menu(state, main_menu)
