import requests
from datetime import datetime, timezone
import smtplib
import time
import os

MY_LAT = 0.00
MY_LONG = 0.00


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now(timezone.utc)
    current_hour = time_now.hour

    if current_hour >= sunset or current_hour <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        my_email = os.environ.get("FROM_ADR")
        pwd = os.environ.get("MAIL_PWD")
        to_email = os.environ.get("TO_ADR")
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=pwd)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=to_email,
                msg="Subject:ISS Overhead\n\nLook Up! ISS Overhead."
            )
