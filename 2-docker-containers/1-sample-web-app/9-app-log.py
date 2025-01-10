# added logging services

import os, logging
from flask import Flask

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    return logger

logger = get_logger('flask-service')
app = Flask(__name__)

def to_fahrenheit(celsius):
    try:
        return int(celsius) * 9./5 + 32
    except Exception as e:
        logger.err(e.args[0])
        return -1

@app.get('/')
def hello():
    celsius = 20
    txt = f"Fahrenheit({celsius}): {to_fahrenheit(celsius)}"
    logger.info(txt)
    return txt

if __name__ == '__main__':
    SERVICE_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVICE_PORT = os.getenv('SERVER_PORT', 8000)
    app.run(host=SERVICE_HOST, port=SERVICE_PORT, debug=True)