from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum


class CargoCategory(Enum):
    STANDARD = "standard"
    EXPRESS = "express"
    FRAGILE = "fragile"


@dataclass
class Cargo:
    id: int
    source: str
    destination: str
    weight: float
    category: CargoCategory
    delivery_time: Optional[datetime] = None
    status: str = "pending"

    def validate(self) -> bool:
        """Validate cargo data."""
        if not (0.1 <= self.weight <= 1000):
            raise ValueError("Weight must be between 0.1 and 1000 kg")
        if not self.source or not self.destination:
            raise ValueError("Source and destination are required")
        if not isinstance(self.category, CargoCategory):
            raise ValueError("Invalid cargo category")
        return True
