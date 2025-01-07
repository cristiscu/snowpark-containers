import logging, os, sys
from flask import Flask, request
from flask import make_response, render_template

SERVICE_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVICE_PORT = os.getenv('SERVER_PORT', 8080)
CHARACTER_NAME = os.getenv('CHARACTER_NAME', 'I')

def get_echo_response(input):
    return f'{CHARACTER_NAME} said {input}'

def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    fmtter = logging.Formatter('%(name)s [%(asctime)s] [%(levelname)s] %(message)s')
    handler.setFormatter(fmtter)
    logger.addHandler(handler)
    return logger

logger = get_logger('echo-service')
app = Flask(__name__)

@app.get("/healthcheck")
def readiness_probe():
    return "I'm ready!"

@app.post("/echo")
def echo():
    message = request.json
    logger.debug(f'Received request: {message}')

    if message is None or not message['data']:
        logger.info('Received empty message')
        return {}

    # I/O format: { "data": [[row_index, col1_val, ...], ...]}
    input_rows = message['data']
    logger.info(f'Received {len(input_rows)} rows')

    output_rows = [[row[0], get_echo_response(row[1])] for row in input_rows]
    logger.info(f'Produced {len(output_rows)} rows')

    response = make_response({"data": output_rows})
    response.headers['Content-type'] = 'application/json'
    logger.debug(f'Sending response: {response.json}')
    return response

@app.route("/ui", methods=["GET", "POST"])
def ui():
    if request.method != "POST":
        return render_template("basic_ui.html")
    
    input = request.form.get("input")
    response = get_echo_response(input)
    return render_template("basic_ui.html",
        echo_input=input, echo_reponse=response)

if __name__ == '__main__':
    app.run(host=SERVICE_HOST, port=SERVICE_PORT)
