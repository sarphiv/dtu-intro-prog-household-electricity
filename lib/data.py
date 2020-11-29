from lib.utilities import eprint

import numpy as np
import pandas as pd
from os.path import exists, isfile


time_data_length = 6
zone_data_length = 4




def file_exists(file_path):
    """
    Returns whether a file path leads to a file
    """
    return exists(file_path) and isfile(file_path)





def get_zones(row):
    return row[-zone_data_length:]



def get_corrupted_indexes(row):
    return np.argwhere(get_zones(row) == -1).reshape(-1) + time_data_length


def is_corrupted(row):
    return len(get_corrupted_indexes(row)) != 0

def filler(row, replacement):
    corrupted = get_corrupted_indexes(row)

    filled_row = row.copy()

    if replacement is None and is_corrupted(row):
        return None

    for i in corrupted:
        filled_row[i] = replacement[i]


    return filled_row


def get_valid_rows(rows):
    for i, row in enumerate(rows):
        if not is_corrupted(row):
            yield (i, row)
        

def backfill_replacement(valid_rows):
    i = 0
    
    for valid_i, row in valid_rows:
        while i <= valid_i:
            i += 1
            yield row


def forfill_replacement(valid_rows):
    i = 0
    valid_rows_iter = iter(valid_rows)
    
    _, current_valid_row = next(valid_rows)
    
    for next_valid_i, next_valid_row in valid_rows_iter:
        while i < next_valid_i:
            i += 1
            yield current_valid_row
            
        current_valid_row = next_valid_row


    while True:
        yield current_valid_row

def drop_replacement(valid_rows):
    while True:
        yield None


fmodes = {
    "forward fill": forfill_replacement,
    "backward fill": backfill_replacement,
    "drop": drop_replacement
}

def load_measurements(filename, fmode):
    rows = pd.read_csv(filename, header = None).to_numpy()
    
    
    valid_rows = get_valid_rows(rows)


    replacement_gen = fmodes[fmode](valid_rows)

    if fmode == "forward fill" and is_corrupted(rows[0]):
        replacement_gen = drop_replacement(valid_rows)
        eprint("Could not forward fill corrupted rows as first row is corrupted. " +
               "Falling back to dropping corrupted rows")
    elif fmode == "backward fill" and is_corrupted(rows[-1]):
        replacement_gen = drop_replacement(valid_rows)
        eprint("Could not backward fill corrupted rows as last row is corrupted. " +
               "Falling back to dropping corrupted rows")
        
    replacement = iter(replacement_gen)
    
    
    filled_rows = []
    
    for row in rows:
        filled_row = filler(row, next(replacement))
        
        if filled_row is not None:
            filled_rows.append(filled_row)

    

    filled_rows = np.array(filled_rows)
    tvec = filled_rows[:, :time_data_length]
    data = filled_rows[:, -zone_data_length:]
    
    return (tvec, data)


    
    

def dataLoad(filename):
    """
    Loads data from a file and returns a numpy array with shape (-1,3): [[temperature, growth_rate, species], ...]
    Skips invalid entries and outputs them to stderr.
    
    REMARK: Does not check for existence of file. Check before calling this function.
    """

    #Load and immediately close file
    with open(filename, mode='r') as file:
        lines = file.readlines()

    #Parse all data
    data = []
    for i, entry in enumerate(lines):
        #Attempt to parse entry 
        (parsed, error) = parse_entry(entry)
        
        #If parsing of line succeeded, store it
        if error == None:
            data.append(parsed)
        #Else, output failure
        else:
            eprint(f'Failed parsing line {i} with error "{error}" and with data "{entry.rstrip()}"')
            continue


    #Return valid entries
    return np.array(data)

