import os
import streamlit as st
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
st.write(f"database={database}, schema={schema}, warehouse={warehouse}, role={role}")

table = st.text_input("Table:", value="snowflake.account_usage.databases")
query = f"select * from {table} limit 10"
st.write(f"Query: {query}")
df = session.sql(query)
st.dataframe(df)
