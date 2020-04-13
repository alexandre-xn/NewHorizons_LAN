import socket
import sys

server_reqs = ['0145000028032500004011eb370a0d784f0a0dffff2cbc2cbc0014d4bf001445110000000000000000',
               '0145000028032600004011eb360a0d784f0a0dffff2cbc2cbc0014d4bf001445110000000000000000',
               '0145000028032700004011eb350a0d784f0a0dffff2cbc2cbc0014d4bf001445110000000000000000']

VERBOSE_MODE = sys.argv.pop()


def fetch_hosts_from_server(server_name, portnum):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

    if any(c.isalpha() for c in server_name):  # Handle direct IPs without server names
        ipaddr = socket.gethostbyname(server_name)
    else:
        ipaddr = server_name

    print("Server : " + server_name + " @ " + ipaddr)
    s.connect((ipaddr, portnum))
    s.settimeout(2)

    retry_times = 3
    req_index = 0

    data = ""
    hosts_found = False

    req = server_reqs[0]
    s.send(bytes.fromhex(req))

    try:
        while retry_times != 0 and not hosts_found:
            data = s.recv(1024)
            if VERBOSE_MODE == "debug":
                print(">>data run " + str(retry_times))
                print(data)
            data = data.decode('ascii', 'ignore').replace('\n', '')
            
            hosts_found = "12345678" in data
            retry_times -= 1
            req_index += 1

        if not hosts_found:
            data = "No hosts available"

    except socket.timeout:
        data = "Timed out"

    print(" Response : " + data)


fetch_hosts_from_server('switch.lan-play.com', 11452)
fetch_hosts_from_server('lanplay.reboot.ms', 11451)
fetch_hosts_from_server('open.t0g3pii.tk', 11451)
fetch_hosts_from_server('frog-skins.com', 11451)
fetch_hosts_from_server('switch.jayseateam.nl', 11451)
fetch_hosts_from_server('chasehall.net', 11451)
fetch_hosts_from_server('nook-inc.net', 11451)
fetch_hosts_from_server('81.98.26.94', 11451)
