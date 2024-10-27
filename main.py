# main.py

# Student ID: [Your Student ID Here]

from package import Package
from hash_table import HashTable


def load_packages(package_table):
    """
    Loads package data into the hash table.
    In practice, this would read from a file. For now, we'll use hardcoded data.
    """
    package_data = [
        ['1', '195 W Oakland Ave', 'Salt Lake City',
            'UT', '84115', '10:30 AM', '21', ''],
        ['2', '2530 S 500 E', 'Salt Lake City', 'UT', '84106', 'EOD', '44', ''],
        ['3', '233 Canyon Rd', 'Salt Lake City', 'UT',
            '84103', 'EOD', '2', 'Can only be on truck 2'],
        # Add more package data as needed...
    ]

    for data in package_data:
        package_id = data[0]
        package = Package(
            package_id=package_id,
            address=data[1],
            city=data[2],
            state=data[3],
            zip_code=data[4],
            delivery_deadline=data[5],
            weight=data[6],
            notes=data[7]
        )
        package_table.insert(package_id, package)


def main():
    """
    Main function to run the WGUPS Routing Program.
    """
    # Initialize the hash table with a suitable size to reduce collisions
    package_table = HashTable(size=40)  # Adjust size as needed

    # Load packages into the hash table
    load_packages(package_table)

    # Example of looking up a package
    package = package_table.lookup('1')
    if package:
        print(f"Package {package.package_id} found:")
        print(package)
    else:
        print("Package not found.")

    # Update package status
    package_table.update_status('1', 'En Route', '9:05 AM')

    # Print all packages
    print("\nAll Packages:")
    package_table.print_all_packages()


if __name__ == "__main__":
    main()
