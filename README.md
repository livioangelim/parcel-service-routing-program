# WGUPS Routing Program

## Overview

This program simulates a delivery system for the Western Governors University Parcel Service (WGUPS). It aims to deliver 40 packages under various constraints while keeping the total mileage under 140 miles.

## Files Included

- `package.py`: Contains the `Package` class representing individual packages.
- `hash_table.py`: Contains the `HashTable` and `Node` classes for managing package data.
- `truck.py`: Contains the `Truck` class for managing truck operations.
- `distance.py`: Contains the `DistanceData` class for handling distances and addresses.
- `main.py`: The main script that runs the program.
- `CSV/packages.csv`: CSV file containing package data.
- `CSV/addresses.csv`: CSV file containing address data.
- `CSV/distances.csv`: CSV file containing distance data.
- `README.md`: This file, containing documentation and steps completed.

## Steps Completed

1. **Custom Hash Table Implementation (Requirements A & B):**
   - Implemented a custom hash table without using built-in dictionaries or additional libraries.
   - Created insertion and lookup functions based on package IDs.
   - Stored all package details, including delivery status and time.

2. **Routing Algorithm (Requirement C):**
   - Developed an initial algorithm using the Nearest Neighbor approach to deliver all 40 packages.
   - Accounted for special conditions such as delayed packages, incorrect addresses, and packages that must be delivered together.
   - Simulated delivery times and updated package statuses accordingly.
   - **Current Challenge:** The total mileage is **351.60 miles**, which exceeds the 140-mile limit.

3. **Time Simulation:**
   - Used the `datetime` module to simulate time accurately.
   - Calculated delivery times based on distances and average speed (18 mph).

4. **User Interface (Requirement D):**
   - Provided a console-based menu for users to view package statuses and total mileage.
   - Allowed users to check the status of all packages or individual packages at a specific time.



## Troubleshooting

- **FileNotFoundError:**
  - If you encounter an error stating that a CSV file is not found, ensure the file exists in the `CSV` directory.
  - Verify the file names and paths.

- **Total Mileage Exceeds Limit:**
  - The current total mileage is over the limit. Proceed to optimize the delivery routes as per the steps outlined in the "Optimization" section.

- **Incorrect Package Statuses:**
  - Ensure that the time entered is in the correct format (e.g., `08:00 AM`).
  - Check that the delivery times are being calculated correctly.


## What's Left to Do

- **Optimization (Requirement C):**
  - **Critical Task:** Optimize the delivery routes to reduce the total mileage below the 140-mile limit.
  - Implement more advanced routing algorithms or adjust truck loading strategies.
  - Consider multiple trips per truck if necessary.

- **Testing and Validation:**
  - Thoroughly test the program after optimization to ensure all packages are delivered within their deadlines.
  - Verify that special delivery notes and constraints are still properly handled.

- **Error Handling:**
  - Enhance error handling for potential edge cases (e.g., invalid input from the user interface).

- **Documentation:**
  - Add comments and docstrings where necessary to improve code readability.
  - Provide additional documentation or a user manual if required.
