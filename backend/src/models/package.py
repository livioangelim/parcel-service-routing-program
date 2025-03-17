from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Package:
    id: int
    source: str
    destination: str
    weight: float
    delivery_time: Optional[datetime] = None
    priority: str = "standard"
    status: str = "pending"

    def validate(self) -> bool:
        """Validate package data."""
        if not (0.1 <= self.weight <= 1000):
            raise ValueError("Weight must be between 0.1 and 1000 kg")
        if not self.source or not self.destination:
            raise ValueError("Source and destination are required")
        return True
