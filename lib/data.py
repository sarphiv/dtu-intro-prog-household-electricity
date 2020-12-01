from lib.utilities import eprint

import numpy as np
import pandas as pd
from os.path import exists, isfile



def file_exists(file_path):
    """
    Returns whether a file path leads to a file
    """
    return exists(file_path) and isfile(file_path)


#Column length of data segments
time_data_length = 6
zone_data_length = 4

def get_times(rows):
    """
    Retrieves times from raw data and returns it as an integer numpy array
    """
    return rows.iloc[:, :time_data_length].to_numpy()

def get_zones(rows):
    """
    Retrieves zones from raw data and returns it as a float numpy array
    """
    return rows.iloc[:, -zone_data_length:].to_numpy()



def get_corrupted_indexes(zone):
    """
    Get an array of indexes for corrupted zone measurements
    """
    return np.argwhere(zone == -1).reshape(-1)

def is_corrupted_indexes(indexes):
    """
    Helper function to check if any corrupted indexes exists.
    It just checks if the array is not empty.
    """
    return len(indexes) != 0

def is_corrupted(zone):
    """
    Checks if a zone has any corrupted measurements
    """
    return is_corrupted_indexes(get_corrupted_indexes(zone))



def get_valid_zones(zones):
    """
    Generator that yields all zones without any corrupted measurements.
    """
    #Give each zone an index and yield it, if the zone is not corrupted
    for i, zone in enumerate(zones):
        if not is_corrupted(zone):
            yield (i, zone)



def normalize_row(time, zone, replacement):
    """
    Replaces corrupted zone measurements with replacement zone measurements.
    If replacement zone measurements is "None", returns "None" if there is corruption.
    """
    #Create a copy of zone measurements to mutate
    normalized_zone = zone.copy()
    
    #Get indexes of corrupted zones
    corrupt_indexes = get_corrupted_indexes(zone)

    #If replacement zone measurement is None and there is corruption, 
    # return "None".
    if replacement is None and is_corrupted_indexes(corrupt_indexes):
        return None

    #Replace all corrupted zone measurements with associated replacement zone
    for i in corrupt_indexes:
        normalized_zone[i] = replacement[i]


    #Return normalized row
    return (time, normalized_zone)



def backfill_replacement(valid_zones):
    """
    Generator that yields the next valid zone measurement relative to current zone measurement.
    """
    i = 0

    #Get and yield next valid zone
    for valid_i, row in valid_zones:
        #While current zone is before CURRENT VALID zone,
        # keep yielding the CURRENT VALID zone
        while i <= valid_i:
            yield row
            i += 1


def forwfill_replacement(valid_zones):
    """
    Generator that yields the most recently seen valid zone measurement relative to current zone measurement.
    """
    i = 0

    #Get first valid zone
    valid_rows_iter = iter(valid_zones)
    _, current_valid_zone = next(valid_zones)
    
    #Get and yield next valid zone
    for next_valid_i, next_valid_zone in valid_rows_iter:
        #While current zone is before NEXT VALID zone,
        # keep yielding the CURRENT VALID zone
        while i < next_valid_i:
            yield current_valid_zone
            i += 1
        
        #Current zone is same as NEXT VALID zone,
        # set NEXT VALID zone as the new CURRENT VALID zone
        current_valid_zone = next_valid_zone


    #No more NEXT VALID zones to choose from,
    # continue yielding the last known VALID ZONE
    while True:
        yield current_valid_zone


def drop_replacement(valid_zones):
    """
    Generator that infinitely yields "None" to signify rows should be dropped in case of corruption.
    """
    #Always yield a "None" as replacement to drop rows
    while True:
        yield None



#Map "fmode" to its associated replacement generator
fmodes = {
    "forward fill": forwfill_replacement,
    "backward fill": backfill_replacement,
    "drop": drop_replacement
}


def enforce_fmode(fmode, raw_zones):
    """
    Enforce a valid "fmode" by defaulting to "drop" if conditions do not allow for the requested "fmode".
    """
    #If "fmode" is "forward fill", check if first row is corrupted
    fmode_forwfill_impossible = fmode == "forward fill" and is_corrupted(raw_zones[0])
    #If "fmode" is "backward fill", check if last row is corrupted
    fmode_backfill_impossible = fmode == "backward fill" and is_corrupted(raw_zones[-1])

    #If requested mode is impossible, print warning and default to "fmode = drop"
    if fmode_forwfill_impossible or fmode_backfill_impossible:
        eprint(f"Could not {fmode} corrupted rows as " +
               f"{'first' if fmode_forwfill_impossible else 'last'} row is corrupted. " +
               "Falling back to dropping corrupted rows")
        return "drop"
    #Else if fmode is unknown, print warning and default to "fmode = drop"
    elif fmode not in fmodes:
        eprint(f"Invalid fill mode: {fmode}" +
               "Falling back to dropping corrupted rows")
        return "drop"
    #Else, allow requested "fmode"
    #WARN: Assuming there are only three "fmode = { "forward fill", "backward fill", "drop" }".
    else:
        return fmode



def load_measurements(filename, fmode):
    """
    Loads data from a comma seperated file and returns a tuple of two numpy arrays of dimension (N, 6) and (N, 4) respectively: 
        ([[year, month, day, hour, minute, second], 
          ...], 
         [[zone1, zone2, zone3, zone4],
          ...])
    
    "fmode" can be one of:
        "forward fill": Individual corrupted zone measurements are replaced with latest valid individual measurement.
            First row must be a valid measurement, else "fmode" defaults to "drop.
        "backward fill": Individual corrupted zone measurements are replaced with next valid individual measurement.
            Last row must be a valid measurement, else "fmode" defaults to "drop.
        "drop": Individual corrupted zone measurements will cause the whole measurement row to be deleted.
    
    
    REMARK: Does not check for existence of file. Check before calling this function.
    REMARK: Specification does not say file structure can be corrupted. It is assumed file has correct structure.
    """
    
    #Read data from file
    pd_rows = pd.read_csv(filename, header = None)
    
    #If there are no rows, return empty measurements
    if len(pd_rows) == 0:
        return (np.empty((0, time_data_length)),
                np.empty((0, zone_data_length)))



    #Split data into times and zones
    (raw_times, raw_zones) = (get_times(pd_rows), 
                              get_zones(pd_rows))

    #Get all zones without corrupted data
    valid_zones = get_valid_zones(raw_zones)

    #Select valid fmode based on zone data
    selected_fmode = enforce_fmode(fmode, raw_zones)

    #Create zone replacement generator for zones with invalid data
    replacement_gen = fmodes[selected_fmode](valid_zones)
    replacement = iter(replacement_gen)


    #Prepare lists to store normalized measurements in
    #NOTE: Not using numpy arrays as we would continously need to reallocate memory,
    # since we do not know the final size when using "fmode=drop".
    tvec = []
    data = []
    
    #Iterate through all rows
    for time, zone in zip(raw_times, raw_zones):
        #Normalize row and deal with corruption according to the selected "fmode".
        # The "replacement" for a corrupted row is determined by the "fmode".
        normalized_row = normalize_row(time, zone, next(replacement))
        
        #If normalized row is not to be dropped, save it
        if normalized_row is not None:
            #Deconstruct row
            (t, d) = normalized_row
            
            #Save into respective lists
            tvec.append(t)
            data.append(d)


    #NOTE: Reassigning, because specification specifies this
    (tvec, data) = (np.array(tvec), np.array(data))
    
    #Return numpy arrays of times as integers and zones as floats
    return (tvec, data)

