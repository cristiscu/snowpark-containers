-- see https://docs.snowflake.com/en/developer-guide/snowpark-container-services/tutorials/advanced/tutorial-4-block-storage#introduction
USE ROLE SYSADMIN;
USE test.public;

SHOW IMAGES IN IMAGE REPOSITORY repo;

-- =========================================================
-- (1) create service w/ block volume
CREATE SERVICE sb1
    IN COMPUTE POOL cpu1
    FROM SPECIFICATION $$
spec:
  containers:
  - name: echo
    image: /test/public/repo/service1
    volumeMounts:
    - name: block-vol1
      mountPath: /opt/block/path
    readinessProbe:
      port: 8080
      path: /healthcheck
  endpoints:
  - name: echoendpoint
    port: 8080
    public: true
  volumes:
  - name: block-vol1
    source: block
    size: 10Gi
$$;
DESC SERVICE sb1;
SHOW SERVICE CONTAINERS IN SERVICE sb1;

-- =========================================================
-- (2) take snapshop from block volume
CREATE SNAPSHOT snapshot1
    FROM SERVICE sb1
    VOLUME "block-vol1"
    INSTANCE 0;
DESC SNAPSHOT snapshot1;
SHOW SNAPSHOTS;

-- =========================================================
-- create another service w/ block volume
CREATE SERVICE sb2
    IN COMPUTE POOL cpu1
    FROM SPECIFICATION $$
spec:
  containers:
  - name: echo
    image: /test/public/repo/service1
    volumeMounts:
    - name: fromsnapshotvol
      mountPath: /opt/block/path
    readinessProbe:
      port: 8080
      path: /healthcheck
  endpoints:
  - name: echoendpoint
    port: 8080
    public: true
  volumes:
  - name: fromsnapshotvol
    source: block
    size: 50Gi
    blockConfig:
      initialContents:
        fromSnapshot: snapshot1
$$
    min_instances=3
    max_instances=3;

-- =========================================================
-- replace block volume from saved snapshot + resume service
ALTER SERVICE sb2 SUSPEND;
ALTER SERVICE sb2 RESTORE
    VOLUME "block-vol1"
    INSTANCES 0
    FROM SNAPSHOT snapshot1;
DESC SERVICE sb2;
DROP SNAPSHOT snapshot1;

-- =========================================================
-- cleanup

DROP SERVICE sb1;
DROP SERVICE sb2;

ALTER COMPUTE POOL cpu1 STOP ALL;
