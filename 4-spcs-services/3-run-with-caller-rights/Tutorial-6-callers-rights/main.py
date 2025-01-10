from flask import Flask
from flask import request
from flask import render_template
import logging, os, sys

from snowflake.snowpark import Session
from snowflake.snowpark.exceptions import *

# Environment variables below will be automatically populated by Snowflake.
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_HOST = os.getenv("SNOWFLAKE_HOST")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")

# Custom environment variables
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")

SERVICE_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = os.getenv("SERVER_PORT", 8080)


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter("%(name)s [%(asctime)s] [%(levelname)s] %(message)s")
    )
    logger.addHandler(handler)
    return logger


def get_login_token():
    """
    Read the login token supplied automatically by Snowflake. These tokens
    are short lived and should always be read right before creating any new connection.
    """
    with open("/snowflake/session/token", "r") as f:
        return f.read()


def get_connection_params(ingress_user_token=None):
    """
    Construct Snowflake connection params from environment variables.
    """
    if os.path.exists("/snowflake/session/token"):
        if ingress_user_token:
            logger.info("Creating a session on behalf of user.")
            token = get_login_token() + "." + ingress_user_token
        else:
            logger.info("Creating a session as service user.")
            token = get_login_token()

        return {
            "account": SNOWFLAKE_ACCOUNT,
            "host": SNOWFLAKE_HOST,
            "authenticator": "oauth",
            "token": token,
            "warehouse": SNOWFLAKE_WAREHOUSE,
            "database": SNOWFLAKE_DATABASE,
            "schema": SNOWFLAKE_SCHEMA,
        }
    else:
        return {
            "account": SNOWFLAKE_ACCOUNT,
            "host": SNOWFLAKE_HOST,
            "user": SNOWFLAKE_USER,
            "password": SNOWFLAKE_PASSWORD,
            "role": SNOWFLAKE_ROLE,
            "warehouse": SNOWFLAKE_WAREHOUSE,
            "database": SNOWFLAKE_DATABASE,
            "schema": SNOWFLAKE_SCHEMA,
        }


logger = get_logger("query-service")
app = Flask(__name__)


@app.get("/healthcheck")
def readiness_probe():
    return "I'm ready!"


@app.route("/ui", methods=["GET", "POST"])
def ui():
    """
    Main handler for providing a web UI.
    """
    if request.method == "POST":
        # get ingress user token
        ingress_user = request.headers.get("Sf-Context-Current-User")
        ingress_user_token = request.headers.get("Sf-Context-Current-User-Token")

        if ingress_user:
            logger.info(f"Received a request from user {ingress_user}")

        # getting input in HTML form
        query = request.form.get("query")
        if query:
            logger.info(f"Received a request for query: {query}.")
            query_result_ingress_user = (
                run_query(query, ingress_user_token)
                if ingress_user_token
                else "Token is missing. Can't execute as ingress user."
            )
            query_result_service_user = run_query(query)
            return render_template(
                "basic_ui.html",
                query_input=query,
                query_result_ingress_user=query_result_ingress_user,
                query_result_service_user=query_result_service_user,
            )
    return render_template("basic_ui.html")


@app.route("/query", methods=["GET"])
def query():
    """
    Main handler for providing a programmatic access.
    """
    # get ingress user token
    query = request.args.get("query")
    logger.info(f"Received query request: {query}.")
    if query:
        ingress_user = request.headers.get("Sf-Context-Current-User")
        ingress_user_token = request.headers.get("Sf-Context-Current-User-Token")

        if ingress_user:
            logger.info(f"Received a request from user {ingress_user}")

        res = run_query(query, ingress_user_token)
        return str(res)
    return "DONE"


def run_query(query, ingress_user_token=None):
    # start a Snowflake session as the ingress user
    try:
        with Session.builder.configs(
            get_connection_params(ingress_user_token)
        ).create() as session:
            logger.info(
                f"Snowflake connection established (id={session.session_id}). Now executing query: {query}."
            )
            try:
                res = session.sql(query).collect()
                logger.info(f"Query execution done: {query}.")
                return (
                    "[Empty Result]"
                    if len(res) == 0
                    else [", ".join(row) for row in res]
                )
            except Exception as e:
                return "Encountered an error when executing query: " + str(e)
    except Exception as e:
        return "Encountered an error when connecting to Snowflake: " + str(e)

if __name__ == '__main__':
  app.run(host=SERVICE_HOST, port=SERVER_PORT)

