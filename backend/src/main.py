from flask import Flask, request, jsonify
from flask_cors import CORS
from models.cargo import Cargo, CargoCategory
from models.vehicle import Truck, Drone
from models.hash_table import HashTable
from utils.route_optimizer import optimize_route
from typing import Dict, Any, Union, List

app = Flask(__name__)
CORS(app)
cargo_table = HashTable()
vehicles = {
    'trucks': [Truck(f"T{i}", 1000, 60) for i in range(3)],
    'drones': [Drone(f"D{i}", 5, 100) for i in range(2)]
}


@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({
        'error': type(error).__name__,
        'message': str(error)
    }), 400


@app.route('/api/route', methods=['POST'])
def calculate_route():
    try:
        data: Dict[str, Any] = request.get_json()
        cargo = Cargo(
            id=len(cargo_table) + 1,
            source=data['source'],
            destination=data['destination'],
            weight=float(data['weight']),
            category=CargoCategory(data.get('category', 'standard'))
        )
        cargo.validate()

        # Add to hash table
        cargo_table.insert(cargo.id, cargo)

        # Find suitable vehicle and optimize route
        route_data, vehicle = optimize_route(cargo, vehicles)
        cost = calculate_delivery_cost(route_data, cargo, vehicle)

        return jsonify({
            'route': route_data['path'],
            'distances': route_data['distances'],
            'cost': cost,
            'cargo_id': cargo.id,
            'vehicle_id': vehicle.id
        })

    except (KeyError, ValueError) as e:
        return jsonify({
            'error': 'validation_error',
            'message': str(e)
        }), 400


def calculate_delivery_cost(route: Dict[str, Union[List[str], List[float]]], cargo: Cargo, vehicle: Vehicle) -> float:
    """Calculate delivery cost based on route distance and cargo weight"""
    base_rate = 10.0
    distance_rate = 2.0 if isinstance(vehicle, Truck) else 4.0
    weight_rate = 1.5

    total_distance = sum(route['distances'])
    return base_rate + (distance_rate * total_distance) + (weight_rate * cargo.weight)


if __name__ == '__main__':
    app.run(debug=True)
