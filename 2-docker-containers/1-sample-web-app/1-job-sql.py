# this could run like a job service connecting to Snowflake

import os
from snowflake.snowpark import Session

# pass input data w/ env vars
session = Session.builder.configs({
	"account": os.getenv("SNOWFLAKE_ACCOUNT"),
	"user": os.getenv("SNOWFLAKE_USER"),
	"password": os.getenv("SNOWFLAKE_PASSWORD")
}).create()

table = "snowflake.account_usage.databases"
query = f"select * from {table}"
session.sql(query).show()