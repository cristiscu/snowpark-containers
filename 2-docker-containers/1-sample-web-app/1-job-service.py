# this could run like a job service

import os
from snowflake.snowpark import Session

session = Session.builder.configs({
	"account": os.getenv("SNOWFLAKE_ACCOUNT"),
	"user": os.getenv("SNOWFLAKE_USER"),
	"password": os.getenv("SNOWFLAKE_PASSWORD")
}).create()

database = session.get_current_database()
schema = session.get_current_schema()
warehouse = session.get_current_warehouse()
role = session.get_current_role()
print(f"database={database}, schema={schema}, warehouse={warehouse}, role={role}")

table = "snowflake.account_usage.databases"
query = f"select * from {table}"
print(f"Query: {query}")
session.sql(query).show()
