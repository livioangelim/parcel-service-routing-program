from abc import ABC, abstractmethod
from typing import List, Dict, Union
from src.models.cargo import Cargo, CargoCategory
from src.utils.distance import calculate_route_distance


class Vehicle(ABC):
    def __init__(self, id: str, capacity: float, speed: float):
        self.id = id
        self.capacity = capacity
        self.speed = speed
        self.cargo_items: List[Cargo] = []

    @abstractmethod
    def can_transport(self, cargo: Cargo) -> bool:
        """Check if vehicle can transport specific cargo type"""
        pass

    def add_cargo(self, cargo: Cargo) -> bool:
        if self.get_total_weight() + cargo.weight <= self.capacity and self.can_transport(cargo):
            self.cargo_items.append(cargo)
            return True
        return False

    def get_total_weight(self) -> float:
        return sum(cargo.weight for cargo in self.cargo_items)

    def calculate_eta(self, distance: float) -> float:
        """Calculate estimated time of arrival in hours"""
        return distance / self.speed if self.speed > 0 else float('inf')

    def calculate_route(self, cargo: Cargo) -> Dict[str, Union[List[str], List[float]]]:
        """Calculate optimal route for cargo delivery"""
        if not self.can_transport(cargo):
        return cargo.category in [CargoCategory.STANDARD, CargoCategory.EXPRESS]


class Drone(Vehicle):
    def can_transport(self, cargo: Cargo) -> bool:
        return cargo.weight <= 5.0 and cargo.category == CargoCategory.EXPRESS
