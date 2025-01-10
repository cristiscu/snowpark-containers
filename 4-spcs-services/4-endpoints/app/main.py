import json, logging, requests

logger = logging.getLogger('service-to-service')
logger.setLevel(logging.DEBUG)

def call_service(url, msg):
    response = requests.post(url=url,
        data=json.dumps({"data": [[0, msg]]}),
        headers={"Content-Type": "application/json"})
    res = response.json()["data"][0]
    logger.info(f'{url}: {msg} --> {res[1]}')

if __name__ == '__main__':
    call_service('http://echo-service:8000/echo', 'Hello')
