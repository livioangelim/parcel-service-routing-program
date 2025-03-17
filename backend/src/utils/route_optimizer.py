from typing import Dict, List, Tuple
from ..models.cargo import Cargo
from ..models.vehicle import Vehicle
from .distance import calculate_route_distance


def optimize_route(cargo: Cargo, available_vehicles: Dict[str, List[Vehicle]]) -> Tuple[List[str], Vehicle]:
    """Find optimal route and vehicle for cargo delivery."""
    suitable_vehicles = []

    # Find all suitable vehicles
    for vehicle_list in available_vehicles.values():
        for vehicle in vehicle_list:
            if vehicle.can_transport(cargo):
                suitable_vehicles.append(vehicle)

    if not suitable_vehicles:
        raise ValueError("No suitable vehicle found for this cargo")

    # Find vehicle with best route
    best_route = None
    best_vehicle = None
    best_cost = float('inf')

    for vehicle in suitable_vehicles:
        route = calculate_vehicle_route(vehicle, cargo)
        cost = calculate_route_cost(route, vehicle)

        if cost < best_cost:
            best_cost = cost
            best_route = route
            best_vehicle = vehicle

    return best_route, best_vehicle
