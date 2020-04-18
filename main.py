import socket
import sys
from enum import Enum

class PayloadPart(Enum):
    SPACE_1 = 0,
    SPACE_2 = 1,
    LETTER = 2


server_reqs = ['0145000028032500004011eb370a0d784f0a0dffff2cbc2cbc0014d4bf001445110000000000000000',
               '0145000028032600004011eb360a0d784f0a0dffff2cbc2cbc0014d4bf001445110000000000000000',
               '0145000028032700004011eb350a0d784f0a0dffff2cbc2cbc0014d4bf001445110000000000000000']

VERBOSE_MODE = "not_verbose"


def fetch_hosts_from_server(server_name, portnum):
    hosts = []
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

    if any(c.isalpha() for c in server_name):  # Handle direct IPs without server names otherwise
        ipaddr = socket.gethostbyname(server_name)
    else:
        ipaddr = server_name

    print("Server : " + server_name + " @ " + ipaddr)
    s.connect((ipaddr, portnum))
    s.settimeout(3)

    retry_times = 5

    req = server_reqs[0]
    s.send(bytes.fromhex(req))

    try:
        while retry_times != 0:
            data = s.recv(2048)
            data = data.decode('utf-8', 'ignore')

            if "12345678" in data:
                udp_payload = data.replace('\n', '')
                # case russian name : print(data.decode('utf_16', 'ignore').replace('\n', ''))
                if VERBOSE_MODE == "debug":
                    print(udp_payload)

                player_count = convert_raw_int_to_int(udp_payload[str.index(udp_payload, '>') - 2])
                player_list = []
                for i in range(0, player_count):
                    temp_player, udp_payload = extract_next_string_from_udp_payload(udp_payload)
                    player_list.append(temp_player)
                island_name, udp_payload = extract_next_string_from_udp_payload(udp_payload)
                if len(island_name) == 1:
                    if VERBOSE_MODE == "debug":
                        print("Missing player names")
                    if len(player_list[-1]) != 1:
                        island_name = player_list[-1]
                    else:
                        island_name = "Russian"
                        player_count = 1

                hosts.append((island_name, player_list, player_count))
            else:
                if VERBOSE_MODE == "debug":
                    print("Data received but no hosts")

            retry_times -= 1
        print("Response : Communication established")

    except socket.timeout:
        print("Response : Timed out (no hosts ?)")
    

    return hosts

def extract_next_string_from_udp_payload(payload):
    payload = payload[::-1]
    d = payload[0]
    str_index = 0
    string = ""
    while ord(d) <= 32:
        str_index += 1
        d = payload[str_index]
    next_byte = PayloadPart.LETTER
    next_byte_correct = True
    while next_byte_correct:
        string += d
        str_index += 1
        d = payload[str_index]
        if next_byte == PayloadPart.LETTER:
            next_byte_correct = ord(d) == 0
            next_byte = PayloadPart.SPACE_1
        elif next_byte == PayloadPart.SPACE_1:
            next_byte_correct = ord(d) == 0
            next_byte = PayloadPart.SPACE_2
        else:
            next_byte_correct = 32 <= ord(d) <= 126
            next_byte = PayloadPart.LETTER
    payload = payload[::-1]
    return string[::-1].replace('\x00', ''), payload[0:len(payload) - str_index - 3]


def convert_raw_int_to_int(
        raw_int):  # Converts the Python raw string to a proper int for the player count, i've not found a cleaner way
    switcher = {
        '': 1,
        '': 2,
        '': 3,
        '': 4,
        '': 5,
        '': 6,
        '': 7
    }
    return switcher.get(raw_int, 1)


def fetch_all():
    print(fetch_hosts_from_server('switch.lan-play.com', 11452))
    print(fetch_hosts_from_server('lanplay.reboot.ms', 11451))
    print(fetch_hosts_from_server('open.t0g3pii.tk', 11451))
    print(fetch_hosts_from_server('frog-skins.com', 11451))
    print(fetch_hosts_from_server('chasehall.net', 11451))
    print(fetch_hosts_from_server('nook-inc.net', 11451))
    print(fetch_hosts_from_server('81.98.26.94', 11451))
    print(fetch_hosts_from_server('lanplay2.reboot.ms', 11451))
    print(fetch_hosts_from_server('joinsg.net', 11451))
    print("------------")
    fetch_all()

#fetch_all()
print(str(sys.argv[1]) + ":" + sys.argv[2])
print(fetch_hosts_from_server(str(sys.argv[1]), int(sys.argv[2])))