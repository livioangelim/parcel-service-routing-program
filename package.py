# package.py

class Package:
    """
    Represents a package with all relevant details required for delivery.
    """

    def __init__(self, package_id, address, city, state, zip_code,
                 delivery_deadline, weight, notes):
        self.package_id = package_id          # Unique ID for the package
        self.address = address                # Delivery address
        self.city = city                      # Delivery city
        self.state = state                    # Delivery state
        self.zip_code = zip_code              # Delivery ZIP code
        self.delivery_deadline = delivery_deadline  # Delivery deadline
        self.weight = weight                  # Package weight
        self.notes = notes                    # Special notes
        self.status = 'At Hub'                # Delivery status
        self.delivery_time = None             # Time of delivery

    def __str__(self):
        """
        Returns a string representation of the package details.
        """
        return (f"Package ID: {self.package_id}, Address: {self.address}, "
                f"City: {self.city}, State: {
                    self.state}, ZIP: {self.zip_code}, "
                f"Deadline: {self.delivery_deadline}, Weight: {
                    self.weight}kg, "
                f"Status: {self.status}, Delivery Time: {self.delivery_time}, "
                f"Notes: {self.notes}")
