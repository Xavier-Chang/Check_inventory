import os
import requests
from bs4 import BeautifulSoup
import smtplib
import time

# Load environment variables for configuration
PRODUCT_URL = os.getenv('PRODUCT_URL')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

# Check the stock status function
def check_stock():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(PRODUCT_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Check for availability text
        if "Add to basket" in soup.text:
            send_email("商品有存貨！")
        elif "Notify me when available" in soup.text:
            print("商品無存貨")
        else:
            print("無法判斷商品庫存狀態")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch product page: {e}")

# Function to send email notifications
def send_email(message):
    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # Construct the email
        subject = 'Loewe商品通知'
        body = f'{message}\n鏈接：{PRODUCT_URL}'
        msg = f'Subject: {subject}\n\n{body}'

        # Send the email
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg)
        print("通知已發送")

        # Close the SMTP server
        server.quit()
    except Exception as e:
        print(f"發送郵件失敗: {e}")

# Main program to check stock every 5 minutes
while True:
    check_stock()
    time.sleep(300)  # Check every 5 minutes
