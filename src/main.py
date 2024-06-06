import requests
import logging

# Enable debugging output for requests
logging.basicConfig(level=logging.DEBUG)

# Define the Unifi controller IP address
unifi_controller_ip = "192.168.100.1"

# Define the URL for logging in
login_url = f"https://{unifi_controller_ip}/api/auth/login"

# Define the URL for getting device status
device_status_url = f"https://{unifi_controller_ip}/proxy/network/api/s/default/stat/device/"

# Define your credentials
username = "api2"
password = "HarfordSound69"

# Create a session object
session = requests.Session()

# Login to the Unifi controller
login_data = {
    "username": username,
    "password": password
}

# Disable SSL certificate verification
session.verify = False

response = session.post(login_url, json=login_data)

# Check if login was successful
if response.status_code != 200:
    print("Login failed!")
    print(response.json())
    exit()

print("Login successful!")

# Get device status
device_status_response = session.get(device_status_url)

# Check if getting device status was successful
if device_status_response.status_code != 200:
    print("Failed to get device status!")
    exit()

# Print device status
print("Device Status:")
print(device_status_response.json())
