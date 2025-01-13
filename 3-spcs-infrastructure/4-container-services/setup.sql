USE ROLE ACCOUNTADMIN;
USE test.public;

SHOW IMAGES IN IMAGE REPOSITORY repo;
SHOW COMPUTE POOLS;

-- ==============================================
-- execute job service (this will fail!)
EXECUTE JOB SERVICE
    IN COMPUTE POOL cpu1
    FROM SPECIFICATION $$
        spec:
          containers:
          - name: job1c
            image: /test/public/repo/job1
    $$
    NAME=job1;

-- grant access to SYSADMIN
grant USAGE on database test to role SYSADMIN;
grant ALL on schema test.public to role SYSADMIN;
grant ALL on warehouse compute_wh to role SYSADMIN;

grant READ on image repository test.public.repo to role SYSADMIN;
grant USAGE, OPERATE on compute pool cpu1 to role SYSADMIN;

-- ==============================================
-- execute job service (with another role!)
USE ROLE SYSADMIN;
EXECUTE JOB SERVICE
    IN COMPUTE POOL cpu1
    FROM SPECIFICATION $$
        spec:
          containers:
          - name: job1c
            image: /test/public/repo/job1
    $$
    NAME=job1
    ASYNC=true;
DESC SERVICE job1;
CALL SYSTEM$GET_SERVICE_STATUS('job1')
SHOW SERVICES;

SHOW SERVICE INSTANCES IN SERVICE job1;
SHOW SERVICE CONTAINERS IN SERVICE job1;
SELECT SYSTEM$GET_SERVICE_LOGS('job1', 0, 'job1c')

ALTER SERVICE job1 SUSPEND;
DROP SERVICE job1;
SHOW COMPUTE POOLS;

-- ==============================================
-- create long-running service
CREATE SERVICE service1
    IN COMPUTE POOL cpu1
    FROM SPECIFICATION $$
        spec:
          containers:
          - name: service1c
            image: /test/public/repo/service1
            env:
              VAR1: val1
              VAR2: val2
          endpoints:
          - name: ep1
            port: 8000
            public: true
    $$
    MIN_INSTANCES=1
    MAX_INSTANCES=1;
DESC SERVICE service1;
SHOW SERVICE INSTANCES IN SERVICE service1;
SHOW SERVICE CONTAINERS IN SERVICE service1;

-- go to ingress_url when RUNNING (req OAuth)
SHOW ENDPOINTS IN SERVICE service1;

ALTER SERVICE service1 SUSPEND;
DESC SERVICE service1;

ALTER COMPUTE POOL cpu1 SUSPEND;
SHOW COMPUTE POOLS;
