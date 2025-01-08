-- execute one by one in a SQL Worksheet, in a commercial Snowflake account
use role accountadmin;
use test.public;

-- check that the previous image has been uploaded
show images in image repository repo;

-- =========================================================
-- (1) create EAI for egress HTTP/HTTPS calls to google.com
CREATE OR REPLACE NETWORK RULE google_search_rule
    TYPE = HOST_PORT
    MODE = EGRESS
    VALUE_LIST = ('google.com:80', 'google.com:443');

CREATE EXTERNAL ACCESS INTEGRATION google_search_integration
    ALLOWED_NETWORK_RULES = (google_search_rule)
    ENABLED = true;

-- ======================================================
-- (2) grant access to SYSADMIN
grant read on image repository repo to role sysadmin;
grant usage, operate on compute pool cpu to role sysadmin;
grant usage on integration google_search_integration to role sysadmin;

use role sysadmin;

-- ======================================================
-- (3) create and run job service
EXECUTE JOB SERVICE
    IN COMPUTE POOL cpu
    NAME = google_search_job
    EXTERNAL_ACCESS_INTEGRATIONS = (google_search_integration)
    FROM SPECIFICATION $$
      spec:
        container:
        - name: curl
          image: /test/public/repo/alpine-curl
          command:
          - "curl"
          - "http://google.com/"
    $$;

-- ======================================================
-- (4) cleanup
alter compute pool cpu suspend;
describe compute pool cpu;
