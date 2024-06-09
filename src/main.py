import requests
import logging
from flask import Flask
import json
import snake_status

# Enable debugging output for requests
logging.basicConfig(level=logging.DEBUG)

# Define the Unifi controller IP address
unifi_controller_ip = "192.168.100.1"

# Define your credentials
username = "api2"
password = "HarfordSound69"

# Define the URL for logging in
login_url = f"https://{unifi_controller_ip}/api/auth/login"

# Define the URL for getting device status
device_status_url = f"https://{unifi_controller_ip}/proxy/network/api/s/default/stat/device/"

# Create a session object
session = requests.Session()

# Disable SSL certificate verification
session.verify = False

# Initialize Flask application
app = Flask(__name__)

def login():
    # Login to the Unifi controller
    login_data = {
        "username": username,
        "password": password
    }

    response = session.post(login_url, json=login_data)
    # Check if login was successful
    if response.status_code != 200:
        print("Login failed!")
        print(response.json())
        return False
    else:
        print("Login successful!")
        return True
    
def getSnakeStatus():
    # Get device status
    device_status_response = session.get(device_status_url)

    # Check if getting device status was successful
    if device_status_response.status_code != 200:
        # print("Failed to get device status!")
        return False, {"Error":f"Unifi API returned {device_status_response.status_code} status code"}

    # get snake status
    snake_status_class = snake_status.snake_status()
    device_status = device_status_response.json()["data"]
    snake_status_result = snake_status_class.run(device_status)
    return True, snake_status_result

@app.route('/metrics', methods=['GET'])
def metrics():
    ss_success, ss_result = getSnakeStatus()
    return json.dumps(ss_result)

if __name__ == "__main__":
    # login to Unifi API
    if not login():
        exit()

    # Start Flask application
    app.run(host='0.0.0.0', port=5000)