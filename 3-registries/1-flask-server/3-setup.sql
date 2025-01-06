-- see https://docs.snowflake.com/en/developer-guide/snowpark-container-services/tutorials/common-setup#create-snowflake-objects

-- service role
create role if not exists role1;
grant role role1 to role sysadmin;
grant all on warehouse compute_wh to role role1;
grant bind service endpoint on account to role role1;

-- database and schema
create database if not exists test;
use test.public;
grant usage on database test to role role1;
grant all on schema test.public to role role1;
grant create service on schema test.public to role role1;

-- stage (for service spec file)
create stage if not exists stage1
    directory = (enable = true);
grant read, write on stage test.public.stage1 to role role1;

-- image repository
create image repository if not exists repo1;
grant read on image repository repo1 to role role1;

-- yictmgu-xtractpro-std.registry.snowflakecomputing.com/test/public/repo1
show image repositories;
show image repositories like 'repo1' in schema test.public; -- no DESCRIBE!

-- compute pool
create compute pool if not exists pool1
    min_nodes = 1
    max_nodes = 1
    instance_family = CPU_X64_XS
    auto_suspend_secs = 60
    initially_suspended = TRUE;
alter compute pool pool1 suspend;
grant usage, monitor, operate on compute pool pool1 to role role1;

