USE ROLE SYSADMIN;
USE test.public;

-- ======================================================
-- this can be executed as a SQL script (w/ Snowflake CLI or SnowSQL)
CREATE STAGE IF NOT EXISTS stage1 directory = (enable=true);
PUT file://.\specs\job1_spec.yml @stage1/specs overwrite=true auto_compress=false;
PUT file://.\specs\job1_template.yml @stage1/specs overwrite=true auto_compress=false;
PUT file://.\specs\service1_spec.yml @stage1/specs overwrite=true auto_compress=false;
PUT file://.\specs\service1_template.yml @stage1/specs overwrite=true auto_compress=false;

-- ======================================================
-- for a job service
EXECUTE JOB SERVICE
    IN COMPUTE POOL cpu1
    FROM SPECIFICATION $$
        spec:
          containers:
          - name: job1c
            image: /test/public/repo/job1
    $$
    NAME=job1;
EXECUTE JOB SERVICE
    IN COMPUTE POOL cpu1
    FROM @stage1 SPECIFICATION_FILE='specs/job1_spec.yml'
    NAME=job2;

EXECUTE JOB SERVICE
    IN COMPUTE POOL cpu1
    FROM SPECIFICATION_TEMPLATE $$
        spec:
          containers:
          - name: {{ container_name | default('job1c') }}
            image: {{ image_name | default('/test/public/repo/job1') }}    $$
    USING (container_name =>'job1c', image_name=>'/test/public/repo/job1')
    NAME=job3;

EXECUTE JOB SERVICE
    IN COMPUTE POOL cpu1
    FROM @stage1 SPECIFICATION_TEMPLATE_FILE='specs/job1_template.yml'
    USING (container_name =>'job1c', image_name=>'/test/public/repo/job1')
    NAME=job4;

-- ======================================================
-- for a long-running service
CREATE SERVICE service1
    IN COMPUTE POOL cpu1
    FROM SPECIFICATION $$
        spec:
          containers:
          - name: service1c
            image: /test/public/repo/service1
            env:
              VAR1: val1
              VAR2: val2
          endpoints:
          - name: ep1
            port: 8000
            public: true
    $$
    MIN_INSTANCES=1
    MAX_INSTANCES=1;

CREATE SERVICE service2
    IN COMPUTE POOL cpu1
    FROM @stage1 SPECIFICATION_FILE='specs/service1_template.yml'
    MIN_INSTANCES=1
    MAX_INSTANCES=1;
ALTER SERVICE service2
    FROM @stage1 SPECIFICATION_FILE='specs/service1_template.yml';

CREATE SERVICE service3
    IN COMPUTE POOL cpu1
    FROM SPECIFICATION_TEMPLATE $$
        spec:
          containers:
          - name: service1c
            image: /test/public/repo/service1
            env: {{env_values}}
          endpoints:
          - name: ep1
            port: {{ port_number }}
            public: true
    $$
    USING (port_number=>'8000', env_values=>'{"VAR1": val1, "VAR2": val2}')
    MIN_INSTANCES=1
    MAX_INSTANCES=1;
ALTER SERVICE service3
    FROM @stage1 SPECIFICATION_TEMPLATE_FILE='specs/service1_template.yml'
    USING (port_number=>'8000', env_values=>'{"VAR1": val1, "VAR2": val2}');
