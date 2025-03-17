from typing import Tuple
import math

Point = Tuple[float, float]


def calculate_distance(point_a: Point, point_b: Point) -> float:
    """Calculate Euclidean distance between two points."""
    x1, y1 = point_a
    x2, y2 = point_b
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_route_distance(points: list[Point]) -> float:
    """Calculate total distance of a route."""
    if len(points) < 2:
        return 0.0
    return sum(calculate_distance(points[i], points[i+1])
               for i in range(len(points)-1))
