import requests
from bs4 import BeautifulSoup
import json
import os
import time


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
        link = "https://www.myhome.ie" + listing.find("a")["href"]
    except:
        return

    if any(item["link"] == link for item in known_listings):
        return  # already seen

    record = {
        "title": title,
        "link": link
    }

    known_listings.append(record)
    save_data()

    message = f"New listing found:\n{title}\n{link}"
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
