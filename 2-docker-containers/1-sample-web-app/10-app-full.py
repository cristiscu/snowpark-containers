import os, sys, logging, argparse, requests
from flask import Flask, request, render_template, make_response
from snowflake.snowpark import Session

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

# dump call history from file
@app.get('/history')
def dump():
    with open("logs/log.txt", "r") as f:
        return f.read(f)

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
    if data_in is None or not data_in['data']:
        logger.info('Received empty message')
        return {}
    
    logger.debug(f'Received: {data_in}')
    data_out = [[row[0], to_fahrenheit(row[1])] for row in data_in['data']]
    ret = {"data": data_out}
    logger.debug(f'Returned: {ret}')
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

# (6) job running a Snowflake query
def query(table):

    # (7) I/O data as environment variables
    params = {
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD")
    }
    session = Session.builder.configs(params).create()
    
    database = session.get_current_database()
    schema = session.get_current_schema()
    warehouse = session.get_current_warehouse()
    role = session.get_current_role()
    logger.info(f"database={database}, schema={schema}, warehouse={warehouse}, role={role}")

    return session.sql(f"select * from {table} limit 10").show()

if __name__ == '__main__':

    # (8) I/O data as command line args
    # ex: python main.py --table "snowflake.account_usage.databases"
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", required=False)
    args = parser.parse_args()
    table = args.table
    if table is not None:
        query(table)
    else:
        SERVICE_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
        SERVICE_PORT = os.getenv('SERVER_PORT', 8000)
        app.run(host=SERVICE_HOST, port=SERVICE_PORT, debug=True)