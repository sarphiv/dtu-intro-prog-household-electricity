from lib.ui_utilities import check_data_unavailable
from lib.statistics import get_temperature, get_growth_rate, get_species
from lib.data import bacteria_species

import numpy as np


class Filters:
    """
    Manages filters used to process data.
    
    The filters managed by this class are 2-tuples,
    consisting of a function that filters the data,
    and a string describing what the function does:
    
    (filter_function, filter_description)
    
    There are two filter groups. 
        More filters in the scalar group creates a more restrictive filter.
        More filters in the species group creates a laxer filter,
        allowing for selection of multiple species.


    No filters in the scalar group is interpreted as allowing all values.
    No filters in the species group is interpreted as selecting for all species.
    """
    
    def __init__(self):
        """
        Initialized to not contain any filters.
        """

        self.scalars = []
        self.species = []


    def as_array(self):
        """
        Flatten all filter groups into a list and return them
        """
        return [*self.scalars, *self.species]

    def as_descriptions(self):
        """
        Gets the descriptions for each filter and returns them as a list
        """
        return [description for _, description in self.as_array()]


    def apply(self, data):
        """
        Filters the data based on the currently active filters
        """
        #Return no data, if the provided data is unavailable
        if check_data_unavailable(data):
            return []


        #Initialize scalar group to select for all entries via a boolean array
        scalar_indexes = np.ones(len(data), dtype=bool)
        #Run each filter on the data and restrict the scalar group selection
        # to always be smaller or equal to what it was before
        for filter, _ in self.scalars:
            scalar_indexes &= filter(data)


        #If there are filters for the species, start selecting for species
        if len(self.species) > 0:
            #Initialize species group to select for no species via a boolean array
            species_indexes = np.zeros(len(data), dtype=bool)
            
            #Run each filter on the data and add the selection
            # to the species group selection so that it either
            # always expands or stays the same size.
            for filter, _ in self.species:
                species_indexes |= filter(data)

        #Else, select all species
        else:
            species_indexes = np.ones(len(data), dtype=bool)


        #Return the intersection of 
        # the scalar group's selection,
        # and the species group's selection
        return data[scalar_indexes & species_indexes]


    def remove(self, index):
        """
        Removes an active filter via the filter's "flattened index".
        """

        #Get amount of scalar group filters
        len_scalar_group = len(self.scalars)
        
        #WARN: Not checking for out of bound indexes
        
        #If filter is in the scalar group, use the index directly to remove it
        if (index < len_scalar_group):
            del self.scalars[index]
        #Else the filter is in the species group, shift the index then remove it
        else:
            del self.species[index - len_scalar_group]


    @staticmethod
    def filter_scalar(scalar_data, min, max):
        """
        Returns an array of true and false values for the entries,
        that are within the provided range [min; max[
        """
        return (min <= scalar_data) & (scalar_data < max)
    
    def add_filter_scalar(self, scalar_getter, scalar_name, min, max):
        """
        Adds an exclusive filter that only allows values within the provided range.
        The restricted values are selected via a "scalar_getter" function,
        while the "scalar_name" is a string for the name of the scalar e.g. "temperatures".
        """
        self.scalars.append((
            lambda data: Filters.filter_scalar(scalar_getter(data), min, max),
            f"Filtering for {scalar_name} in the range [{min}, {max}["))


    def add_filter_temperature(self, min, max):
        """
        Adds an exclusive filter that only allows temperatures within the provided range.
        """
        self.add_filter_scalar(get_temperature, "temperatures", min, max)

    def add_filter_growth_rate(self, min, max):
        """
        Adds an exclusive filter that only allows growth rates within the provided range.
        """
        self.add_filter_scalar(get_growth_rate, "growth rates", min, max)



    @staticmethod
    def filter_species(data, species):
        """
        Returns an array of true and false values for the entries,
        that are the given species.
        """
        return get_species(data) == species
    
    def add_filter_species(self, species):
        """
        Adds an inclusive filter that selects for a specific species.
        """
        self.species.append((
            lambda data: Filters.filter_species(data, species),
            f"Filtering for the species {bacteria_species[species]}"))
