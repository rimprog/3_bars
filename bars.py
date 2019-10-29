import json
from math import radians, sin, cos, asin, sqrt


def load_data(filepath):
    with open(filepath, 'r') as file_handler:
        return json.load(file_handler)


def get_biggest_bar(data):

    biggest_bar = max(data, key=lambda x: x['properties']['Attributes']['SeatsCount'])

    return biggest_bar


def get_smallest_bar(data):

    smallest_bar = min(data, key=lambda x: x['properties']['Attributes']['SeatsCount'])

    return smallest_bar


def get_closest_bar(data, longitude, latitude):
    def haversine(bar):
        bar_longitude, bar_latitude = bar['geometry']['coordinates']
        lon1, lat1, lon2, lat2 = map(radians, [float(longitude), float(latitude), bar_longitude, bar_latitude])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2) ** 2
        c = 2 * asin(sqrt(a))
        earth_radius = 6371

        return c * earth_radius

    closest_bar = min(data, key=lambda x: haversine(x))

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
