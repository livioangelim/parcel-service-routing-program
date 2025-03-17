from abc import ABC, abstractmethod
from typing import List
from .cargo import Cargo
from ..utils.distance import calculate_route_distance


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


class Truck(Vehicle):
    def can_transport(self, cargo: Cargo) -> bool:
        return cargo.category in ["standard", "express"]


class Drone(Vehicle):
    def can_transport(self, cargo: Cargo) -> bool:
        return cargo.weight <= 5.0 and cargo.category == "express"
