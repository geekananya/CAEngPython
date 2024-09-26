class Ride:
    def __init__(self, name, age_limit, height_limit, price):
        self.name = name
        self.age_limit = age_limit
        self.height_limit = height_limit
        self.price = price

    def __repr__(self):
        return f"Ride(name='{self.name}', age_limit={self.age_limit}, height_limit={self.height_limit}, price={self.price})"

    # def __str__(self):
    #     return f"Ride(name='{self.name}', age_limit={self.age_limit}, height_limit={self.height_limit}, price={self.price})"


# class to handle add/remove ops on ride
class Rides:
    def __init__(self):
        self.rides_list = []        # compositely stores Ride instances

    def initialize_rides(self, data):
        for ride_data in data:
            self.add_ride(
                ride_data["name"],
                ride_data["age_limit"],
                ride_data["height_limit"],
                ride_data["price"]
            )

    def add_ride(self, name, age_limit, height_limit, price):
        new_ride = Ride(name, age_limit, height_limit, price)
        self.rides_list.append(new_ride)


    def remove_ride(self, name):
        for ride in self.rides_list:
            if ride.name == name:
                self.rides_list.remove(ride)
                return self.get_rides()
        raise Exception("Ride not found.")


    def update_ride(self, name, **ride_info):
        for ride in self.rides_list:
            if ride.name == name:
                if ride_info.get('age_limit') is not None:
                    ride.age_limit = ride_info.get('age_limit')
                if ride_info.get('height_limit') is not None:
                    ride.height_limit = ride_info.get('height_limit')
                if ride_info.get('price') is not None:
                    ride.price = ride_info.get('price')
                return self.get_rides()
        raise Exception("Ride not found.")


    def get_rides(self):
        if not self.rides_list:
            return []
        return self.rides_list


credentials = [
    {"username": "admin", "password": "adminpass"},
    {"username": "user1", "password": "userpass1"},
    {"username": "user2", "password": "userpass2"},
]

rides_data = [
    {"name": "Roller Coaster", "age_limit": 12, "height_limit": 140, "price": 10},
    {"name": "Ferris Wheel", "age_limit": 0, "height_limit": 0, "price": 5},
    {"name": "Bumper Cars", "age_limit": 8, "height_limit": 120, "price": 7},
    {"name": "Haunted House", "age_limit": 10, "height_limit": 0, "price": 8},
    {"name": "Merry-Go-Round", "age_limit": 0, "height_limit": 0, "price": 4},
    {"name": "Water Slide", "age_limit": 5, "height_limit": 100, "price": 6},
    {"name": "Log Flume", "age_limit": 6, "height_limit": 110, "price": 7},
    {"name": "Swing Ride", "age_limit": 0, "height_limit": 0, "price": 5},
    {"name": "Drop Tower", "age_limit": 12, "height_limit": 130, "price": 9},
    {"name": "Go-Karts", "age_limit": 10, "height_limit": 130, "price": 15},
]