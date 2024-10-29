# Parcel_Service_Routing_Program

Welcome to the **Parcel Service Routing Program**, a Python-based project designed to optimize delivery routes. This program ensures that packages are delivered efficiently and within deadlines, using algorithms and data structures tailored for effective delivery management.

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

The Parcel Service Routing Program provides a way to:
- Load and manage package data from CSV files.
- Optimize delivery routes using the Nearest Neighbor Algorithm.
- Handle special delivery constraints such as delayed packages and address corrections.
- Simulate dynamic delivery progress with a time-based system.
- Provide an interactive user interface to check package statuses and track delivery mileage.
- Ensure the total mileage stays under a set limit (140 miles).

---

## Features

- **Custom Hash Table**: Efficient package storage and lookup.
- **Multi-Truck Delivery Simulation**: Simulates trucks with specific capacities and speeds.
- **Distance Management**: Uses distance data to calculate optimal delivery routes.
- **Dynamic Time Simulation**: Updates package statuses based on time progression.
- **Constraint Management**: Manages special requirements for package delivery.
- **User Interface**: Offers an interactive menu to track deliveries and mileage.

---

## Installation

### Prerequisites
- Python 3.6 or higher.

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/Parcel_Service_Routing_Program.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd Parcel_Service_Routing_Program
   ```
3. **Ensure Directory Structure**:
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
2. **Interactive Menu**:
   ```
   Parcel Service Routing Program
   1. View status of all packages at a given time
   2. View status of a specific package
   3. View total mileage
   4. Exit
   ```

---

## Modules

- **`main.py`**: Main driver handling data loading and the user interface.
- **`package.py`**: Defines the `Package` class with attributes and methods.
- **`hash_table.py`**: Custom hash table implementation for package management.
- **`truck.py`**: Simulates truck behavior with route optimization.
- **`distance.py`**: Manages distances between locations.

---

## Data Files

- **`packages.csv`**: Contains package details.
- **`distances.csv`**: Provides distance data between delivery locations.
- **`addresses.csv`**: Lists all delivery addresses.

---

## Algorithm Explanation

The **Nearest Neighbor Algorithm** selects the closest unvisited location for each delivery, ensuring efficient routing and prompt deliveries.

---

## Constraints Handling

- **Delayed Packages**: Not loaded until their arrival.
- **Address Corrections**: Updates made mid-simulation.
- **Grouped Packages**: Delivered together based on constraints.
- **Truck-Specific Packages**: Loaded only on designated trucks.

---

## Assumptions

- Trucks travel at 18 mph.
- Simultaneous truck departures are allowed.
- No refueling or traffic delays are considered.
