import requests
from geopy.geocoders import Nominatim

# Get your public IP address
response = requests.get('https://api64.ipify.org?format=json')
ip_address = response.json()['ip']

# Get your location details from IP address
geolocator = Nominatim(user_agent='location_tracker')
location = geolocator.geocode(ip_address)

# Extract latitude and longitude from location details
latitude = location.latitude
longitude = location.longitude

# Print your location details
print('Your IP address:', ip_address)
print('Your Latitude:', latitude)
print('Your Longitude:', longitude)
