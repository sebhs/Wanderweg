import requests
import json
googleAPIKey = 'AIzaSyBw0StR76cWn1lE3laP23Tr9zig47bC-K8'

# Function to add coordinate infor for each city to the map
def addCoordData(cityMap):
    for key in cityMap:
        city = key.replace(' ', '+')
        url = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + city + ',+'
        url += cityMap[key][0] + '&key=' + googleAPIKey
        response = requests.get(url)
        data = response.json()
        cityMap[key].append(data['results'][0]['geometry']['location']['lat'])
        cityMap[key].append(data['results'][0]['geometry']['location']['lng'])