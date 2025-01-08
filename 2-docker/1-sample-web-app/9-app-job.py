# call with: python main.py --table "snowflake.account_usage.databases"

import os, argparse
from flask import Flask
from snowflake.snowpark import Session

app = Flask(__name__)

# job running a Snowflake query
def query(table):

    # I/O data as environment variables
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
    print(f"database={database}, schema={schema}, warehouse={warehouse}, role={role}")

    return session.sql(f"select * from {table} limit 10").show()

# I/O data as command line args
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--table", required=True)
    args = parser.parse_args()
    query(args.table)
