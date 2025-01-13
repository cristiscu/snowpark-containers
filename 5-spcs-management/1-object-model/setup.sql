use role accountadmin;

-- =============================================
-- image repo (must manually upload job1 and service1 images!)
create database if not exists test;
use test.public;

show image repositories;
create image repository if not exists repo;
show images in image repository repo;

-- =============================================
-- compute pool
show compute pools;
create compute pool if not exists cpu5
    INSTANCE_FAMILY=CPU_X64_XS
    MIN_NODES=1
    MAX_NODES=1;
alter compute pool cpu5 suspend;
desc compute pool cpu5;

-- =============================================
-- service role
create role if not exists role5;
grant role role5 to role sysadmin;

grant usage on database test to role role5;
grant all on schema test.public to role role5;
grant usage, operate on warehouse compute_wh to role role5;

grant read on image repository test.public.repo to role role5;
grant usage, operate on compute pool cpu5 to role role5;
grant create service on schema test.public to role role5;
grant bind service endpoint on account to role role5;

-- =============================================
-- services
use role role5;

execute job service
    IN COMPUTE POOL cpu5
    FROM SPECIFICATION $$
        spec:
          containers:
          - name: job5c
            image: /test/public/repo/job1
    $$
    NAME=job5
    ASYNC=true;

create service if not exists service5
    IN COMPUTE POOL cpu5
    FROM SPECIFICATION $$
        spec:
          containers:
          - name: service5c
            image: /test/public/repo/service1
          endpoints:
          - name: ep5
            port: 8000
            public: true
    $$
    MIN_INSTANCES=1
    MAX_INSTANCES=1;
alter service service5 suspend;

show endpoints in service service5;
show service instances in service service5;
show service containers in service service5;

-- =============================================
-- make sure nothing is running (to save money)
alter compute pool cpu5 suspend;
show compute pools;