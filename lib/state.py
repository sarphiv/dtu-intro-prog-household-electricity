from lib.aggregate import period_to_status

class State:
    """
    A DTO encapsulating the program state.
    
    Initialized to contain no data, aggregation mode "minute", and to measure usage in watt-hour.
    """

    def __init__(self):
        self.raw_data = None
        self.aggregated_data = None

        self.aggregation_mode = "minute"
        self.aggregation_status = None
        self.set_aggregation_mode(self.aggregation_mode)
        
        self.measurement_unit_status = "Usage in watt-hour"


    def set_raw_data(self, raw_data):
        """
        Method to set raw data as an alternative to direct assignment
        """
        self.raw_data = raw_data
        
    def set_aggregation_mode(self, period):
        """
        Method to update aggregation mode and its associated status
        """
        self.aggregation_mode = period
        self.aggregation_status = period_to_status[period]

    @property
    def aggregated_times(self):
        """
        Property to access aggregated times directly
        """
        if self.aggregated_data is None:
            return None
        else:
            return self.aggregated_data[0]
    
    @property
    def aggregated_zones(self):
        """
        Property to access aggregated zones directly
        """
        if self.aggregated_data is None:
            return None
        else:
            return self.aggregated_data[1]
    
    @property
    def status(self):
        """
        Property to access statuses in list form
        """
        return [self.aggregation_status, self.measurement_unit_status]
