# this could run like a job service connecting to Snowflake

import os, argparse
from snowflake.snowpark import Session

# pass input data w/ env vars
session = Session.builder.configs({
	"account": os.getenv("SNOWFLAKE_ACCOUNT"),
	"user": os.getenv("SNOWFLAKE_USER"),
	"password": os.getenv("SNOWFLAKE_PASSWORD")
}).create()

# pass input data w/ command line args
# ex: python file.py --table "snowflake.account_usage.columns"
parser = argparse.ArgumentParser()
parser.add_argument("--table", required=False)
args = parser.parse_args()
table = args.table
if args.table is None:
	table = "snowflake.account_usage.databases"

query = f"select * from {table}"
session.sql(query).show()