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
        self.departure_time = departure_time  # Datetime object
        self.packages = []                    # List to hold packages loaded onto the truck
        self.current_location = '4001 South 700 East'  # Starting location (Hub's address)
        self.mileage = 0.0                    # Total miles traveled by the truck
        self.time = departure_time            # Current time for the truck

    def load_packages(self, packages):
        """
        Loads multiple packages onto the truck.
        Returns a list of loading events.
        """
        loading_events = []
        for package in packages:
            if len(self.packages) < self.MAX_CAPACITY:
                self.packages.append(package)
                package.status = 'En Route'
                package.departure_time = self.departure_time
                package.truck_id = self.truck_id  # Assign the truck ID to the package
                # Collect the loading event
                loading_events.append({
                    'event_type': 'load',
                    'package_id': package.package_id,
                    'event_time': self.departure_time,
                    'truck_id': self.truck_id
                })
            else:
                break  # Truck is full
        return loading_events

    def deliver_packages(self, distance_data):
        """
        Delivers all packages loaded on the truck, prioritizing packages with deadlines.
        Returns a list of delivery events.
        """
        # Initialize unvisited locations
        delivery_events = []
        self.time = self.departure_time
        trip_mileage = 0.0  # Mileage for this trip

        # Separate packages with deadlines and without deadlines
        packages_with_deadlines = [p for p in self.packages if p.delivery_deadline != 'EOD']
        packages_without_deadlines = [p for p in self.packages if p.delivery_deadline == 'EOD']

        # Deliver packages with deadlines first
        for package_list in [packages_with_deadlines, packages_without_deadlines]:
            unvisited = package_list.copy()
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
                    trip_mileage += min_distance
                    travel_time = timedelta(hours=min_distance / self.AVERAGE_SPEED)
                    self.time += travel_time
                    next_package.delivery_time = self.time
                    next_package.status = 'Delivered'
                    # Collect the delivery event
                    delivery_events.append({
                        'event_type': 'delivery',
                        'package_id': next_package.package_id,
                        'event_time': next_package.delivery_time,
                        'truck_id': self.truck_id
                    })
                    self.current_location = next_package.address
                    unvisited.remove(next_package)

        # Return to the hub
        distance_to_hub = distance_data.get_distance(self.current_location, '4001 South 700 East')
        trip_mileage += distance_to_hub
        travel_time = timedelta(hours=distance_to_hub / self.AVERAGE_SPEED)
        self.time += travel_time
        self.current_location = '4001 South 700 East'

        # Update the truck's total mileage
        self.mileage += trip_mileage

        # Clear the packages after delivery
        self.packages = []

        return delivery_events

    def reset_for_next_trip(self, new_departure_time):
        """
        Resets the truck's state for the next trip.
        """
        self.departure_time = new_departure_time
        self.time = new_departure_time
        self.current_location = '4001 South 700 East'  # Hub address
        # Total mileage is cumulative over all trips

    def __str__(self):
        """
        Returns a string representation of the truck's status.
        """
        return (f"Truck ID: {self.truck_id}, Mileage: {self.mileage:.2f}, "
                f"Current Location: {self.current_location}, Time: {self.time.strftime('%I:%M %p')}")
