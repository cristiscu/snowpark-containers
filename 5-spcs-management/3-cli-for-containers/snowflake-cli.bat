REM run these one by one in a Terminal window

REM docker login ...
snow spcs image-registry login -c std

REM show image repositories;
snow spcs image-repository list -c std

REM show images in image repository test.public.repo;
snow spcs image-repository list-images test.public.repo -c std

REM desc compute pool cpu1;
snow spcs compute-pool describe cpu1 -c std

REM show services;
snow spcs service list -c std

REM alter service test.public.service1 resume;
snow spcs service resume test.public.service1 -c std

REM show endpoints in service test.public.service1;
snow spcs service list-endpoints test.public.service1 -c std

REM show service instances in service test.public.service1;
snow spcs service list-instances test.public.service1 -c std

REM show service containers in service test.public.service1;
snow spcs service list-containers test.public.service1 -c std

REM show roles in service test.public.service1;
snow spcs service list-roles test.public.service1 -c std

REM alter service test.public.service1 suspend;
snow spcs service suspend test.public.service1 -c std

REM alter compute pool cpu1 suspend;
snow spcs compute-pool suspend cpu1 -c std

REM show compute pools;
snow spcs compute-pool list -c std