import json
from math import radians, sin, cos, asin, sqrt


def load_data(filepath):
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def get_seats_count(bar):
    return bar['properties']['Attributes']['SeatsCount']


def get_biggest_bar(bars):

    biggest_bar = max(bars, key=lambda bar: get_seats_count(bar))

    return biggest_bar


def get_smallest_bar(bars):

    smallest_bar = min(bars, key=lambda bar: get_seats_count(bar))

    return smallest_bar


def get_bar_coordinates(bar):
    bar_longitude, bar_latitude = bar['geometry']['coordinates']

    return [bar_longitude, bar_latitude]


def find_haversine(longitude_start, latitude_start, longitude_end, latitude_end):
    earth_radius = 6371
    longitude_start_in_radians = radians(float(longitude_start))
    longitude_end_in_radians = radians(float(longitude_end))
    latitude_start_in_radians = radians(float(latitude_start))
    latitude_end_in_radians = radians(float(latitude_end))

    longitude_distance = longitude_end_in_radians - longitude_start_in_radians
    latitude_distance = latitude_end_in_radians - latitude_start_in_radians

    arcsin = asin(sqrt(sin(latitude_distance/2)**2 +
                       cos(latitude_start_in_radians) *
                       cos(latitude_end_in_radians) *
                       sin(longitude_distance/2) ** 2))

    distance = 2 * earth_radius * arcsin

    return distance


def get_closest_bar(bars, user_longitude, user_latitude):

    closest_bar = min(bars,
                      key=lambda bar: find_haversine(user_longitude,
                                                     user_latitude,
                                                     get_bar_coordinates(bar)[0],
                                                     get_bar_coordinates(bar)[1]))

    return closest_bar


if __name__ == '__main__':
    data = load_data('moscow_bars.json')

    bars = []
    for bar in data['features']:
        bars.append(bar)

    biggest_bar = get_biggest_bar(bars)
    biggest_bar_name = biggest_bar['properties']['Attributes']['Name']
    biggest_bar_address = biggest_bar['properties']['Attributes']['Address']
    biggest_bar_text_template = 'Biggest Moscow bar: {}.\nAddress: {}\n'
    print(biggest_bar_text_template.format(biggest_bar_name,
                                           biggest_bar_address))

    smallest_bar = get_smallest_bar(bars)
    smallest_bar_name = smallest_bar['properties']['Attributes']['Name']
    smallest_bar_address = smallest_bar['properties']['Attributes']['Address']
    smallest_bar_text_template = 'Smallest Moscow Bar: {}.\nAddress: {}\n'
    print(smallest_bar_text_template.format(smallest_bar_name,
                                            smallest_bar_address))

    coordinate_text_template = 'Input coordinates: latitude, longitude\n'
    user_latitude, user_longitude = input(coordinate_text_template).split(', ')
    closest_bar = get_closest_bar(bars, user_longitude, user_latitude)
    closest_bar_name = closest_bar['properties']['Attributes']['Name']
    closest_bar_address = closest_bar['properties']['Attributes']['Address']
    closest_bar_text_template = 'Closest bar: {}.\nAddress: {}\n'
    print(closest_bar_text_template.format(closest_bar_name,
                                           closest_bar_address))
