import requests
import logging
from flask import Flask, Response
import json
import snake_status

# Enable debugging output for requests
logging.basicConfig(level=logging.DEBUG)

# Define the Unifi controller IP address
unifi_controller_ip = "unifi"

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
    # Unauthorized
    if device_status_response.status_code == 401:
        print("Logged out of Unifi API. Attempting to login...")
        if not login():
            exit()
        else:
            return getSnakeStatus()
    if device_status_response.status_code != 200:
        print("Failed to get device status!")
        print(f"ERROR: Unifi API returned {device_status_response.status_code} status code")
        return False, {"Error":f"Unifi API returned {device_status_response.status_code} status code"}

    # get snake status
    snake_status_class = snake_status.snake_status()
    device_status = device_status_response.json()["data"]
    snake_status_result = snake_status_class.run(device_status)
    return True, snake_status_result

@app.route('/metrics', methods=['GET'])
def metrics():
    return_text = ""

    #snake status
    return_text += "# HELP uniprom_snake_status Status of the trunked snake connection between switches\n"
    return_text += "# TYPE uniprom_snake_status gauge\n"
    ss_success, ss_result = getSnakeStatus()
    if ss_success:
        for media_type, media_type_v in ss_result.items():
            for port_rank, port_rank_v in media_type_v.items():
                return_text += f"uniprom_snake_status{{media_type=\"{media_type}\", port_rank=\"{port_rank}\"}} {port_rank_v}\n"

    return Response(return_text, content_type="text/plain; version=0.0.4; charset=utf-8; escaping=values")

if __name__ == "__main__":
    # login to Unifi API
    if not login():
        exit()

    # Start Flask application
    app.run(host='0.0.0.0', port=9430)