import requests
import os
from pprint import pprint
from flight_data import FlightData
FLIGHT_APIKEY = os.environ["FLIGHT_APIKEY"]
FLIGHT_ENDPOINT = os.environ["FLIGHT_ENDPOINT"]
location_endpoint = f"{FLIGHT_ENDPOINT}/locations/query"


class FlightSearch:
    # This class is responsible for talking to the Flight Search API

    def get_destination_code(self, city_name):
        query = {"term": city_name, "location_types": "city"}
        headers = {"apikey": FLIGHT_APIKEY}
        response = requests.get(url=location_endpoint, headers=headers, params=query)
        results = response.json()["locations"]
        code = results[0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"apikey": FLIGHT_APIKEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "KES"
        }

        response = requests.get(
            url=f"{FLIGHT_ENDPOINT}/v2/search",
            headers=headers,
            params=query,
        )

        try:
            data = response.json()["data"][0]
        except IndexError:
            try:
                data = response.json()["data"][0]
            except IndexError:
                return None
            else:
                query["max_stopovers"] = 1
                response = requests.get(
                    url=f"{FLIGHT_ENDPOINT}/v2/search",
                    headers=headers,
                    params=query,
                )
                data = response.json()["data"][0]
                # pprint(data)
                flight_data = FlightData(
                    price=data["price"],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
                return flight_data
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0]
            )
            # print(f"{flight_data.destination_city}: KSh {flight_data.price}")
            return flight_data


