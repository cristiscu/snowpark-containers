-- see https://docs.snowflake.com/en/developer-guide/snowpark-container-services/additional-considerations-services-jobs#configuring-network-egress

CREATE OR REPLACE NETWORK RULE network_rule -- ~open-up ports in firewall
  TYPE = HOST_PORT MODE = EGRESS
  VALUE_LIST = ('translation.googleapis.com'); -- not working, use OpenAI instead

CREATE EXTERNAL ACCESS INTEGRATION access_integration
  ALLOWED_NETWORK_RULES = (network_rule, ...)
  ENABLED = true;

CREATE SERVICE eai_service
  IN COMPUTE POOL my_pool
  EXTERNAL_ACCESS_INTEGRATIONS = (access_integration, ...)
FROM SPECIFICATION $$
  spec:
    containers:
      - name: main
        image: /db/schema/repo/my_service:tutorial
        env:
          TEST_FILE_STAGE: source_stage/test_file
        args:
          - read_secret.py
    endpoints:
      - name: read
        port: 8080
$$;
