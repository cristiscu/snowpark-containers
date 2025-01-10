# test service (not Flask!)

import requests

# { "data": [[0, 20]] } --> { "data": [[0, 68]] }
def client():
    return requests.post(
        "http://localhost:5000/service",
        json={ "data": [[0, "20"]]} ).json()

if __name__ == '__main__':
    client()