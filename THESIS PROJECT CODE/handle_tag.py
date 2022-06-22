import haversine as hs

from database import handledb
from gps import gps
from sms import send_message


class Passenger():
    def __init__(self, tag_id):
        self.tag_id = tag_id
        self.destination_latitude = 0
        self.destination_longitude = 0
        self.starting_latitude = 0
        self.starting_longitude = 0

    def calculate_distance(self):
        starting_point = (self.starting_latitude,
                          self.starting_longitude)
        destination_point = (self.destination_latitude + 10,
                             self.destination_longitude + 10)

        distance = hs.haversine(starting_point, destination_point)
        return distance


tag_list = []
users = {}


def handle_tag(tag_id):
    global tag_list
    global users
    if tag_id in tag_list:  # destination point
        print('arrived')  # delete this line
        user = users[f'tag_id']
        user.destination_latitude, user.destination_longitude = (
            10.2345, 15.900)  # gps()
        distance = user.calculate_distance()
        handledb(tag_id, distance)
        tag_list.remove(tag_id)
        users.pop(f'tag_id')
        del user
        send_message()

    else:  # starting point
        print('started')  # delete this line
        tag_list = tag_list + [tag_id]
        user = Passenger(tag_id)
        user.starting_latitude, user.starting_longitude = (1, 2)  # gps()
        users[f'tag_id'] = user

    return tag_list
