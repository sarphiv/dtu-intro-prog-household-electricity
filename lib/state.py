from lib.aggregate import period_to_status

class State:
    """
    A DTO encapsulating the program state.
    
    Initialized to contain no data and no filters.
    """

    def __init__(self):
        self.raw_data = None
        self.aggregated_data = None

        self.aggregation_mode = "minute"
        self.aggregation_status = None
        self.set_aggregation_mode(self.aggregation_mode)
        
        self.measurement_unit_status = "Measurements in watt-hour"


    def set_raw_data(self, raw_data):
        self.raw_data = raw_data

    @property
    def aggregated_times(self):
        if self.aggregated_data is None:
            return None
        else:
            return self.aggregated_data[0]
    
    @property
    def aggregated_zones(self):
        if self.aggregated_data is None:
            return None
        else:
            return self.aggregated_data[1]
    
    @property
    def status(self):
        return [self.aggregation_status, self.measurement_unit_status]

    def set_aggregation_mode(self, period):
        self.aggregation_mode = period
        self.aggregation_status = period_to_status[period]