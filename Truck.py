class Truck:
    """
    Represents a delivery truck.

    Attributes:
        capacity (int): The capacity of the truck.
        speed (float): The speed of the truck.
        load (list): The current load of the truck.
        packages (list): The package IDs the truck is responsible for.
        mileage (float): Total mileage covered by the truck.
        address (str): Current address of the truck.
        depart_time (datetime.timedelta): Departure time of the truck.
    """
    def __init__(self, capacity, speed, load, packages, mileage, address, depart_time):
        self.capacity = capacity
        self.speed = speed
        self.load = load
        self.packages = packages
        self.mileage = mileage
        self.address = address
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self):
        formatted_packages = ', '.join(map(str, self.packages))
        return (f"Capacity: {self.capacity}, Speed: {self.speed}, Load: {self.load}, "
                f"Packages: [{formatted_packages}], Mileage: {self.mileage}, "
                f"Address: {self.address}, Departure Time: {self.depart_time}")