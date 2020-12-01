from lib.ui_base import prompt_continue

import numpy as np

#Table header and row name definitions
table_column_width = 14
table_header = ["Zones", "Minimum", "1. quart.", "2. quart.", "3. quart.", "Maximum"]
table_row_name = ["1", "2", "3", "4", "All"]


def print_row(elements):
    """
    Print elements evenly spaced and centered in statistics table
    """
    #Create format string
    row_spacing = f"{{:^{table_column_width}}}" * len(elements)

    #Insert elements and print string
    print(row_spacing.format(*elements))


def print_line():
    """
    Print horizontal line that spans full width of table
    """
    print("-" * table_column_width * len(table_header))
    


def get_quartiles(zones):
    """
    Computes the minimum, 1., median, 3., maximum quartiles
    """
    return np.quantile(zones, [0.00, 0.25, 0.50, 0.75, 1.00], axis=0)



def print_statistics(tvec, data):
    """
    Compute and print quartile statistics about the provided data.
    """
    #Get quartiles for each zone and store in the form [[zone1_quartiles...], ...]
    quartiles = get_quartiles(data).T
    #Get quartiles for total usage
    summed_quartiles = get_quartiles(data.sum(axis=1))
    #Append "summed_quartiles" to "quartiles"
    quartiles = np.append(quartiles, np.expand_dims(summed_quartiles, 0), axis=0)

    #Round all quartiles
    quartiles = np.round(quartiles, 2)


    #Print table header
    print_row(table_header)
    #Print horizontal line
    print_line()
    
    #Print each row and its associated name
    for name, quartile in zip(table_row_name, quartiles):
        print_row([name, *quartile])

    #Print horizontal line
    print_line()
