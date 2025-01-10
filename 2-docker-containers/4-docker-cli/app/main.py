import os, sys, logging
from flask import Flask, request, render_template, jsonify

# (1) logging services
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

# (2) business logic --> could later use a storage volume
def to_fahrenheit(celsius):
    fahrenheit = int(celsius) * 9./5 + 32
    try:
        with open("logs/log.txt", "a") as f:
            f.write(f"{celsius}: {fahrenheit}\n")
    except Exception as e:
        logger.warning(e.args[1])
    return fahrenheit

# (3) can use as service healthcheck (readiness probe)
@app.get('/')
def hello():
    celsius = 20
    txt = f"Fahrenheit({celsius}): {to_fahrenheit(celsius)}"
    logger.info(txt)
    return txt

# (4) I/O data through UI
@app.route("/ui", methods=["GET", "POST"])
def ui():
    if request.method != "POST":
        return render_template("basic_ui.html")

    celsius = request.form.get("input")
    logger.info(f'Received from UI: {celsius}')
    return render_template("basic_ui.html",
        celsius=celsius,
        fahrenheit=to_fahrenheit(celsius))

# (5) I/O data through JSON: { "data": [[row_index, val1, ...], ...]}
@app.post('/service')
def service():
    data_in = request.json
    if 'data' not in data_in:
        logger.error(f'Bad data format: {data_in}')
        return {}
    
    logger.debug(f'Received: {data_in}')
    data_out = [[row[0], to_fahrenheit(row[1])] for row in data_in['data']]
    ret = jsonify({'data': data_out})
    logger.debug(f'Returned: {ret}')
    return ret

if __name__ == '__main__':
    # (6) I/O data as environment variables
    SERVICE_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
    SERVICE_PORT = os.getenv('SERVER_PORT', 8000)
    app.run(host=SERVICE_HOST, port=SERVICE_PORT, debug=True)