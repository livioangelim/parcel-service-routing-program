import os
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from flask import Flask, request
from flask_cors import CORS
from src.models.cargo import Cargo, CargoCategory
from src.models.vehicle import Vehicle, Truck, Drone
from src.models.hash_table import HashTable
from src.utils.route_optimizer import optimize_route
from typing import Dict, Any, Union, List, Tuple
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
CORS(app)

# Initialize data structures
cargo_table = HashTable()
vehicles = {
    'trucks': [Truck(f"T{i}", 1000, 60) for i in range(3)],
    'drones': [Drone(f"D{i}", 5, 100) for i in range(2)]
}


@app.route('/health')
def health_check() -> Tuple[Dict[str, str], int]:
    """Health check endpoint for monitoring"""
    return {"status": "healthy", "version": "1.0"}, 200


@app.errorhandler(HTTPException)
def handle_http_error(error: HTTPException) -> Tuple[Dict[str, str], int]:
    """Handle HTTP exceptions"""
    return {
        'error': error.__class__.__name__,
        'message': error.description
    }, error.code


@app.errorhandler(Exception)
def handle_error(error: Exception) -> Tuple[Dict[str, str], int]:
    """Handle general exceptions"""
    app.logger.error(f"Unexpected error: {error}")
    return {
        'error': 'internal_server_error',
        'message': 'An unexpected error occurred'
    }, 500


@app.route('/api/route', methods=['POST'])
def calculate_route() -> Tuple[Dict[str, Any], int]:
    """Calculate optimal delivery route"""
    try:
        data: Dict[str, Any] = request.get_json()

        # Validate required fields
        required_fields = ['source', 'destination', 'weight']
        missing_fields = [
            field for field in required_fields if field not in data]
        if missing_fields:
            return {
                'error': 'validation_error',
                'message': f'Missing required fields: {", ".join(missing_fields)}'
            }, 400

        # Create cargo instance
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

        return {
            'route': route_data['path'],
            'distances': route_data['distances'],
            'cost': cost,
            'cargo_id': cargo.id,
            'vehicle_id': vehicle.id
        }, 200

    except ValueError as e:
        return {
            'error': 'validation_error',
            'message': str(e)
        }, 400
    except Exception as e:
        app.logger.error(f"Route calculation error: {e}")
        return {
            'error': 'calculation_error',
            'message': 'Failed to calculate route'
        }, 500


def calculate_delivery_cost(
    route: Dict[str, Union[List[str], List[float]]],
    cargo: Cargo,
    vehicle: Vehicle
) -> float:
    """
    Calculate delivery cost based on route distance and cargo weight

    Args:
        route: Dictionary containing path and distances
        cargo: Cargo instance
        vehicle: Vehicle instance

    Returns:
        float: Total delivery cost
    """
    base_rate = float(os.getenv('BASE_RATE', '10.0'))
    distance_rate = 2.0 if isinstance(vehicle, Truck) else 4.0
    weight_rate = float(os.getenv('WEIGHT_RATE', '1.5'))

    total_distance = sum(route['distances'])
    return base_rate + (distance_rate * total_distance) + (weight_rate * cargo.weight)


if __name__ == '__main__':
    # Configure logging
    import logging
    logging.basicConfig(level=logging.INFO)

    # Start server
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
