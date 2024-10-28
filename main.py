# Student ID: 123456789

# main.py

import csv
from package import Package
from hash_table import HashTable
from truck import Truck
from distance import DistanceData
from datetime import datetime, timedelta

# Define a base date for all datetime objects
BASE_DATE = datetime.strptime('2023-01-01', '%Y-%m-%d').date()


def parse_time_with_base_date(time_str):
    """
    Parses a time string and attaches the base date.
    """
    time = datetime.strptime(time_str, '%I:%M %p')
    return time.replace(year=BASE_DATE.year, month=BASE_DATE.month, day=BASE_DATE.day)


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
                delivery_deadline = data[5].strip()
                if delivery_deadline == 'EOD':
                    deadline_time = parse_time_with_base_date('11:59 PM')
                else:
                    deadline_time = parse_time_with_base_date(delivery_deadline)
                package = Package(
                    package_id=package_id,
                    address=data[1].strip(),
                    city=data[2].strip(),
                    state=data[3].strip(),
                    zip_code=data[4].strip(),
                    delivery_deadline=delivery_deadline,
                    weight=data[6].strip(),
                    notes=data[7].strip() if len(data) > 7 else ''
                )
                package.deadline_time = deadline_time
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
        # Collect the address update event
        update_event = {
            'event_type': 'update',
            'package_id': '9',
            'event_time': parse_time_with_base_date('10:20 AM'),
            'message': 'Updated address for Package 9 at 10:20 AM.'
        }
        return update_event
    else:
        return None


def assign_packages(truck, packages, current_time, package_table):
    """
    Assigns packages to the truck for the next trip based on constraints.
    """
    available_space = Truck.MAX_CAPACITY - len(truck.packages)
    assigned_packages = []
    assigned_package_ids = set(p.package_id for p in truck.packages)

    # Filter packages that are available (not delayed) and can be loaded now
    available_packages = []
    for package in packages:
        # Check if package is already delivered or en route
        if package.status != 'At Hub':
            continue

        # Skip if package is already assigned to this truck
        if package.package_id in assigned_package_ids:
            continue

        # Handle delayed packages
        if 'delayed' in package.notes.lower():
            delayed_time = parse_time_with_base_date('09:05 AM')
            if current_time < delayed_time:
                continue  # Skip delayed packages until they arrive

        # Handle wrong address (package #9)
        if package.package_id == '9':
            address_update_time = parse_time_with_base_date('10:20 AM')
            if current_time < address_update_time:
                continue  # Skip until address is updated

        # Apply package constraints
        if 'can only be on truck 2' in package.notes.lower():
            if truck.truck_id != 2:
                continue  # Skip if package must be on Truck 2

        # Add package to available packages
        available_packages.append(package)

    # Sort available packages by delivery deadline (earlier deadlines first)
    available_packages.sort(key=lambda p: (p.deadline_time, p.package_id))

    # Assign packages to the truck until it's full or no more packages
    for package in available_packages:
        if len(assigned_packages) >= Truck.MAX_CAPACITY:
            break

        # Handle 'must be delivered with' constraints
        if 'must be delivered with' in package.notes.lower():
            # Ensure all related packages are assigned together
            related_ids = package.notes.lower().replace('must be delivered with', '').split(',')
            related_ids = [rid.strip().strip('"') for rid in related_ids]
            related_ids.append(package.package_id)  # Include current package

            # Check if any related packages are at the hub
            related_packages_at_hub = [package_table.lookup(rid) for rid in related_ids if
                                       package_table.lookup(rid).status == 'At Hub']

            if related_packages_at_hub:
                # Need to assign all related packages together
                total_needed_space = len(related_packages_at_hub)
                if len(assigned_packages) + total_needed_space <= Truck.MAX_CAPACITY:
                    for related_package in related_packages_at_hub:
                        assigned_packages.append(related_package)
                        assigned_package_ids.add(related_package.package_id)
                        related_package.status = 'En Route'  # Mark as en route
                else:
                    continue  # Not enough space
            else:
                # All related packages have been delivered; proceed to assign the current package
                assigned_packages.append(package)
                assigned_package_ids.add(package.package_id)
                package.status = 'En Route'  # Mark as en route
            continue  # Move to next package

        # Assign package if there's space
        assigned_packages.append(package)
        assigned_package_ids.add(package.package_id)
        package.status = 'En Route'  # Mark as en route

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
    current_time = parse_time_with_base_date('08:00 AM')
    address_updated = False  # Flag to ensure package 9's address is updated only once

    # Create trucks
    truck1 = Truck(truck_id=1, departure_time=current_time)
    truck2 = Truck(truck_id=2, departure_time=current_time)

    # Prepare list of all packages
    all_packages = [package_table.lookup(str(i)) for i in range(1, 41)]

    # Collect all events (both loading and delivery)
    events = []

    # Simulation loop
    while any(p.status != 'Delivered' for p in all_packages):
        # Update package #9's address at 10:20 AM
        if not address_updated and current_time >= parse_time_with_base_date('10:20 AM'):
            update_event = update_package_address(package_table)
            if update_event:
                events.append(update_event)
            address_updated = True

        # List to keep track of trucks that will deliver packages
        trucks_to_dispatch = []

        # Only assign packages to trucks that are at the hub and available
        if truck1.time <= current_time and not truck1.packages:
            truck1_packages = assign_packages(truck1, all_packages, current_time, package_table)
            if truck1_packages:
                loading_events = truck1.load_packages(truck1_packages)
                events.extend(loading_events)
                trucks_to_dispatch.append(truck1)
        if truck2.time <= current_time and not truck2.packages:
            truck2_packages = assign_packages(truck2, all_packages, current_time, package_table)
            if truck2_packages:
                loading_events = truck2.load_packages(truck2_packages)
                events.extend(loading_events)
                trucks_to_dispatch.append(truck2)

        # If no trucks are dispatched, advance time
        if not trucks_to_dispatch:
            current_time += timedelta(minutes=1)
            continue

        # Deliver packages and collect delivery events
        for truck in trucks_to_dispatch:
            deliveries = truck.deliver_packages(distance_data)
            events.extend(deliveries)

        # Update current time to the earliest time when a truck returns
        truck_return_times = [truck.time for truck in [truck1, truck2] if truck.time > current_time]
        if truck_return_times:
            current_time = min(truck_return_times)
        else:
            current_time += timedelta(minutes=1)

        # Reset trucks for next trip
        for truck in [truck1, truck2]:
            if truck.time <= current_time and not truck.packages:
                truck.reset_for_next_trip(current_time)

    # Calculate total mileage after simulation
    total_mileage = truck1.mileage + truck2.mileage

    # Sort events by event_time
    events.sort(key=lambda x: x['event_time'])

    # Print all events in chronological order
    for event in events:
        if event['event_type'] == 'load':
            print(f"Package {event['package_id']} loaded onto Truck {event['truck_id']} at {event['event_time'].strftime('%I:%M %p')}.")
        elif event['event_type'] == 'delivery':
            print(f"Delivered Package {event['package_id']} at {event['event_time'].strftime('%I:%M %p')} by Truck {event['truck_id']}.")
        elif event['event_type'] == 'update':
            print(event['message'])

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
        return f'Delivered by Truck {package.truck_id} at {package.delivery_time.strftime("%I:%M %p")}'
    else:
        return f'En Route on Truck {package.truck_id}'


