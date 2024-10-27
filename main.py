# main.py

from package import Package
from hash_table import HashTable
from truck import Truck
from distance import DistanceData
from datetime import datetime, timedelta

def load_packages_from_csv(filename, package_table):
    """
    Reads package data from a CSV file and inserts packages into the hash table.
    """
    try:
        with open(filename, 'r') as file:
            next(file)  # Skip header line if present
            for line in file:
                data = line.strip().split(',')
                package_id = data[0]
                package = Package(
                    package_id=package_id,
                    address=data[1],
                    city=data[2],
                    state=data[3],
                    zip_code=data[4],
                    delivery_deadline=data[5],
                    weight=data[6],
                    notes=data[7] if len(data) > 7 else ''
                )
                package_table.insert(package_id, package)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        print("Please ensure the CSV files are in the correct directory.")
        exit(1)

def group_packages(package_table):
    """
    Groups packages based on special conditions and returns lists for each truck.
    """
    truck1_packages = []
    truck2_packages = []
    truck3_packages = []

    delayed_packages = []
    wrong_address_packages = []
    must_be_delivered_together = []

    for package_id in range(1, 41):  # Package IDs from 1 to 40
        package = package_table.lookup(str(package_id))
        if package:
            notes = package.notes.lower()
            if 'delayed' in notes:
                delayed_packages.append(package)
            elif 'wrong address' in notes:
                wrong_address_packages.append(package)
            elif 'must be delivered with' in notes or 'can only be on truck 2' in notes:
                must_be_delivered_together.append(package)
            else:
                if package.delivery_deadline != 'EOD':
                    truck1_packages.append(package)
                else:
                    truck3_packages.append(package)

    # Assign packages that must be delivered together to Truck 2
    truck2_packages.extend(must_be_delivered_together)

    # Add delayed packages to Truck 2 (assuming it leaves after 9:05 AM)
    truck2_packages.extend(delayed_packages)

    # Add wrong address packages to Truck 3 (address corrected before departure)
    truck3_packages.extend(wrong_address_packages)

    return truck1_packages, truck2_packages, truck3_packages

def update_package_address(package_table):
    """
    Updates the address for package #9 at 10:20 AM.
    """
    package_9 = package_table.lookup('9')
    if package_9:
        # Simulate the address correction at 10:20 AM
        corrected_time = datetime.strptime('10:20 AM', '%I:%M %p')
        package_9.address = '410 S State St'  # Corrected address
        package_9.city = 'Salt Lake City'
        package_9.state = 'UT'
        package_9.zip_code = '84111'
        print("Updated address for Package 9 at 10:20 AM.")
    else:
        print("Package 9 not found.")

def print_package_statuses(package_table, user_time):
    for package_id in range(1, 41):
        package = package_table.lookup(str(package_id))
        if package:
            status = get_package_status(package, user_time)
            print(f"Package {package_id}: {status}")

def print_single_package_status(package_table, package_id, user_time):
    package = package_table.lookup(package_id)
    if package:
        status = get_package_status(package, user_time)
        print(f"Package {package_id}: {status}")
    else:
        print("Package not found.")

def get_package_status(package, user_time):
    if user_time < package.departure_time:
        return 'At Hub'
    elif package.delivery_time and user_time >= package.delivery_time:
        return f'Delivered at {package.delivery_time.strftime("%I:%M %p")}'
    else:
        return 'En Route'

def user_interface(package_table, total_mileage):
    """
    Provides an interface for the user to view package statuses and total mileage.
    """
    while True:
        print("\nWGUPS Package Delivery System")
        print("1. View status of all packages at a given time")
        print("2. View status of a single package at a given time")
        print("3. View total mileage")
        print("4. Exit")

        choice = input("Please select an option: ")

        if choice == '1':
            time_input = input("Enter the time (HH:MM AM/PM): ")
            user_time = datetime.strptime(time_input, '%I:%M %p')
            print_package_statuses(package_table, user_time)
        elif choice == '2':
            package_id = input("Enter the package ID: ")
            time_input = input("Enter the time (HH:MM AM/PM): ")
            user_time = datetime.strptime(time_input, '%I:%M %p')
            print_single_package_status(package_table, package_id, user_time)
        elif choice == '3':
            print(f"Total mileage: {total_mileage:.2f}")
        elif choice == '4':
            break
        else:
            print("Invalid option. Please try again.")

def main():
    """
    Main function to run the WGUPS Routing Program.
    """
    # Initialize the hash table
    package_table = HashTable(size=40)

    # Load packages into the hash table from the CSV directory
    load_packages_from_csv('CSV/packages.csv', package_table)

    # Update package address at 10:20 AM (simulate during the run)
    update_package_address(package_table)

    # Initialize trucks with departure times
    start_time = datetime.strptime('08:00 AM', '%I:%M %p')
    truck1 = Truck(truck_id=1, departure_time=start_time)
    truck2 = Truck(truck_id=2, departure_time=start_time + timedelta(hours=1, minutes=5))  # Leaves at 9:05 AM
    truck3 = Truck(truck_id=3, departure_time=start_time + timedelta(hours=2))  # Leaves at 10:00 AM

    # Ensure trucks start at the hub's address
    hub_address = '4001 South 700 East'
    truck1.current_location = hub_address
    truck2.current_location = hub_address
    truck3.current_location = hub_address

    # Group packages based on constraints
    truck1_packages, truck2_packages, truck3_packages = group_packages(package_table)

    # Load packages onto trucks
    truck1.load_packages(truck1_packages)
    truck2.load_packages(truck2_packages)
    truck3.load_packages(truck3_packages)

    # Load distance data from the CSV directory
    distance_data = DistanceData()
    distance_data.load_addresses('CSV/addresses.csv')
    distance_data.load_distances('CSV/distances.csv')

    # Deliver packages
    truck1.deliver_packages(distance_data)
    truck2.deliver_packages(distance_data)
    truck3.deliver_packages(distance_data)

    # Calculate total mileage
    total_mileage = truck1.mileage + truck2.mileage + truck3.mileage
    print(f"\nTotal mileage: {total_mileage:.2f}")

    # Verify total mileage is under 140 miles
    if total_mileage <= 140:
        print("Total mileage is within the limit.")
    else:
        print("Total mileage exceeds the limit!")

    # Provide user interface to check package statuses
    user_interface(package_table, total_mileage)

if __name__ == "__main__":
    main()
