USE ROLE ACCOUNTADMIN;
USE test.public;

SHOW IMAGES IN IMAGE REPOSITORY repo;
SHOW COMPUTE POOLS;

-- ==============================================
-- create CPU pool
CREATE COMPUTE POOL cpu1
    INSTANCE_FAMILY=CPU_X64_XS
    MIN_NODES=1
    MAX_NODES=1
    INITIALLY_SUSPENDED=TRUE
    AUTO_SUSPEND_SECS=60;
DESC COMPUTE POOL cpu1;
ALTER COMPUTE POOL cpu1 STOP ALL;
DESC COMPUTE POOL cpu1;

-- ==============================================
-- create+drop GPU pool
CREATE COMPUTE POOL gpu1
    INSTANCE_FAMILY=GPU_NV_S
    MIN_NODES=1
    MAX_NODES=3
    -- INITIALLY_SUSPENDED=TRUE
    AUTO_SUSPEND_SECS=60;
DESC COMPUTE POOL gpu1;
ALTER COMPUTE POOL gpu1 SUSPEND;
DESC COMPUTE POOL gpu1;

DROP COMPUTE POOL gpu1;
SHOW COMPUTE POOLS;