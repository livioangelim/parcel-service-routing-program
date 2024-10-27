# WGUPS Package Delivery System

Welcome to the **WGUPS Package Delivery System**, a Python-based program that simulates package delivery optimization for the Western Governors University Parcel Service (WGUPS). This program uses a combination of data structures and algorithms to optimize delivery routes and ensure all packages are delivered within their deadlines while minimizing total mileage.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
- [Data Files](#data-files)
- [Algorithm Explanation](#algorithm-explanation)
- [Constraints Handling](#constraints-handling)
- [Assumptions](#assumptions)

---

## Project Overview

The WGUPS Package Delivery System is designed to:

- Load and manage package data from a CSV file.
- Calculate optimal delivery routes using the Nearest Neighbor Algorithm.
- Handle special delivery constraints (e.g., delayed packages, address corrections, package groupings).
- Provide a user interface to check the status of packages at any given time.
- Ensure all packages are delivered within their specified deadlines.
- Keep the total mileage under 140 miles, as per project requirements.

---

## Features

- **Hash Table Implementation**: Custom hash table for efficient package storage and retrieval.
- **Truck Simulation**: Simulates multiple trucks with capacity and speed constraints.
- **Distance Calculation**: Computes distances between addresses using provided distance data.
- **Delivery Optimization**: Implements the Nearest Neighbor Algorithm for route optimization.
- **Constraint Management**: Handles special notes and constraints associated with packages.
- **Dynamic Time Simulation**: Updates package statuses based on simulated time progression.
- **User Interface**: Interactive menu for querying package statuses and total mileage.

---

## Installation

### Prerequisites

- **Python 3.6 or higher** installed on your system.
- Basic understanding of running Python scripts from the command line.

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/WGUPS_Package_Delivery_System.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd WGUPS_Package_Delivery_System
   ```

3. **Ensure the Directory Structure**:

   The project should have the following files and directories:

   ```
   - main.py
   - truck.py
   - package.py
   - hash_table.py
   - distance.py
   - CSV/
     - packages.csv
     - distances.csv
     - addresses.csv
   - README.md
   ```

---

## Usage

1. **Run the Program**:

   ```bash
   python main.py
   ```

2. **Follow On-Screen Instructions**:

   After the simulation completes, you'll be presented with a menu:

   ```
   WGUPS Package Delivery System
   1. View status of all packages at a given time
   2. View status of a single package at a given time
   3. View total mileage
   4. Exit
   Please select an option:
   ```

3. **Select an Option**:

   - **Option 1**: Enter a time (e.g., `10:30 AM`) to view the status of all packages at that time.
   - **Option 2**: Enter a package ID and time to view the status of a specific package.
   - **Option 3**: View the total mileage accumulated by all trucks.
   - **Option 4**: Exit the program.

---

## Modules

### 1. `main.py`

The main driver of the program, responsible for:

- Loading package and distance data.
- Initializing trucks and starting the simulation loop.
- Handling the user interface.

### 2. `package.py`

Defines the `Package` class, which includes:

- Package attributes like ID, address, deadline, weight, notes, status, etc.
- Methods to represent package information.

### 3. `hash_table.py`

Custom hash table implementation using chaining for collision resolution:

- Efficiently stores and retrieves packages based on their IDs.
- Methods include `insert`, `lookup`, and `update_status`.

### 4. `truck.py`

Defines the `Truck` class, simulating delivery trucks:

- Manages package loading, delivery, and route optimization.
- Attributes include capacity, speed, current location, mileage, etc.
- Implements the Nearest Neighbor Algorithm for deliveries.

### 5. `distance.py`

Handles distance calculations between addresses:

- Loads addresses and distance data from CSV files.
- Provides a method `get_distance` to retrieve distances between two locations.

---

## Data Files

All CSV files are located in the `CSV` directory.

### 1. `packages.csv`

Contains package data with the following columns:

- Package ID
- Address
- City
- State
- Zip
- Delivery Deadline
- Weight
- Notes

### 2. `distances.csv`

Contains a distance matrix representing the distances between different locations.

### 3. `addresses.csv`

Lists all the addresses corresponding to the indices used in the distance matrix.

---

## Algorithm Explanation

### Nearest Neighbor Algorithm

The Nearest Neighbor Algorithm is used to determine the delivery route for each truck:

1. **Start at the Hub**:

   - The truck begins its journey from the hub located at `4001 South 700 East`.

2. **Select the Next Destination**:

   - From the current location, select the closest package destination that hasn't been delivered yet.

3. **Deliver the Package**:

   - Move to the selected address, update the truck's current location, time, and mileage.

4. **Repeat**:

   - Continue selecting the nearest unvisited package destination until all packages on the truck are delivered.

5. **Return to the Hub**:

   - After all deliveries, the truck returns to the hub, updating the total mileage and time.

---

## Constraints Handling

The program accounts for various delivery constraints:

1. **Delayed Packages**:

   - Packages with notes indicating a delay are not loaded onto a truck until after their arrival time.

2. **Wrong Address Corrections**:

   - Package 9 has a wrong address that is corrected at 10:20 AM. It cannot be loaded onto a truck before the address is updated.

3. **Package Groupings**:

   - Some packages must be delivered together (e.g., "Must be delivered with 13, 15").
   - The program ensures that grouped packages are loaded onto the same truck and delivered together.

4. **Truck-Specific Packages**:

   - Certain packages can only be loaded onto specific trucks (e.g., "Can only be on truck 2").
   - The assignment logic respects these constraints.

---

## Assumptions

- **Uniform Speed**:

  - Trucks travel at a constant average speed of 18 mph.

- **Simultaneous Departures**:

  - Trucks can depart at the same time, provided they have packages to deliver.

- **Infinite Fuel**:

  - Trucks do not need to refuel; fuel constraints are not considered.

- **No Traffic Delays**:

  - The simulation does not account for traffic conditions or delays other than those specified in package notes.
