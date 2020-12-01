"""
function, select out specific time columns or range of them
unique time columns

loop through all of them,
    select rows from original dataset that have the same time columns,
    sum the zone columns 


for specific things like hours, days, months
    choose all times before the one we select for
    so e.g. hours, we unique on months and days

for the hourly
    we choose to unique by hour




plotting
    input data, zone based wanted
    
    
        if zones, 
            prep data
            subplots, 
            send each (name, data) into plot drawer for each subplot
        else sum, send one fig into plot drawer
            prep data
            send into plot drawer
    
    
    func draw plot based on fig, name, data
        label things
        bar plot if under 25
        
        only responsible for drawing one plot


copy pasta ui code



add function docstrings

ADD SOURCE REFERENCE FOR PREVIOUS PROJECT


split up some files

prevent them from showing plot if data unavailable


add text to say plot is loading..., and to close plot to return or whatever



"""

from lib.ui_menu_plots import display_plots_menu
from lib.plot import show_plot
from lib.ui_menu_aggregate import display_aggregate_menu
from lib.ui_menu_main import display_main_menu
from sys import exit
from lib.state import State
from lib.data import load_measurements
from lib.aggregate import aggregate_measurements
from lib.ui_menu_statistics import display_statistics
from lib.ui_menu_data import display_load_data_menu
from lib.statistics import print_statistics


"""
The program state consists of:
    Raw data loaded in.
    Aggregated data of the raw data
    Status messages
"""
#Initialize state of program
state = State()


#Define main menu of the program. This is where the program starts.
main_menu = [
    #Parameters consist of program state and definition of the menu to show.
    # Some options do not have a second parameter,
    # because they do not lead to menus.
    ("Load data",                         lambda: display_load_data_menu(state)),
    ("Aggregate data",                    lambda: display_aggregate_menu(state)),
    ("Display statistics",                lambda: display_statistics(state)),
    ("Visualize electricity consumption", lambda: display_plots_menu(state)),
    #Option to close the program
    ("Quit",                              exit),
]


display_main_menu(state, main_menu)

