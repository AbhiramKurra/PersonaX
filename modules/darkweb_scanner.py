import requests
import socks
import socket

def run(data):
    email = data.get("email")
    username = data.get("username")
    if not (email or username):
        return "No email or username provided."
    # Set up Tor proxy
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket
    onion_sites = [
        "http://msydqstlz2kzerdg.onion"  # Example: Ahmia
    ]
    found = []
    for site in onion_sites:
        try:
            r = requests.get(site, timeout=10)
            if r.status_code == 200 and ((email and email in r.text) or (username and username in r.text)):
                found.append(site)
        except Exception as e:
            continue
    return found or "No dark web results found." 