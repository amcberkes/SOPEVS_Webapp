import os
import csv
import numpy as np
import random

class ElectricVehicle:
    def __init__(self, battery_capacity, min_soc, max_soc, charging_capacity, charging_connectivity, charging_preference):
        self.battery_capacity = battery_capacity
        self.min_soc = min_soc
        self.max_soc = max_soc
        self.charging_capacity = charging_capacity
        self.charging_connectivity = charging_connectivity
        self.charging_preference = charging_preference

    def compute_SOC_arr(self, dist_km, consumption):
        used_kwh = (dist_km * consumption) / 1000  
        soc_change = used_kwh / self.battery_capacity
        return max(self.max_soc * self.battery_capacity - soc_change, self.min_soc * self.battery_capacity)

class TripSimulator:
    def __init__(self, ev):
        self.ev = ev

    def generate_trip_data(self, num_days, output_file):
        # Your existing logic for generating trip data
        trip_data = []
        for day in range(num_days):
            # Implement trip logic
            pass
        self.write_to_csv(output_file, trip_data)

    def write_to_csv(self, file_name, data):
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Day", "Weekday", "Departure Time", "SOC on Departure", "Arrival Time", "SOC on Arrival"])
            # Existing logic for writing to CSV
            pass

def setup_ev_simulation(battery_capacity, min_soc, max_soc, charging_capacity, charging_connectivity, charging_preference, num_days, output_file):
    ev = ElectricVehicle(battery_capacity, min_soc, max_soc, charging_capacity, charging_connectivity, charging_preference)
    simulator = TripSimulator(ev)
    simulator.generate_trip_data(num_days, output_file)

# Example of how you might call this in another file:
# setup_ev_simulation(40, 0.2, 0.8, 22, True, 'Home', 365, 'output.csv')
