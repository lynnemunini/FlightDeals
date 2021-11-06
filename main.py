from datetime import datetime, timedelta
from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager
notification_manager = NotificationManager()
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
ORIGIN_CITY_IATA = "NBO"
if sheet_data[0]["iataCode"] == "":
    from flight_search import FlightSearch
    for row in sheet_data:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    print(f"sheet_data:\n {sheet_data}")

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()
tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

for destination in sheet_data:
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    if flight is not None and flight.price < destination["lowestPrice"]:
        message = f"Low price alert! Only Ksh {flight.price} to fly from " \
                  f"{flight.origin_city}-{flight.origin_airport} to " \
                  f"{flight.destination_city}-{flight.destination_airport}, from {flight.out_date} " \
                  f"to {flight.return_date}."
        if flight.stop_overs > 0:
            message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."
            print(message)

        notification_manager.send_sms(message)
