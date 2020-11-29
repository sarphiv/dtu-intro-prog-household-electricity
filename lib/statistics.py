from lib.data import bacteria_species


#Isolate temperature from each row
get_temperature = lambda data: data[:, 0]
#Isolate growth rate from each row
get_growth_rate = lambda data: data[:, 1]
#Isolate species from each row
get_species     = lambda data: data[:, 2]
#Isolate temperature and growth rate from each row
get_temperature_growth_rate = lambda data: data[:, 0:2]


"""
A dictionary mapping strings of statistical calculation names
to functions that do that exact calculation.
"""
#Dictionary mapping from statistic operation name to function.
# It is assumed the input data is given as a numpy array.
statistic_functions = {
    #Get mean of temperature
    "mean temperature": lambda data: 
        get_temperature(data).mean(),

    #Get mean of growth rate
    "mean growth rate": lambda data: 
        get_growth_rate(data).mean(),

    #Get standard deviation of temperature
    "std temperature": lambda data: 
        get_temperature(data).std(),

    #Get standard deviation of growth rate
    "std growth rate": lambda data: 
        get_growth_rate(data).std(),

    #Get length of first dimension (rows) of data
    "rows": lambda data: 
        data.shape[0],

    #Get mean growth rate of rows with temperature below 20,
    # by filtering out entries with temperatures above 20,
    # and then calling the data statistics function
    # on the filtered data
    "mean cold growth rate": lambda data: 
        dataStatistics(
            data[get_temperature(data) < 20],
            "mean growth rate"
        ),

    #Get mean growth rate of rows with temperature above 50,
    # by filtering out entries with temperatures below 50,
    # and then calling the data statistics function
    # on the filtered data
    "mean hot growth rate": lambda data: 
        dataStatistics(
            data[get_temperature(data) > 50],
            "mean growth rate"
        ),

    #Data keyed by species.
    # Groups rows/entries into a dictionary keyed by species
    "data by species": lambda data: { 
            species: data[get_species(data) == species]
            for species in bacteria_species.keys()
        },

    #Amount of rows/entries keyed by species {species: number, ...}
    "rows by species": lambda data: { 
            species: dataStatistics(entries, "rows")
            for species, entries in dataStatistics(data, "data by species").items()
        },

    #Temperature keyed by species {species: [[temperature], ...], ...}
    "temperature by species": lambda data: { 
            species: get_temperature(entries)
            for species, entries in dataStatistics(data, "data by species").items()
        },

    #Growth rate keyed by species {species: [[growth_rate], ...], ...}
    "growth rate by species": lambda data: { 
            species: get_growth_rate(entries)
            for species, entries in dataStatistics(data, "data by species").items()
        },
    
    #Temperature and growth rate keyed by species {species: [[temperature, growth_rate], ...], ...}
    "temperature and growth rate by species": lambda data: { 
            species: get_temperature_growth_rate(entries)
            for species, entries in dataStatistics(data, "data by species").items()
        },
}


#Dictionary mapping statistic operation name to a description of the operation.
statistic_descriptions = {
    "mean temperature": "Mean temperature of all species",
    "mean growth rate": "Mean growth rate of all species",
    "std temperature": "Standard deviation of temperature of all species",
    "std growth rate": "Standard deviation of growth rate of all species",
    "rows": "Amount of rows in the data",
    "mean cold growth rate": "Mean growth rate of all species with a temperature below 20",
    "mean hot growth rate": "Mean growth rate of all species with a temperature above 50"
}


def dataStatistics(data, statistic):
    """
    Calculate statistics on the provided data and returns the result.
    The statistic should be given as a string being one of (case sensitive):
        "mean temperature",
        "mean growth rate",
        "std temperature",
        "std growth rate",
        "rows",
        "mean cold growth rate",
        "mean hot growth rate",
        "data by species",
        "rows by species",
        "temperature by species",
        "growth rate by species",
        "temperature and growth rate by species"
    """
    #Get requested statistic function, and then apply the function on data entries
    return statistic_functions[statistic](data)