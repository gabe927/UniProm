import json

# get data
f = open("device_status_example.json", "r")
data = json.loads(f.read())
data = data["data"]


# Filter Devices
devices = []

def isValidDevice(dut):
    return i["type"] == "usw" and (i["model"] == "USL24P" or i["model"] == "USL24PB")

for i in data:
    if isValidDevice(i):
        devices.append(i)

# for i in devices:
#     print(i["name"])

# Map MAC addresses to devices
MACs = {}

for i in devices:
    MACs.update({i["name"]:i["mac"]})

print(MACs)