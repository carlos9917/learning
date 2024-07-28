import requests

def get_weather_stations(latitude, longitude):
    url = 'https://api.open-meteo.com/v1/stations'
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'radius': 50,  # Radius in kilometers to search for stations
        'limit': 10    # Limit the number of stations returned
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        stations = response.json().get('stations', [])
        return stations
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None



def get_weather_locations(query):
    url = 'https://api.metaweather.com/api/location/search/'
    params = {
        'query': query
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        locations = response.json()
        return locations
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Example usage
query = 'Berlin'  # Name of the city or location

# Example usage
query = 'Berlin'  # Name of the city or location

locations = get_weather_locations(query)
if locations:
    for location in locations:
        print(f"Location: {location['title']}, WOEID: {location['woeid']}")

#if locations:
#    for location in locations:
#        print(f"Location: {location['title']}, WOEID: {location['woeid']}")
#

# Example usage
latitude = 52.52  # Latitude for Berlin
longitude = 13.405  # Longitude for Berlin

#stations = get_weather_stations(latitude, longitude)
#if stations:
#    for station in stations:
#        print(f"Station ID: {station['id']}, Name: {station['name']}, Distance: {station['distance']} km")
#
