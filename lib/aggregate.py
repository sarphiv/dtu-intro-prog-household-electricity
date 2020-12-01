from lib.data import time_data_length, zone_data_length
import numpy as np
from collections import defaultdict



def select_time_unit(time, columns):
    """
    Migrates specific columns of a time vector to a time unit tuple.
    REMARK: Throws away information in columns not selected for.
    """
    return tuple(time[c] for c in columns)

def time_unit_selector(columns):
    """
    Creates an instance of a "select_time_unit" with "columns" predefined.
    """
    return lambda time: select_time_unit(time, columns)


def reverse_time_unit(time_unit, columns):
    """
    Turns a time unit tuple into a time vector using the available information.
    Inverse operation of "select_time_unit".
    
    REMARK: Assumes "time_unit" is not empty
    """
    #Create empty time vector
    time = np.zeros(time_data_length, dtype=np.dtype(time_unit[0]))
    
    #If reversing a date (more than one column)
    # initialize days and months to 1
    date_and_zero_month = len(columns) > 1
    if date_and_zero_month:
        time[1] = 1
        time[2] = 1

    #Migrate each available time from the tuple to the time vector
    for unit, c in zip(time_unit, columns):
        time[c] = unit


    #Return time vector representation of time unit
    return time

def time_unit_reverser(columns):
    """
    Creates an instance of a "reverse_time_unit" with "columns" predefined.
    """
    return lambda time_unit: reverse_time_unit(time_unit, columns)



#Map from period (aggregation mode) to status message (description)
period_to_status = {
    "none": "Usage directly from measurements",
    "minute": "Usage per minute",
    "hour": "Usage per hour",
    "day": "Usage per day",
    "month": "Usage per month",
    "hour of the day": "Usage per hour of the day",
}

#Map from period (aggregation mode) to time vector columns to select for uniqueness with
period_to_columns = {
    "none": [0, 1, 2, 3, 4, 5],
    "minute": [0, 1, 2, 3, 4],
    "hour": [0, 1, 2, 3],
    "day": [0, 1, 2],
    "month": [0, 1],
    "hour of the day": [3]
}

#Map from period (aggregation mode) to time unit selector instances with predefined columns
period_to_time_unit_selector = {
    period: time_unit_selector(columns)
    for period, columns in period_to_columns.items()
}

#Map from period (aggregation mode) to time unit reverser instances with predefined columns
period_to_time_unit_reverser = {
    period: time_unit_reverser(columns)
    for period, columns in period_to_columns.items()
}

#Map from period (aggregation mode) to function that defines how zone measurements with the same time unit are aggregated
period_to_zone_aggregator = {
    period: (lambda zones: zones.mean(axis=0))
            if (period == "hour of the day") else 
            (lambda zones: zones.sum(axis=0))
    for period in period_to_columns.keys()
}



def group_by_time_units(times, zones, time_unit_selector):
    """
    Group all measurements with the same time unit together.
    """
    #Dictionary to store time unit to zones map
    grouped_zones = defaultdict(lambda: [])

    #Iterate through all measurements, and group by time unit
    for time, zone in zip(times, zones):
        #Get time unit from current time and get associated group
        group = grouped_zones[time_unit_selector(time)]
        
        #Append zone measurement to group
        group.append(zone)

    #Make each outermost list in each group a numpy array,
    # resulting in everything being numpy arrays.
    #Return converted groups
    return { g: np.array(z) for g, z in grouped_zones.items() }


def add_zero_hour_measurements(grouped_zones, tu_selector):
    """
    Pad hour based time unit groups with "zero zone measurements",
    to get measurements for the full 24 hours of a day.
    
    Useful when aggregation mode is "hour of the day".
    """
    #Loop through all hours of the day, 
    # add "zero zone measurement" if no measurement for associated hour.
    for i in range(24):
        #Artificially construct hour time unit
        hour_unit = tu_selector(np.array([0, 0, 0, i, 0, 0]))
        #Create zone measurements that are all zero
        zero_zone = np.zeros((1, zone_data_length))

        #If the hour time unit has no measurements, pad with "zero zone measurement"
        if hour_unit not in grouped_zones:
            grouped_zones[hour_unit] = zero_zone



def aggregate_measurements(tvec, data, period):
    """
    Aggregates zone measurements based on time periods by summing usage.
    If period is "hour of the day" aggregation is done via a mean of the usage instead of summing.

    REMARK: Assumes "period" parameter is one of:
        "none"
        "minute"
        "hour"
        "day"
        "month"
        "hour of the day"
    """
    
    #If empty, do nothing and return original empty input
    if (len(tvec) == 0):
        return (tvec, data)


    #Retrieve time unit selector and reverser for the given period (aggregation mode)
    tu_selector = period_to_time_unit_selector[period]
    tu_reverser = period_to_time_unit_reverser[period]

    #Retrieve zone measurement aggregator for the given period (aggregation mode)
    zone_aggregator = period_to_zone_aggregator[period]


    #Group zones measurements by period
    grouped_zones = group_by_time_units(tvec, data, tu_selector)

    #If aggregation mode is "hour of the day", pad empty hours with "zero zone measurements"
    if (period == "hour of the day"):
        add_zero_hour_measurements(grouped_zones, tu_selector)


    #Prepare aggregated data lists to store final results in
    tvec_a = []
    data_a = []

    #Iterate through each time period/unit group, aggregate zone measurements, store
    for group, zones in grouped_zones.items():
        #Retrieve time vector from group time unit
        time_aggregated = tu_reverser(group)
        #Aggregate zone measurements within group
        zones_aggregated = zone_aggregator(zones)
        
        #Store time vector and aggregated measurements
        tvec_a.append(time_aggregated)
        data_a.append(zones_aggregated)


    #NOTE: Reassigning, because specification specifies this
    (tvec_a, data_a) = (np.array(tvec_a), np.array(data_a))

    #Return aggregated data
    return (tvec_a, data_a)


def aggregate_sort_data(state):
    """
    Aggregate and sort raw data in program state and store the result in program state.
    Prints out status messages too.
    """

    #Start aggregating data
    print("Aggregating data...")
    state.aggregated_data = aggregate_measurements(*state.raw_data, state.aggregation_mode)

    #Sort data if there is data
    (times, zones) = state.aggregated_data
    if len(times) > 0:
        #Get sorted indexes with seconds as primary sort key
        sorted_indexes = np.lexsort(times.T[::-1])
        
        #Access data in sorted order and save
        state.aggregated_data = (times[sorted_indexes], zones[sorted_indexes])


    #Aggregated data
    print("Aggregated data", end="\n\n")
