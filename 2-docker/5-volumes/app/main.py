import os, sys, logging
from flask import Flask, request, render_template, jsonify

# ~business logic
def to_fahrenheit(celsius):
    return celsius * 9./5 + 32

# logging services
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

# can use as service healthcheck (readiness probe)
@app.route('/')
def to_fahrenheit():
	celsius = 20
	return f"Fahrenheit(celsius): {to_fahrenheit(celsius)}"

# (1) I/O data through UI
@app.route("/ui", methods=["GET", "POST"])
def ui():
    celsius = request.form.get("celsius")
    logger.info(f'Received from UI: {celsius}')
    return render_template("basic_ui.html",
        fahrenheit=to_fahrenheit(celsius))

# (2) I/O data through JSON: { "data": [[row_index, val1, ...], ...]}
@app.get('/service')
def service():
    data_in = request.get_json()
    if 'data' not in data_in:
        logger.error(f'Bad data format: {data_in}')
    
    logger.debug(f'Received: {data_in}')
    data_out = [[row[0], to_fahrenheit(row[1])] for row in data_in['data']]
    ret = jsonify({'data': data_out})
    logger.debug(f'Returned: {ret}')

    # this could use a storage volume
    with open("logs/log.txt", "a") as f:
        f.write(f"{data_in}: {ret}\n")
    return ret

if __name__ == '__main__':
    # (3) I/O data as environment variables
    SERVICE_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVICE_PORT = os.getenv('SERVER_PORT', 8000)
    app.run(host=SERVICE_HOST, port=SERVICE_PORT, debug=True)