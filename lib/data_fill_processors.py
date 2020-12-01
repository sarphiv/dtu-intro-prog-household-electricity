import numpy as np


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