def get_package_address(package, user_time):
    if package.package_id == '9':
        address_update_time = parse_time_with_base_date('10:20 AM')
        if user_time < address_update_time:
            return package.original_address
        else:
            return package.address
    else:
        return package.address


def get_package_city_state_zip(package, user_time):
    if package.package_id == '9':
        address_update_time = parse_time_with_base_date('10:20 AM')
        if user_time < address_update_time:
            return package.original_city, package.original_state, package.original_zip_code
        else:
            return package.city, package.state, package.zip_code
    else:
        return package.city, package.state, package.zip_code


def print_package_statuses(package_table, user_time):
    for package_id in range(1, 41):
        package = package_table.lookup(str(package_id))
        if package:
            status = get_package_status(package, user_time)
            address = get_package_address(package, user_time)
            city, state, zip_code = get_package_city_state_zip(package, user_time)
            print(f"Package {package.package_id}:")
            print(f"  Address: {address}, {city}, {state} {zip_code}")
            print(f"  Delivery Deadline: {package.delivery_deadline}")
            print(f"  Weight: {package.weight} kg")
            print(f"  Status at {user_time.strftime('%I:%M %p')}: {status}")
            print()


def print_single_package_status(package_table, package_id, user_time):
    package = package_table.lookup(package_id)
    if package:
        status = get_package_status(package, user_time)
        address = get_package_address(package, user_time)
        city, state, zip_code = get_package_city_state_zip(package, user_time)
        print(f"Package {package.package_id}:")
        print(f"  Address: {address}, {city}, {state} {zip_code}")
        print(f"  Delivery Deadline: {package.delivery_deadline}")
        print(f"  Weight: {package.weight} kg")
        print(f"  Status at {user_time.strftime('%I:%M %p')}: {status}")
        print()
    else:
        print("Package not found.")


def print_packages_by_address(package_table, address, user_time):
    """
    Prints the status of all packages matching the given address at the specified time.
    """
    found = False
    for package_id in range(1, 41):
        package = package_table.lookup(str(package_id))
        if package:
            package_address = get_package_address(package, user_time)
            if package_address.lower() == address.lower():
                status = get_package_status(package, user_time)
                city, state, zip_code = get_package_city_state_zip(package, user_time)
                print(f"Package {package.package_id}:")
                print(f"  Address: {package_address}, {city}, {state} {zip_code}")
                print(f"  Delivery Deadline: {package.delivery_deadline}")
                print(f"  Weight: {package.weight} kg")
                print(f"  Status at {user_time.strftime('%I:%M %p')}: {status}")
                print()
                found = True
    if not found:
        print(f"No packages found for address '{address}'.")


def user_interface(package_table, total_mileage):
    """
    Provides an interface for the user to view package statuses and total mileage.
    """
    while True:
        print("\nWGUPS Package Delivery System")
        print("1. View status of all packages at a given time")
        print("2. View status of a single package at a given time")
        print("3. View status of packages by address at a given time")
        print("4. View total mileage")
        print("5. Exit")

        choice = input("Please select an option: ")

        if choice == '1':
            time_input = input("Enter the time (HH:MM AM/PM): ")
            user_time = parse_time_with_base_date(time_input)
            print_package_statuses(package_table, user_time)
        elif choice == '2':
            package_id = input("Enter the package ID: ")
            time_input = input("Enter the time (HH:MM AM/PM): ")
            user_time = parse_time_with_base_date(time_input)
            print_single_package_status(package_table, package_id, user_time)
        elif choice == '3':
            address = input("Enter the address: ")
            time_input = input("Enter the time (HH:MM AM/PM): ")
            user_time = parse_time_with_base_date(time_input)
            print_packages_by_address(package_table, address, user_time)
        elif choice == '4':
            print(f"Total mileage: {total_mileage:.2f}")
        elif choice == '5':
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
