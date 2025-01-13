use role accountadmin;
grant IMPORTED PRIVILEGES on database snowflake to role sysadmin;

USE ROLE SYSADMIN;
USE test.public;

select count(*) from snowflake.account_usage.databases;

SHOW IMAGES IN IMAGE REPOSITORY repo;
SHOW COMPUTE POOLS;

EXECUTE JOB SERVICE
    IN COMPUTE POOL cpu1
    FROM SPECIFICATION $$
        spec:
          containers:
          - name: sql-job-cont
            image: /test/public/repo/sql-job
    $$
    NAME=sql_job
    ASYNC=true
    QUERY_WAREHOUSE='compute_wh';   -- try first without it!
DESC SERVICE sql_job;
SHOW SERVICES;
CALL SYSTEM$GET_SERVICE_STATUS('sql_job')

SHOW SERVICE INSTANCES IN SERVICE sql_job;
SHOW SERVICE CONTAINERS IN SERVICE sql_job;
SELECT SYSTEM$GET_SERVICE_LOGS('sql_job', 0, 'sql-job-cont')

ALTER SERVICE sql_job SUSPEND;
DROP SERVICE sql_job;

ALTER COMPUTE POOL cpu1 SUSPEND;
SHOW COMPUTE POOLS;
