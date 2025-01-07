-- execute one by one in a SQL Worksheet, in a commercial Snowflake account
use role sysadmin;
use hello_db.public;

-- check that the previous image has been uploaded
show images in image repository hello_repo;

-- =========================================================
-- (4) long-running service (schema-level)
create service hello_service
  in compute pool hello_pool
  from specification $$
    spec:
      containers:
      - name: hello
        image: /hello_db/public/hello_repo/hello_image
      endpoints:
      - name: hello
        port: 8000
        public: true
    $$;
show services in schema hello_db.public;

show service instances in service hello_service;
show service containers in service hello_service;

-- check ingress_url value ina browser! (must re-login first)
-- ~https://mqdeegc-yictmgu-xtractpro-std.snowflakecomputing.app/
show endpoints in service hello_service;