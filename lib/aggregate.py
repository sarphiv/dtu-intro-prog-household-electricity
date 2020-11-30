"""
function, select out specific time columns or range of them
unique time columns

loop through all of them,
    select rows from original dataset that have the same time columns,
    we can append those to each other, then sum along a zone axis
    sum the zone columns 


for specific things like hours, days, months
    choose all times before the one we select for
    so e.g. hours, we unique on months and days

for the hourly
    we choose to unique by hour
"""

from lib.data import time_data_length, zone_data_length
import numpy as np
from collections import defaultdict



def select_time_unit(time, columns):
    return tuple(time[c] for c in columns)

def time_unit_selector(columns):
    return lambda time: select_time_unit(time, columns)


def reverse_time_unit(time_unit, columns):
    """
    REMARK: Assumes "time_unit" is not empty
    """
    time = np.zeros(time_data_length, dtype=np.dtype(time_unit[0]))

    for unit, c in zip(time_unit, columns):
        time[c] = unit

    return time

def time_unit_reverser(columns):
    return lambda time_unit: reverse_time_unit(time_unit, columns)



period_to_columns = {
    "hour": [0, 1, 2, 3],
    "day": [0, 1, 2],
    "month": [0, 1],
    "hour of the day": [3]
}

period_to_time_unit_selector = {
    period: time_unit_selector(columns)
    for period, columns in period_to_columns.items()
}

period_to_time_unit_reverser = {
    period: time_unit_reverser(columns)
    for period, columns in period_to_columns.items()
}

period_to_zone_aggregator = {
    period: (lambda zones: zones.mean(axis=0))
            if (period == "hour of the day") else 
            (lambda zones: zones.sum(axis=0))
    for period in period_to_columns.keys()
}

    



def group_by_time_units(times, zones, time_selector):
    grouped_zones = defaultdict(lambda: [])

    for time, zone in zip(times, zones):
        group = grouped_zones[time_selector(time)]
        
        group.append(zone)

    return { g: np.array(z) for g, z in grouped_zones.items() }


def add_zero_hour_measurements(grouped_zones, tu_selector):
    for i in range(24):
        hour_unit = tu_selector(np.array([0, 0, 0, i, 0, 0]))
        zero_zone = np.zeros((1, zone_data_length))

        if hour_unit not in grouped_zones:
            grouped_zones[hour_unit] = zero_zone


#sum output of generator and append
#return aggregated

def aggregate_measurements(tvec, data, period):
    """
    REMARK: Assumes "period" input is one of:
        "hour"
        "day"
        "month"
        "hour of the day"
    """
    
    #If empty, do nothing
    if (len(tvec) == 0):
        return (tvec, data)

    tu_selector = period_to_time_unit_selector[period]
    tu_reverser = period_to_time_unit_reverser[period]

    zone_aggregator = period_to_zone_aggregator[period]


    grouped_zones = group_by_time_units(tvec, data, tu_selector)
    
    if (period == "hour of the day"):
        add_zero_hour_measurements(grouped_zones, tu_selector)


    tvec_a = []
    data_a = []


    for group, zones in grouped_zones.items():
        time_aggregated = tu_reverser(group)
        zones_aggregated = zone_aggregator(zones)
        
        tvec_a.append(time_aggregated)
        data_a.append(zones_aggregated)


    #NOTE: Reassigning, because specification specifies this
    (tvec_a, data_a) = (np.array(tvec_a), np.array(data_a))
    

    return (tvec_a, data_a)