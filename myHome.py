import requests
from bs4 import BeautifulSoup
import json
import os
import time
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

new_listings_found = False

DCU_coordinates = (53.38569455370613, -6.258966096623697)
UCD_coordinates = (53.30982292759559, -6.221074718690762)

geolocator = Nominatim(user_agent="rentAlertProgram")

DATA_FILE = "data.json"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        known_listings = json.load(f)
else:
    known_listings = []

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(known_listings, f, indent=4)


TOKEN = "8193236905:AAF5zcPUMeB4FF7XA5Mdv_0-5KuejiPjUEw"
CHAT_ID = "8339401080"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)


def process_listing(listing):
    try:
        title = listing.find("h2", {"class": "card-title"}).text.strip()
        address = listing.find("h3", {"class": "card-text"}).text.strip()
        link = "https://www.myhome.ie" + listing.find("a")["href"]
    except:
        return

    if any(item["link"] == link for item in known_listings):
        return

    record = {
        "title": title,
        "link": link
    }

    known_listings.append(record)
    save_data()

    global new_listings_found
    new_listings_found = True

    location = geolocator.geocode(address)

    if location != None:
        distance_to_DCU = str(round(geodesic(DCU_coordinates, (location.latitude, location.longitude)).km, 2)) + 'km'
        distance_to_UCD = str(round(geodesic(UCD_coordinates, (location.latitude, location.longitude)).km, 2)) + 'km'
    else:
        distance_to_DCU = 'Failed to calculate distance to DCU'
        distance_to_UCD = 'Failed to calculate distance to UCD'

    message = f"New listing found:\n{title}\nDistance to DCU: {distance_to_DCU}\nDistance to UCD: {distance_to_UCD}\n{address}\n{link}"
    send_telegram(message)
    print("Sent Telegram:", title)


def scrape():
    page = 1
    while True:
        url = f"https://www.myhome.ie/rentals/dublin/property-to-rent?page={page}&maxprice=2200&minbeds=2&maxbeds=2"
        print("Scraping:", url)

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        listings = soup.find_all("div", {"class": "card-body"})

        if not listings:
            print("No more pages.")
            break

        for listing in listings:
            process_listing(listing)

        page += 1
        time.sleep(1)


scrape()

if not new_listings_found:
    send_telegram("Program ran successfully, but no new listings were found.")

