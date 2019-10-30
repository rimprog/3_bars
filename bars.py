import json
from math import radians, sin, cos, asin, sqrt


def load_data(filepath):
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def get_biggest_bar(bars):

    biggest_bar = max(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])

    return biggest_bar


def get_smallest_bar(bars):

    smallest_bar = min(bars, key=lambda bar: bar['properties']['Attributes']['SeatsCount'])

    return smallest_bar


def get_closest_bar(bars, longitude, latitude):
    def haversine(bar):
        earth_radius = 6371
        bar_longitude, bar_latitude = bar['geometry']['coordinates']
        longitude_1, latitude_1, longitude_2, latitude_2 = map(radians, [float(longitude), float(latitude), bar_longitude, bar_latitude])
        dlon = longitude_2 - longitude_1
        dlat = latitude_2 - latitude_1
        arcsin = asin(sqrt(sin(dlat/2)**2 + cos(latitude_1) * cos(latitude_2) * sin(dlon/2) ** 2))
        distanse = 2 * earth_radius * arcsin

        return distanse

    closest_bar = min(bars, key=lambda bar: haversine(bar))

    return closest_bar


if __name__ == '__main__':
    data = load_data('moscow_bars.json')

    bars = []
    for bar in data['features']:
        bars.append(bar)

    biggest_bar = get_biggest_bar(bars)
    biggest_bar_name = biggest_bar['properties']['Attributes']['Name']
    biggest_bar_address = biggest_bar['properties']['Attributes']['Address']
    print('Самый большой бар Москвы: {}.\nАдрес: {}\n'.format(biggest_bar_name, biggest_bar_address))

    smallest_bar = get_smallest_bar(bars)
    smallest_bar_name = smallest_bar['properties']['Attributes']['Name']
    smallest_bar_address = smallest_bar['properties']['Attributes']['Address']
    print('Самый маленький бар Москвы: {}.\nАдрес: {}\n'.format(smallest_bar_name, smallest_bar_address))

    current_latitude, current_longitude = input('Ведите ваши координаты в формате "latitude, longitude":\n').split(', ')
    closest_bar = get_closest_bar(bars, current_longitude, current_latitude)
    closest_bar_name = closest_bar['properties']['Attributes']['Name']
    closest_bar_address = closest_bar['properties']['Attributes']['Address']
    print('Самый ближайший бар к указанным вами координатам: {}.\nАдрес: {}\n'.format(closest_bar_name, closest_bar_address))
