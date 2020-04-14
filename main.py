import socket
import sys

server_reqs = ['0145000028032500004011eb370a0d784f0a0dffff2cbc2cbc0014d4bf001445110000000000000000',
               '0145000028032600004011eb360a0d784f0a0dffff2cbc2cbc0014d4bf001445110000000000000000',
               '0145000028032700004011eb350a0d784f0a0dffff2cbc2cbc0014d4bf001445110000000000000000']

VERBOSE_MODE = sys.argv.pop()


def fetch_hosts_from_server(server_name, portnum):
    hosts = []
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

    if any(c.isalpha() for c in server_name):  # Handle direct IPs without server names otherwise
        ipaddr = socket.gethostbyname(server_name)
    else:
        ipaddr = server_name

    print("Server : " + server_name + " @ " + ipaddr)
    s.connect((ipaddr, portnum))
    s.settimeout(2)

    retry_times = 5

    req = server_reqs[0]
    s.send(bytes.fromhex(req))

    try:
        while retry_times != 0:
            data = s.recv(2048)
            if VERBOSE_MODE == "debug":
                print(">>data run " + str(retry_times))
                print(data)

            hosts_found = "12345678" in data.decode('utf-8', 'ignore')

            if hosts_found and data not in hosts:
                data = data.decode('utf-8', 'ignore').replace('\n', '')
                # case russian name : print(data.decode('utf_16', 'ignore').replace('\n', ''))
                print(data)
                hosts.append(data)

            retry_times -= 1

    except socket.timeout:
        print("Response : Timed out")

    return hosts


def fetch_all():
    print(fetch_hosts_from_server('switch.lan-play.com', 11452))
    print(fetch_hosts_from_server('lanplay.reboot.ms', 11451))
    print(fetch_hosts_from_server('open.t0g3pii.tk', 11451))
    print(fetch_hosts_from_server('frog-skins.com', 11451))
    print(fetch_hosts_from_server('switch.jayseateam.nl', 11451))
    print(fetch_hosts_from_server('chasehall.net', 11451))
    print(fetch_hosts_from_server('nook-inc.net', 11451))
    print(fetch_hosts_from_server('81.98.26.94', 11451))


fetch_all()
