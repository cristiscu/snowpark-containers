-- execute one by one in a SQL Worksheet, in a commercial Snowflake account

-- =========================================================
-- (1) service role (account-level, other than ACCOUNTADMIN!)
use role sysadmin;

-- =========================================================
-- (2) image repository (schema-level!)
create or replace database hello_db;
use hello_db.public;

create image repository hello_repo;

-- copy repository_url!
show image repositories;

-- =========================================================
-- (3) compute pool (account-level)
create compute pool hello_pool
    min_nodes = 1
    max_nodes = 1
    instance_family = CPU_X64_XS;

show compute pools;

alter compute pool hello_pool suspend;
