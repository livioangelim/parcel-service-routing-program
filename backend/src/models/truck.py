from .package import Package
from ..utils.distance import calculate_distance


class Truck:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.packages = []

    def add_package(self, package):
        if self.get_total_weight() + package.weight <= self.capacity:
            self.packages.append(package)
            return True
        return False

    def get_total_weight(self):
        return sum(package.weight for package in self.packages)

    def calculate_route(self):
        # Implement route calculation logic
        pass
