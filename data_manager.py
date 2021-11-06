import requests
from pprint import pprint
import os
token = os.environ["TOKEN"]
SHEETY_FLIGHT_ENDPOINT = os.environ["SHEETY_FLIGHT_ENDPOINT"]
authorization_header = {

    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"

}
class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_FLIGHT_ENDPOINT, headers=authorization_header)
        data = response.json()
        self.destination_data = data["prices"]
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_FLIGHT_ENDPOINT}/{city['id']}",
                json=new_data, headers=authorization_header
            )
            print(response.text)
