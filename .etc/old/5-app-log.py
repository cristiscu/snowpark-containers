# added logging services

import sys, logging
from flask import Flask

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(name)s [%(asctime)s] [%(levelname)s] %(message)s')
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger

logger = get_logger('flask-service')
app = Flask(__name__)

def to_fahrenheit(celsius):
    return int(celsius) * 9./5 + 32

@app.get('/')
def hello():
    celsius = 20
    txt = f"Fahrenheit({celsius}): {to_fahrenheit(celsius)}"
    logger.info(txt)
    return txt

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)