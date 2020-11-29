from lib.ui_base import prompt_continue, prompt_options, prompt_range
from lib.data import bacteria_species


def display_filters_menu(state, menu):
    """
    Enters the filters management menu
    """
    prompt_options(menu, state.filters.as_descriptions())


def display_filters_add_menu(state, menu):
    """
    Enters the menu allowing selection of which filter type to add.
    """
    prompt_options(menu, state.filters.as_descriptions())


def display_filters_add_scalar_menu(state, filters_menu, scalar_getter, scalar_name):
    """
    Enters the prompt that allows specifying the parameters for a scalar filter.
    """
    
    #Get minimum and maximum range for scalar filter
    (min, max) = prompt_range()
    
    #Add scalar filter to list of active filters
    # using the provided scalar retriever, 
    # and scalar name for use in the filter description.
    state.filters.add_filter_scalar(scalar_getter, scalar_name, min, max)

    #Update program state filtered data with the new filter
    state.filtered_data = state.filters.apply(state.raw_data)
    
    #Go back to the filters management menu
    display_filters_menu(state, filters_menu)


def display_filters_add_species_menu(state, filters_menu):
    """
    Enters the menu that allows specifying species for a species filter.
    """
    
    #Higher-order function that creates a function,
    # that adds a new filter based on the given species index.
    #NOTE: Capturing species ID as parameter to break closure when used in list comprehension
    add_filter_func = lambda id: lambda: state.filters.add_filter_species(id)
    
    #Create prompt options with
    # species name as text,
    # and the function to add the respective filter as the "action".
    options = [(s, add_filter_func(id)) for id, s in bacteria_species.items()]
    
    
    #Prompt user with the created options, and execute the chosen option
    prompt_options(options, 
                   state.filters.as_descriptions(), 
                   msg="Choose species to include")


    #Update program state filtered data with the new filter
    state.filtered_data = state.filters.apply(state.raw_data)
    
    #Go back to the filters management menu
    display_filters_menu(state, filters_menu)


def display_filters_remove_menu(state, filters_menu):
    """
    Enters the menu that allows specifying which active filter to remove.
    """
    #Higher-order function that creates a function,
    # that removes a filter based on the given "flattened" filter index.
    #NOTE: Capturing filter index as parameter to break closure when used in list comprehension
    remove_filter_func = lambda i: lambda: state.filters.remove(i)
    
    #Get descriptions of each active filter
    descriptions = state.filters.as_descriptions()


    #If there are no filters, inform the user, and return to filters management menu
    if len(descriptions) == 0:
        #Inform user no filters are active, prompt to continue
        prompt_continue("No filters to remove - press enter to continue...")
        
        #Go back to filters management menu
        display_filters_menu(state, filters_menu)
        return


    #Create prompt options with
    # filter description as text,
    # and the function to remove the respective filter as the "action".
    options = [(desc, remove_filter_func(i)) for i, desc in enumerate(descriptions)]

    #Prompt user with the created options, and execute the chosen option
    prompt_options(options, msg="Choose filter to remove")


    #Update program state filtered data with the new filter
    state.filtered_data = state.filters.apply(state.raw_data)

    #Go back to the filters management menu
    display_filters_menu(state, filters_menu)