# package.py

class Package:
    """
    Represents a package with all relevant details required for delivery.
    """

    def __init__(self, package_id, address, city, state, zip_code,
                 delivery_deadline, weight, notes):
        self.package_id = package_id          # Unique ID for the package
        self.address = address.strip()        # Delivery address
        self.city = city.strip()              # Delivery city
        self.state = state.strip()            # Delivery state
        self.zip_code = zip_code.strip()      # Delivery ZIP code
        self.delivery_deadline = delivery_deadline.strip()  # Delivery deadline
        self.weight = weight.strip()          # Package weight
        self.notes = notes.strip()            # Special notes
        self.status = 'At Hub'                # Delivery status
        self.delivery_time = None             # Time of delivery
        self.departure_time = None            # Time when the package left the hub

    def __str__(self):
        """
        Returns a string representation of the package details.
        """
        delivery_time_str = self.delivery_time.strftime('%I:%M %p') if self.delivery_time else 'N/A'
        departure_time_str = self.departure_time.strftime('%I:%M %p') if self.departure_time else 'N/A'
        return (f"Package ID: {self.package_id}, Address: {self.address}, "
                f"City: {self.city}, State: {self.state}, ZIP: {self.zip_code}, "
                f"Deadline: {self.delivery_deadline}, Weight: {self.weight}kg, "
                f"Status: {self.status}, Departure Time: {departure_time_str}, "
                f"Delivery Time: {delivery_time_str}, Notes: {self.notes}")
