# package.py

class Package:
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, weight, notes):
        self.package_id = package_id
        self.address = address
        self.original_address = address
        self.city = city
        self.original_city = city
        self.state = state
        self.original_state = state
        self.zip_code = zip_code
        self.original_zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.notes = notes
        self.status = 'At Hub'  # Possible statuses: 'At Hub', 'En Route', 'Delivered'
        self.departure_time = None  # Time when the package left the hub
        self.delivery_time = None   # Time when the package was delivered
        self.truck_id = None        # Truck number that delivered the package
        self.deadline_time = None   # Parsed delivery deadline as datetime object

    def __str__(self):
        return f"Package {self.package_id}: {self.address}, {self.city}, {self.state} {self.zip_code}"
