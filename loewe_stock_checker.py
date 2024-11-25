import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os
from flask import Flask

# Flask setup to keep a port open
app = Flask(__name__)

# Environment Variables Setup
PRODUCT_URL = os.getenv('PRODUCT_URL')
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')

# Check stock function
def check_stock():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(PRODUCT_URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Print the whole HTML content for debugging
    print(soup.prettify())

    if "Add to basket" in soup.text:
        print("Product is in stock!")  # Add print statement to verify
        send_email("商品有存貨！")
    elif "Notify me when available" in soup.text:
        print("商品無存貨")  # Add print statement to verify
    else:
        print("無法判斷商品庫存狀態")

# Send email function
def send_email(message):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        subject = 'Loewe商品通知'
        body = f'{message}\n鏈接：{PRODUCT_URL}'
        msg = f'Subject: {subject}\n\n{body}'
        
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg)
        print("通知已發送")
        server.quit()
    except Exception as e:
        print(f"發送郵件失敗: {e}")


# Main loop to check stock every 5 minutes
@app.route('/')
def index():
    return "Service is running!"

if __name__ == '__main__':
    # Start the Flask app to keep the port open
    from threading import Thread

    # Run the stock checker in a separate thread
    def stock_checker():
        while True:
            check_stock()
            time.sleep(300)

    # Start the Flask server
    Thread(target=stock_checker).start()
    app.run(host='0.0.0.0', port=10000)
