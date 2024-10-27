# truck.py

from datetime import timedelta

class Truck:
    """
    Represents a delivery truck with capacity, speed, and package management.
    """

    MAX_CAPACITY = 16        # Maximum number of packages the truck can carry
    AVERAGE_SPEED = 18       # Average speed in miles per hour

    def __init__(self, truck_id, departure_time):
        self.truck_id = truck_id              # Unique identifier for the truck
        self.departure_time = departure_time  # Should be a datetime object
        self.packages = []                    # List to hold packages loaded onto the truck
        self.current_location = '4001 South 700 East'  # Starting location (Hub's address)
        self.mileage = 0.0                    # Total miles traveled by the truck
        self.time = departure_time            # Current time for the truck

    def load_packages(self, packages):
        """
        Loads multiple packages onto the truck.
        """
        for package in packages:
            if len(self.packages) < self.MAX_CAPACITY:
                self.packages.append(package)
                package.status = 'En Route'
                package.departure_time = self.departure_time
                print(f"Package {package.package_id} loaded onto Truck {self.truck_id} at {self.departure_time.strftime('%I:%M %p')}.")
            else:
                print(f"Truck {self.truck_id} is at full capacity.")
                break

    def deliver_packages(self, distance_data):
        """
        Delivers all packages loaded on the truck using the Nearest Neighbor Algorithm.
        """
        # Initialize unvisited locations
        unvisited = self.packages.copy()
        self.current_location = '4001 South 700 East'
        self.time = self.departure_time
        self.mileage = 0.0  # Reset mileage for the trip

        while unvisited:
            # Find the closest package destination
            min_distance = float('inf')
            next_package = None

            for package in unvisited:
                distance = distance_data.get_distance(self.current_location, package.address)
                if distance < min_distance:
                    min_distance = distance
                    next_package = package

            # Deliver the next package
            if next_package:
                self.mileage += min_distance
                travel_time = timedelta(hours=min_distance / self.AVERAGE_SPEED)
                self.time += travel_time
                next_package.delivery_time = self.time
                next_package.status = 'Delivered'
                print(f"Delivered Package {next_package.package_id} at {self.time.strftime('%I:%M %p')} by Truck {self.truck_id}.")
                self.current_location = next_package.address
                unvisited.remove(next_package)

        # Return to the hub
        distance_to_hub = distance_data.get_distance(self.current_location, '4001 South 700 East')
        self.mileage += distance_to_hub
        travel_time = timedelta(hours=distance_to_hub / self.AVERAGE_SPEED)
        self.time += travel_time
        self.current_location = '4001 South 700 East'

        # Clear the packages after delivery
        self.packages = []

    def reset_for_next_trip(self, new_departure_time):
        """
        Resets the truck's state for the next trip.
        """
        self.packages = []
        self.current_location = '4001 South 700 East'  # Hub address
        self.departure_time = new_departure_time
        self.time = new_departure_time
        self.mileage = 0.0  # Reset mileage

    def __str__(self):
        """
        Returns a string representation of the truck's status.
        """
        return (f"Truck ID: {self.truck_id}, Mileage: {self.mileage:.2f}, "
                f"Current Location: {self.current_location}, Time: {self.time.strftime('%I:%M %p')}")
