# connect to Snowflake locally

import os, sys, logging, warnings
warnings.filterwarnings('ignore', category=UserWarning, module='snowflake.connector')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))

def get_params():
    params = { "account": os.getenv("SNOWFLAKE_ACCOUNT") }
    logger.debug(f'[Account: {params["account"]}]')

    path = "/snowflake/session/token"
    if os.path.exists(path):
        with open(path, "r") as f:
            params["authenticator"] = "oauth"
            params["token"] = f.read()
            logger.debug(f'[Token: {params["token"]}]')
    
            params["host"] = os.getenv("SNOWFLAKE_HOST")
            logger.debug(f'[Host: {params["host"]}]')
            params["database"] = os.getenv("SNOWFLAKE_DATABASE")
            logger.debug(f'[Database: {params["database"]}]')
            params["schema"] = os.getenv("SNOWFLAKE_SCHEMA")
            logger.debug(f'[Schema: {params["schema"]}]')
            #params["warehouse"] = 'COMPUTE_WH'  # we'll use QUERY_WAREHOUSE instead!
    else:
        params["user"] = os.getenv("SNOWFLAKE_USER")
        params["password"] = os.getenv("SNOWFLAKE_PASSWORD")
    return params

from snowflake.snowpark import Session
session = Session.builder.configs(get_params()).create()
role = session.get_current_role()
print(f'Role: {role}')

# warehouse = session.get_current_warehouse()
query = "select current_warehouse()"
warehouse = session.sql(query).collect()[0][0]
print(f'Warehouse: {warehouse}')

query = "select count(*) from snowflake.account_usage.databases"
records = session.sql(query).collect()[0][0]
print(f'Count: {records}')
logger.info(f'[Total {records} records]')
