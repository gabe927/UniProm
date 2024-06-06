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
    MACs.update({i["mac"]:i["name"]})

# Build LLDP table with device names
LLDP_table = {}

for i in devices:
    LLDP_table.update({i["name"]:[]})
    for j in i["lldp_table"]:
        temp_dict:dict = j
        device_mac = temp_dict["chassis_id"]
        if device_mac in MACs:
            temp_dict.update({"recognized_device":MACs[device_mac]})
        LLDP_table[i["name"]].append(temp_dict)

print(json.dumps(LLDP_table, indent=4))