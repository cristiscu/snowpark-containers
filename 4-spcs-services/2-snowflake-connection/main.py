# from Tutorial 2

import os, argparse, logging
from snowflake.snowpark import Session

def get_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True, help="query text to execute")
    parser.add_argument("--result_table", required=True,
        help= "name of the table to store result of query specified by flag --query")
    return parser

SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")

def get_login_token():
    path = "/snowflake/session/token"
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return None

def get_connection_params():
    token = get_login_token()
    return ({
        "account": SNOWFLAKE_ACCOUNT,
        "authenticator": "oauth",
        "token": token
    } if token is not None
    else {
        "account": SNOWFLAKE_ACCOUNT,
        "user": SNOWFLAKE_USER,
        "password": SNOWFLAKE_PASSWORD
    })

if __name__ == "__main__":

    logger = logging.getLogger("job-tutorial")
    logger.setLevel(logging.DEBUG)
    logger.info("Job started")

    args = get_arg_parser().parse_args()
    query = args.query
    result_table = args.result_table

    params = get_connection_params()
    session = Session.builder.configs(params).create()
    logger.info(f"Executing query [{query}] and writing result to table [{result_table}]")
    res = session.sql(query)
    res.write.mode("append").save_as_table(result_table)
    logger.info("Job finished")
