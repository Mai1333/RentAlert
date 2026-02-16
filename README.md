# Dublin Rental Alert Bot

**An automated Python tool that monitors MyHome.ie for rental listings matching student budget criteria and sends instant alerts via Telegram.**

**Screenshot of sample telegram messages**
<img width="1164" height="905" alt="image" src="https://github.com/user-attachments/assets/ca757dce-cf17-4b94-a468-461e1e121b2c" />

## Overview
Finding student accommodation in Dublin is difficult due to high demand and rapid turnover. This bot automates the search process by scraping new listings every hour, filtering for specific criteria, and calculating commute distances to university campuses (DCU & UCD).

## Key Features
* **Real-Time Scraping:** Parses raw HTML from `myhome.ie` using **BeautifulSoup**.
* **Smart Filtering:** Automatically filters for:
    * Price: < €2,200/month
    * Size: Minimum 2 Bedrooms
    * Location: Dublin region
* **Commute Calculator:** Uses geospatial logic to estimate the distance between the property and **DCU/UCD campuses**.
* **Instant Notifications:** Integrates with the **Telegram Bot API** to push alerts directly to mobile.
* **CI/CD Automation:** Runs on a scheduled CRON job (every hour) using **GitHub Actions**, ensuring zero downtime without needing a local server.

## Tech Stack
* **Language:** Python 3.10+
* **Web Scraping:** BeautifulSoup4, Requests
* **APIs:** Telegram Bot API
* **DevOps:** GitHub Actions (YAML workflows)
* **Environment Management:** Python-dotenv

## How It Works
1.  The script runs automatically via a **GitHub Actions workflow** (`.github/workflows/main.yml`).
2.  It uses BeautifulSoup to get listings from myhome.ie
3.  It loops through listings, extracting price, beds, and location data.
4.  If a listing matches the criteria and hasn't been seen before, it formats a message.
5.  The message is sent to a private Telegram channel.

## Local Installation
If you want to run this locally:

1. **Clone the repository**
   ```bash
   git clone [https://github.com/Mai1333/RentAlert.git](https://github.com/Mai1333/RentAlert.git)
   cd RentAlert

2. **Install dependencies**
pip install -r requirements.txt

3. **Configure Environment Variables**
Create a .env file and add your Telegram credentials
TELEGRAM_TOKEN=your_token_here
CHAT_ID=your_chat_id_here

4. **Run the script**
python main.py



