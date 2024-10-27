# main.py

import csv  # Import csv module
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
        with open(filename, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header line if present
            for data in reader:
                package_id = data[0].strip()
                package = Package(
                    package_id=package_id,
                    address=data[1].strip(),
                    city=data[2].strip(),
                    state=data[3].strip(),
                    zip_code=data[4].strip(),
                    delivery_deadline=data[5].strip(),
                    weight=data[6].strip(),
                    notes=data[7].strip() if len(data) > 7 else ''
                )
                package_table.insert(package_id, package)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        print("Please ensure the CSV files are in the correct directory.")
        exit(1)

def update_package_address(package_table):
    """
    Updates the address for package #9 at 10:20 AM.
    """
    package_9 = package_table.lookup('9')
    if package_9:
        # Simulate the address correction at 10:20 AM
        package_9.address = '410 S State St'  # Corrected address
        package_9.city = 'Salt Lake City'
        package_9.state = 'UT'
        package_9.zip_code = '84111'
        print("Updated address for Package 9 at 10:20 AM.")
    else:
        print("Package 9 not found.")

def assign_packages(truck, packages, current_time, package_table):
    """
    Assigns packages to the truck for the next trip based on constraints.
    """
    available_space = Truck.MAX_CAPACITY - len(truck.packages)
    assigned_packages = []
    assigned_package_ids = set(p.package_id for p in truck.packages)

    # Filter packages that are available (not delayed) and can be loaded now
    for package in packages:
        # Check if package is already delivered or en route
        if package.status != 'At Hub':
            continue

        # Skip if package is already assigned to this truck
        if package.package_id in assigned_package_ids:
            continue

        # Handle delayed packages
        if 'delayed' in package.notes.lower():
            delayed_time = datetime.strptime('09:05 AM', '%I:%M %p')
            if current_time < delayed_time:
                continue  # Skip delayed packages until they arrive

        # Handle wrong address (package #9)
        if package.package_id == '9':
            address_update_time = datetime.strptime('10:20 AM', '%I:%M %p')
            if current_time < address_update_time:
                continue  # Skip until address is updated

        # Apply package constraints
        if 'can only be on truck 2' in package.notes.lower():
            if truck.truck_id != 2:
                continue  # Skip if package must be on Truck 2

        if 'must be delivered with' in package.notes.lower():
            # Ensure all related packages are assigned together
            related_ids = package.notes.lower().replace('must be delivered with', '').split(',')
            related_ids = [rid.strip().strip('"') for rid in related_ids]
            related_ids.append(package.package_id)  # Include current package

            # Check if any related packages are at the hub
            related_packages_at_hub = [package_table.lookup(rid) for rid in related_ids if package_table.lookup(rid).status == 'At Hub']

            if related_packages_at_hub:
                # Need to assign all related packages together
                total_needed_space = len(related_packages_at_hub)
                if available_space >= total_needed_space:
                    for related_package in related_packages_at_hub:
                        assigned_packages.append(related_package)
                        assigned_package_ids.add(related_package.package_id)
                        related_package.status = 'En Route'  # Mark as en route
                        available_space -= 1
                else:
                    continue  # Not enough space
            else:
                # All related packages have been delivered; proceed to assign the current package
                if available_space > 0:
                    assigned_packages.append(package)
                    assigned_package_ids.add(package.package_id)
                    available_space -= 1
                    package.status = 'En Route'  # Mark as en route
                else:
                    break  # Truck is full
            continue  # Move to next package

        # Assign package if there's space
        if available_space > 0:
            assigned_packages.append(package)
            assigned_package_ids.add(package.package_id)
            available_space -= 1
            package.status = 'En Route'  # Mark as en route
        else:
            break  # Truck is full

    return assigned_packages

def main():
    """
    Main function to run the WGUPS Routing Program.
    """
    # Initialize the hash table
    package_table = HashTable(size=40)

    # Load packages into the hash table from the CSV directory
    load_packages_from_csv('CSV/packages.csv', package_table)

    # Load distance data
    distance_data = DistanceData()
    distance_data.load_addresses('CSV/addresses.csv')
    distance_data.load_distances('CSV/distances.csv')

    # Initialize variables
    total_mileage = 0.0
    current_time = datetime.strptime('08:00 AM', '%I:%M %p')
    address_updated = False  # Flag to ensure package 9's address is updated only once

    # Create trucks
    truck1 = Truck(truck_id=1, departure_time=current_time)
    truck2 = Truck(truck_id=2, departure_time=current_time)

    # Prepare list of all packages
    all_packages = [package_table.lookup(str(i)) for i in range(1, 41)]

    # Simulation loop
    while any(p.status != 'Delivered' for p in all_packages):
        # Update package #9's address at 10:20 AM
        if not address_updated and current_time >= datetime.strptime('10:20 AM', '%I:%M %p'):
            update_package_address(package_table)
            address_updated = True

        # Assign packages to trucks
        truck1_packages = assign_packages(truck1, all_packages, current_time, package_table)
        truck2_packages = assign_packages(truck2, all_packages, current_time, package_table)

        # Check if any packages were assigned
        if not truck1_packages and not truck2_packages:
            # Advance time if no packages can be loaded now
            current_time += timedelta(minutes=5)
            continue

        # Load packages onto trucks
        if truck1_packages:
            truck1.load_packages(truck1_packages)
        if truck2_packages:
            truck2.load_packages(truck2_packages)

        # Deliver packages
        if truck1.packages:
            truck1.deliver_packages(distance_data)
            total_mileage += truck1.mileage
        if truck2.packages:
            truck2.deliver_packages(distance_data)
            total_mileage += truck2.mileage

        # Update current time to the earliest time when a truck returns
        truck_return_times = []
        if truck1.time > current_time:
            truck_return_times.append(truck1.time)
        if truck2.time > current_time:
            truck_return_times.append(truck2.time)
        if truck_return_times:
            current_time = min(truck_return_times)
        else:
            current_time += timedelta(minutes=5)

        # Reset trucks for next trip
        if truck1.time <= current_time:
            truck1.reset_for_next_trip(current_time)
        if truck2.time <= current_time:
            truck2.reset_for_next_trip(current_time)

    # Print total mileage
    print(f"\nTotal mileage: {total_mileage:.2f}")

    # Verify total mileage is under 140 miles
    if total_mileage <= 140:
        print("Total mileage is within the limit.")
    else:
        print("Total mileage exceeds the limit!")

    # Provide user interface to check package statuses
    user_interface(package_table, total_mileage)

def get_package_status(package, user_time):
    if user_time < package.departure_time:
        return 'At Hub'
    elif package.delivery_time and user_time >= package.delivery_time:
        return f'Delivered at {package.delivery_time.strftime("%I:%M %p")}'
    else:
        return 'En Route'

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

if __name__ == "__main__":
    main()
