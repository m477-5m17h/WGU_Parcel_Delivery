"""
WGU Parcel Service Program
This script manages the delivery of packages using trucks and provides a CLI interface for package status.
Author: Matthew Smith
ID: 001458396
"""

import csv
import datetime
from Truck import Truck
from HashMap import CreateHashMap
from Package import Package

# CSV data handling module
class CSVDataLoader:
    """
    I'm your friendly neighborhood CSVDataLoader.
    I'm here to load all those nifty CSV files you have lying around.
    Think of me as a helpful librarian for your data files.
    """
    def __init__(self):
        self.distanceCSV = self.load_csv("csv/Distances.csv")
        self.addressCSV = self.load_csv("csv/Addresses.csv")
        self.packageCSV = self.load_csv("csv/Packages.csv")

    @staticmethod
    def load_csv(filename):
        """
        Just give me a filename, and I'll turn it into a list of data.
        It's like magic, but with files and data.
        """
        with open(filename, encoding='utf-8-sig') as file:
            return list(csv.reader(file))

dataLoader = CSVDataLoader()

# Package loading function
def load_packages(package_data, hash_table):
    for package in package_data:
        if len(package) >= 7:
            package_obj = Package(*map(str.strip, package[:7]), "At Hub")
            hash_table.insert(int(package_obj.ID), package_obj)
        else:
            print(f"Skipping row {package} - not enough data to create a package.")

# Distance calculation function
def calculate_distance(start_index, end_index, distance_data):
    """
    Calculate the distance between two points.

    Args:
        start_index (int): The index of the starting point in the distance data.
        end_index (int): The index of the ending point in the distance data.
        distance_data (list): A 2D list containing the distances between points.

    Returns:
        float: The distance between the two points. Returns 0 if indices are the same.
               Returns None if the distance data is incomplete or indices are out of range.
    """
    try:
        # Check if the start and end points are the same
        if start_index == end_index:
            return 0.0

        # Extract distance from the 2D list
        distance = distance_data[start_index][end_index]

        # If distance is not found in the specified direction, try the reverse direction
        if distance == '':
            distance = distance_data[end_index][start_index]

        return float(distance)
    except IndexError:
        # Handle cases where the indices are out of the bounds of the distance data
        print(f"Index out of range: start_index={start_index}, end_index={end_index}")
        return None
    except (TypeError, ValueError):
        # Handle cases where the distance data is not in the expected format
        print(f"Invalid distance data at indices: start_index={start_index}, end_index={end_index}")
        return None


# Address lookup function
def find_address_index(address, address_data):
    return next(int(row[0].strip('\ufeff')) for row in address_data if address in row[2])

# Truck initialization
def initialize_trucks():
    start_address = "4001 South 700 East"
    return [
        Truck(16, 18, None, [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40], 0.0, start_address, datetime.timedelta(hours=8)),
        Truck(16, 18, None, [3, 6, 12, 17, 18, 19, 21, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0, start_address, datetime.timedelta(hours=10, minutes=20)),
        Truck(16, 18, None, [2, 4, 5, 6, 7, 8, 9, 10, 11, 25, 28, 32, 33], 0.0, start_address, datetime.timedelta(hours=9, minutes=5))
    ]

# Nearest neighbor delivery algorithm
def deliver_packages(truck, package_hash_table, address_data, distance_data):
    """
    Implements the package delivery algorithm for a given truck.

    This function employs a basic nearest neighbor heuristic to determine the order
    in which packages should be delivered. It iteratively selects the closest package
    to the truck's current location until all packages are delivered. This approach,
    while not guaranteeing an optimal solution, offers a simple and practical method
    for package delivery routing.

       Parameters:
           truck (Truck): The truck object responsible for delivering packages.
           package_hash_table (HashMap): A hash table containing package information.
           address_data (list): A list of address information.
           distance_data (list): A 2D list containing the distances between addresses.

    The function updates the truck's package list, mileage, current address, and
    the delivery and departure time of each package. Packages are removed from the
    'not_delivered' list as they are delivered.

       The algorithm loops through all undelivered packages, calculates the distance
       from the truck's current position to each package's destination, and selects
       the package with the shortest distance for delivery next. This process repeats
       until all packages are delivered. The efficiency of this algorithm is heavily
       dependent on the distribution of package destinations.
       """
    not_delivered = [package_hash_table.lookup(package_id) for package_id in truck.packages]
    truck.packages.clear()

    while not_delivered:
        next_address = float('inf')
        next_package = None

        for package in not_delivered:
            distance = calculate_distance(find_address_index(truck.address, address_data),
                                         find_address_index(package.address, address_data),
                                         distance_data)
            if distance < next_address:
                next_address = distance
                next_package = package

        truck.packages.append(next_package.ID)
        not_delivered.remove(next_package)
        truck.mileage += next_address
        truck.address = next_package.address
        truck.time += datetime.timedelta(hours=next_address / 18)
        next_package.delivery_time = truck.time
        next_package.departure_time = truck.depart_time

# User interaction functions
def get_user_input(prompt):
    return input(prompt).strip()

def get_valid_timedelta(prompt):
    """
    This is to parse the time string and return an object, which for these requirements are purely about capturing hours,
     minutes, and seconds.
    """
    while True:
        user_input = get_user_input(prompt)
        try:
            hours, minutes, seconds = map(int, user_input.split(":"))
            return datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
        except ValueError:
            print("Invalid time format. Please use HH:MM:SS.")

# Main function
def main():
    print("Welcome to the WGU Parcel Service Tracking System")
    print("Loading package and truck information... Please wait.\n")

    trucks = initialize_trucks()
    package_hash_table = CreateHashMap()
    load_packages(dataLoader.packageCSV, package_hash_table)
    for truck in trucks:
        deliver_packages(truck, package_hash_table, dataLoader.addressCSV, dataLoader.distanceCSV)

    total_mileage = sum(truck.mileage for truck in trucks)

    while True:
        print("\nOptions:")
        print("1. View status of a specific package")
        print("2. View status of all packages at a specific time")
        print("3. View total mileage of all trucks")
        print("4. Exit")
        choice = get_user_input("Please choose an option (1-4): ")

        if choice == '1':
            try:
                package_id = int(get_user_input("Enter the package ID: "))
                check_time = get_valid_timedelta("Enter the time to check status (HH:MM:SS): ")
                package = package_hash_table.lookup(package_id)
                package.update_status(check_time)
                print("\nPackage Status:")
                print(package)
            except ValueError:
                print("Invalid input. Please enter a valid package ID and time.")
        elif choice == '2':
            check_time = get_valid_timedelta("Enter the time to check status of all packages (HH:MM:SS): ")
            print("\nStatus of All Packages:")
            for package_id in range(1, 41):
                package = package_hash_table.lookup(package_id)
                package.update_status(check_time)
                print(package)
        elif choice == '3':
            print(f"\nTotal mileage traveled by all trucks: {total_mileage} miles")
        elif choice == '4':
            print("Exiting the system. Thank you!")
            break
        else:
            print("Invalid option. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()
