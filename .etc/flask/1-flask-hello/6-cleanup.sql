-- execute one by one in a SQL Worksheet, in a commercial Snowflake account
use role sysadmin;
use hello_db.public;

-- =========================================================
-- stop service/pool
describe service hello_service;
alter service hello_service suspend;
describe service hello_service;

describe compute pool hello_pool;
alter compute pool hello_pool suspend;
describe compute pool hello_pool;

-- =========================================================
-- cleanup all

-- auto-delete repo + service
drop database hello_db cascade;

drop compute pool hello_pool;
show compute pools;