-- ==================================================
-- start by running this one by one in a SQL Worksheet
-- could create a custom role instead (and grant it to sysadmin)
use role sysadmin;

create or replace database test2;
use test2.public;

create image repository repo2;

create compute pool if not exists pool2
    min_nodes = 1
    max_nodes = 3
    instance_family = GPU_NV_S
    auto_suspend_secs = 60
    initially_suspended = true;

-- ==================================================
-- continue with this AFTER you execute the Docker commands!
show images in image repository repo2;

create service jupyter_service
    in compute pool pool2
    from specification $$
        spec:
          container:
          - name: jupyterlab
            image: yictmgu-xtractpro-std.registry.snowflakecomputing.com/test2/public/repo2/jupyter:v1
            env:
              DISABLE_AUTH: true
          endpoints:
          - name: "jupyter"
            port: 8888
            public: true
    $$;
desc service jupyter_service;

alter service jupyter_service resume;
SHOW SERVICE CONTAINERS IN SERVICE jupyter_service;

-- paste ingress_url in new browser tab + connect to Snowflake
show endpoints in service jupyter_service;

-- find, copy and paste token value to previous url
call SYSTEM$GET_SERVICE_LOGS('jupyter_service', '0', 'jupyterlab');

-- ==================================================
-- to stop the compute resources (and save money)

alter service jupyter_service suspend;

alter compute pool pool2 suspend;

show compute pools;

-- ==================================================
-- to cleanup all (drop/remove ALL created resources)

-- auto-remove image repository (w/ large image!) + service
drop database test2 cascade;

drop compute pool pool2;
