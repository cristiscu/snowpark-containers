-- see https://docs.snowflake.com/en/developer-guide/snowpark-container-services/tutorials/tutorial-1#create-a-service
use role role1;
use test.public;

-- service
CREATE SERVICE service1
  IN COMPUTE POOL pool1
  FROM SPECIFICATION $$
    spec:
      containers:
      - name: echo
        image: /test/public/repo1/service1
        env:
          SERVER_PORT: 8000
          CHARACTER_NAME: Cristian
        readinessProbe:
          port: 8000
          path: /healthcheck
      endpoints:
      - name: echoendpoint
        port: 8000
        public: true
    $$;
SHOW SERVICES;
SHOW SERVICE CONTAINERS IN SERVICE service1;
SHOW ENDPOINTS IN SERVICE service1;

-- service function
CREATE FUNCTION service1_udf(txt varchar)
    RETURNS varchar
    SERVICE = service1
    ENDPOINT = echoendpoint
AS '/echo';

SELECT service1_udf('hello!');

SELECT $1, service1_udf($1)
FROM VALUES ('Thank you'), ('Hello'), ('Hello World');

-- test in browser
-- https://eqdeegc-yictmgu-xtractpro-std.snowflakecomputing.app/ui

-- stop service/pool
describe service service1;
alter service service1 suspend;

describe compute pool pool1;
alter compute pool pool1 suspend;