from lib.ui_base import prompt_continue

import numpy as np


table_column_width = 14
table_header = ["Zones", "Minimum", "1. quart.", "2. quart.", "3. quart.", "Maximum"]
table_row_name = ["1", "2", "3", "4", "All"]


def print_row(elements):
    row_spacing = f"{{:^{table_column_width}}}" * len(elements)
    
    print(row_spacing.format(*elements))
    
def print_line():
    print("-" * table_column_width * len(table_header))
    


def get_quartiles(zones):
    return np.quantile(zones, [0.00, 0.25, 0.50, 0.75, 1.00], axis=0)



def print_statistics(tvec, data):
    quartiles = get_quartiles(data).T
    summed_quartiles = get_quartiles(data.sum(axis=1))
    quartiles = np.append(quartiles, np.expand_dims(summed_quartiles, 0), axis=0)
    quartiles = np.round(quartiles, 2)

    print_row(table_header)
    
    print_line()
    
    for name, quartile in zip(table_row_name, quartiles):
        print_row([name, *quartile])

    print_line()
