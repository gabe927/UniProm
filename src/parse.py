import json

# get data
f = open("device_status_example.json", "r")
data = json.loads(f.read())
data = data["data"]

# Switch Names:
class switch_names:
    dimmer_beach_pri = "BEACH-SW-PRI"
    dimmer_beach_sec = "BEACH-SW-SEC"
    foh_pri = "FOH-SW-PRI"
    foh_sec = "FOH-SW-SEC"

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
lldp_table = {}

for i in devices:
    lldp_table.update({i["name"]:[]})
    for j in i["lldp_table"]:
        temp_dict:dict = j
        device_mac = temp_dict["chassis_id"]
        if device_mac in MACs:
            temp_dict.update({"recognized_device":MACs[device_mac]})
        lldp_table[i["name"]].append(temp_dict)

print(json.dumps(lldp_table, indent=4))


# Build snake status
# {
#     -1: "error",
#     0: "down",
#     1: "ok"
#     2: "flipped"
#     3: "unknown"
# }

# assume down stautus and change to other statuses based on logic below
snake_status = {
    "ethernet":{
        "primary":0,
        "backup":0
    },
    "fiber":{
        "primary":0,
        "backup":0
    }
}

"""
function for checking status of the snake ports
@param dut : device under test, the switch from switch_names class you which to check
@param port_idx : the port id to check, same as local_port_idx in the Unifi API
@param media_type : ethernet or fiber
@param port_rank : primary or backup
@param expected_sw : expected switch for OK status
@param flipped_sw : switch for flipped status
"""
def check_snake_port(dut, port_idx, media_type, port_rank, expected_sw, flipped_sw):
    if dut not in lldp_table:
        snake_status[media_type][port_rank] = -1
    else:
        dut_lldp_table = lldp_table[dut]
        for i in dut_lldp_table:
            if i["local_port_idx"] == port_idx:
                if "recognized_device" not in i:
                    snake_status[media_type][port_rank] = 3
                elif i["recognized_device"] == expected_sw:
                    snake_status[media_type][port_rank] = 1
                elif i["recognized_device"] == flipped_sw:
                    snake_status[media_type][port_rank] = 2

# check primary ethernet
check_snake_port(switch_names.dimmer_beach_pri, 24, "ethernet", "primary", switch_names.foh_pri, switch_names.foh_sec)
# check primary fiber
check_snake_port(switch_names.dimmer_beach_pri, 25, "fiber", "primary", switch_names.foh_pri, switch_names.foh_sec)
# check backup ethernet
check_snake_port(switch_names.dimmer_beach_sec, 24, "ethernet", "backup", switch_names.foh_sec, switch_names.foh_sec)
# check backup fiber
check_snake_port(switch_names.dimmer_beach_sec, 25, "fiber", "backup", switch_names.foh_sec, switch_names.foh_sec)

print(snake_status)