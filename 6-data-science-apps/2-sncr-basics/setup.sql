-- (Phase 1)
-- must have the table test.public.diamonds imported from diamonds.csv
CREATE ROLE IF NOT EXISTS nbook_role;
GRANT ROLE nbook_role TO USER cristiscu;  -- replace with your username!

grant usage on database test to role nbook_role;
grant all on schema test.public to role nbook_role;
-- grant select on table test.public.diamonds to role nbook_role;
grant all on warehouse compute_wh to role nbook_role;
grant create notebook on schema test.public to role nbook_role;
-- grant create service on schema test.public to role nbook_role;

-- ===================================================
-- (Phase 2)
show compute pools;

-- existing: SYSTEM_COMPUTE_POOL_CPU w/ CPU_X64_XS
CREATE COMPUTE POOL IF NOT EXISTS cpu5
    MIN_NODES = 1
    MAX_NODES = 5
    INSTANCE_FAMILY = CPU_X64_XS;
ALTER COMPUTE POOL cpu5 SUSPEND;
grant usage on compute pool cpu5 to role nbook_role;

-- existing: SYSTEM_COMPUTE_POOL_GPU w/ GPU_NV_S
CREATE COMPUTE POOL IF NOT EXISTS gpu5
    MIN_NODES = 1
    MAX_NODES = 5
    INSTANCE_FAMILY = GPU_NV_S;
ALTER COMPUTE POOL gpu5 SUSPEND;
grant usage on compute pool gpu5 to role nbook_role;

-- ===================================================
-- (Phase 3)
create network rule all_rule
  TYPE = HOST_PORT
  MODE = EGRESS
  VALUE_LIST = ('0.0.0.0:443', '0.0.0.0:80');   -- HTTP/HTTPS
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION all_eai
  ALLOWED_NETWORK_RULES = (all_rule)
  ENABLED = true;
GRANT USAGE ON INTEGRATION all_eai TO ROLE nbook_role;

CREATE OR REPLACE NETWORK RULE pip_rule
  TYPE = HOST_PORT
  MODE = EGRESS
  VALUE_LIST = ('pypi.org', 'pypi.python.org', 'pythonhosted.org',  'files.pythonhosted.org');
CREATE OR REPLACE EXTERNAL ACCESS INTEGRATION pip_eai
  ALLOWED_NETWORK_RULES = (pip_rule)
  ENABLED = true;
GRANT USAGE ON INTEGRATION pip_eai TO ROLE nbook_role;
