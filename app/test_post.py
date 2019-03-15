import requests
import json

info = {"trip_info":[{"city_id":"2","ISO_date":"2019-01-10T08:55:34.160Z"},{"city_id":"22","ISO_date":"2019-04-14T07:55:34.160Z"}]}
response = requests.post('http://127.0.0.1:5000/route_info', data = json.dumps(info))
print(response.text)