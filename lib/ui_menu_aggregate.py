from lib.ui_base import prompt_continue, prompt_options
from lib.ui_utilities import inform_if_data_unavailable
from lib.aggregate import aggregate_data, period_to_status



def display_aggregate_menu(state):
    """
    Show menu to change aggregation mode.
    Does not continue if there is no data available.
    """
    #If no data is unavailable, inform user and return
    if inform_if_data_unavailable(state.aggregated_zones):
        return

    #Higher-order function that creates a function,
    # that sets the aggregation mode based on the period
    #NOTE: Capturing period as parameter to break closure when used in list comprehension
    aggregation_setter = lambda period: lambda: state.set_aggregation_mode(period)
    
    aggregate_modes_menu = [
        (status, aggregation_setter(period))
        for period, status in period_to_status.items()
    ]

    prompt_options(aggregate_modes_menu, state.status)

    #Update aggregated data
    aggregate_data(state)
    

