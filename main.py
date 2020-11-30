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


data statistics same form


add function docstrings

ADD SOURCE REFERENCE FOR PREVIOUS PROJECT



oh ffs, we need to have zeros for hours with no data


"""

#%%
from sys import exit
from lib.data import load_measurements
from lib.aggregate import aggregate_measurements
from lib.statistics import print_statistics


#%%

(tvec, data) = load_measurements("2008.csv", "backward fill")


#aggregate_measurements(tvec, data, "minute")

print_statistics(tvec, data)
#%%
