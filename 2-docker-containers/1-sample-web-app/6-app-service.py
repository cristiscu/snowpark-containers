# I/O data through JSON: { "data": [[row1, val1, ...], ...]}

import requests
from flask import Flask, request, make_response

app = Flask(__name__)

def to_fahrenheit(celsius):
    return int(celsius) * 9./5 + 32

@app.post('/service')
def service():
    data_in = request.json
    if data_in is None or not data_in['data']:
        return { }
    
    data_out = [[row[0], to_fahrenheit(row[1])] for row in data_in['data']]
    ret = { "data": data_out }
    response = make_response(ret)
    response.headers['Content-type'] = 'application/json'
    return response

# { "data": [[0, 20]] } --> { "data": [[0, 68]] }
@app.get('/client')
def client():
    response = requests.post(
        f'{request.host_url}service',
        json={ "data": [[0, "20"]] })
    return response.json()

if __name__ == '__main__':
    app.run()