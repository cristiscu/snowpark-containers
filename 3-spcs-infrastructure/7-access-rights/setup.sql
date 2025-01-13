-- use external objects (created by ACCOUNTADMIN)

USE ACCOUNTADMIN;

-- custom role (this could be SYSADMIN!)
DROP ROLE IF EXISTS my_role;
CREATE ROLE my_role;
GRANT ROLE my_role to role sysadmin;
-- GRANT ROLE my_role TO USER cristiscu;  -- replace with your username!

-- grant USAGE on existing database objects
grant USAGE on database test to role my_role;
grant USAGE on schema test.public to role my_role;
grant SELECT on schema test.public.diamonds to role my_role;
grant USAGE, OPERATE on warehouse compute_wh to role my_role;

-- grant USAGE on container-specific objects
grant READ on image repository test.public.repo to role my_role;
grant USAGE, OPERATE on compute pool cpu to role my_role;

-- grant CREATE privileges on own services (cannot use ACCOUNTADMIN!)
grant CREATE SERVICE on schema test.public to role my_role;
grant CREATE NOTEBOOK on schema test.public to role my_role;

CREATE SERVICE my_service
  IN COMPUTE POOL cpu
  FROM SPECIFICATION $$
    spec:
      containers:
      - name: echo
        image: /test/public/repo/image
      endpoints:
      - name: echoendpoint
        port: 8000
        public: true
  $$
  MIN_INSTANCES=1
  MAX_INSTANCES=1;
grant OPERATE, MONITOR on service my_service to role ACCOUNTADMIN;
grant SERVICE ROLE my_service!ALL_ENDPOINTS_USAGE to role ACCOUNTADMIN;
