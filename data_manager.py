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
        self.user_data = None

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

    def get_customer_emails(self):
        sheety_user_endpoint = os.environ["SHEETY_USER_ENDPOINT"]
        user_token = os.environ["USER_TOKEN"]
        authorization_user_header = {

            "Authorization": f"Bearer {user_token}",
            "Content-Type": "application/json"

        }
        # Get user data from the user's sheet
        response = requests.get(url=sheety_user_endpoint, headers=authorization_user_header)
        self.user_data = response.json()
        return self.user_data
