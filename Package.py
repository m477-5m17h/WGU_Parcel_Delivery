class Package:
    """
    Represents a delivery package.

    Attributes:
        ID (int): The ID of the package.
        address (str): Delivery address of the package.
        city (str): Delivery city.
        state (str): Delivery state.
        zipcode (str): Delivery zipcode.
        deadline_time (str): Delivery deadline time.
        weight (float): Weight of the package.
        status (str): Current status of the package.
        departure_time (datetime.timedelta): Time when the package departs.
        delivery_time (datetime.timedelta): Time when the package is delivered.
    """

    def __init__(self, ID, address, city, state, zipcode, deadline_time, weight, status):
        """
        When a new package like me is created, this is where all my details get set up.
        It's like my birth certificate, but for packages.
        """
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline_time = deadline_time
        self.weight = weight
        self.status = status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        """
        Want to know all about me in a quick glance? Call this, and I'll tell you my story in a sentence!
        """
        return (f"ID: {self.ID}, Address: {self.address}, City: {self.city}, State: {self.state}, "
                f"Zipcode: {self.zipcode}, Deadline: {self.deadline_time}, Weight: {self.weight}, "
                f"Delivery Time: {self.delivery_time}, Status: {self.status}")

    def update_status(self, current_time):
        """
        Time for a status update! Let's see where I am on my journey based on the current time.
        Am I still waiting to go, on my way, or have I already made someone's day?
        """
        if self.delivery_time and current_time >= self.delivery_time:
            self.status = "Delivered"
        elif self.departure_time and self.departure_time <= current_time < self.delivery_time:
            self.status = "En route"
        else:
            self.status = "At Hub"

