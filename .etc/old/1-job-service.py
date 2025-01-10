# this could run like a job service

import os
from snowflake.snowpark import Session

session = Session.builder.configs({
	"account": os.getenv("SNOWFLAKE_ACCOUNT"),
	"user": os.getenv("SNOWFLAKE_USER"),
	"password": os.getenv("SNOWFLAKE_PASSWORD")
}).create()

query = f"select * from snowflake.account_usage.databases"
print(f"Query: {query}")
session.sql(query).show()