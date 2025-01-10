REM run these one by one in a terminal
docker images

REM ===================================================
REM tag + push images to Docker Hub (check then)
docker login

docker tag repo1:job1 cristiscu/repo1:job1
docker push cristiscu/repo1:job1

docker tag repo1:service1 cristiscu/repo1:service1
docker push cristiscu/repo1:service1

REM ===================================================
REM tag + push images to Snowflake
docker login yictmgu-xtractpro-std.registry.snowflakecomputing.com -u cristiscu

docker tag repo1:job1 yictmgu-xtractpro-std.registry.snowflakecomputing.com/test/public/repo/job1
docker push yictmgu-xtractpro-std.registry.snowflakecomputing.com/test/public/repo/job1

docker tag repo1:service1 yictmgu-xtractpro-std.registry.snowflakecomputing.com/test/public/repo/service1
docker push yictmgu-xtractpro-std.registry.snowflakecomputing.com/test/public/repo/service1

REM ===================================================
REM delete some images?
docker images
docker rmi 4ad9
docker images

docker rmi cristiscu/repo1:job1
docker rmi cristiscu/repo1:service1
