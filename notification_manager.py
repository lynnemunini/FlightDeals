from twilio.rest import Client
import os
from data_manager import DataManager
import smtplib
data_manager = DataManager()
TWILIO_SID = os.environ["TWILIO_SID"]
TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
TWILIO_NUMBER = os.environ["TWILIO_NUMBER"]
TWILIO_VERIFIED_NUMBER = os.environ["TWILIO_VERIFIED_NUMBER"]
my_email = os.environ["my_email"]
password = os.environ["password"]
user_data = data_manager.get_customer_emails()


class NotificationManager:

    # def __init__(self):
    #     self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    # def send_sms(self, message):
    #     message = self.client.messages.create(
    #         body=message,
    #         from_=TWILIO_NUMBER,
    #         to=TWILIO_VERIFIED_NUMBER,
    #     )
    #     # Prints if successfully sent.
    #     print(message.sid)

    def send_email(self, message, google_flight_link):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            for user in user_data["users"]:
                user_email = user["email"]
                connection.sendmail(from_addr=my_email, to_addrs=f"{user_email}",
                                    msg=f"Subject:New Flight Deals Alert\n\n{message}"
                                        f"{google_flight_link}".encode('utf-8'))
