REM run these one by one in a terminal

REM ===================================================
REM build and test local image for job (check stdout)
docker build --rm --platform linux/amd64 -t repo1:job1 job1
docker run -it repo1:job1

REM ===================================================
REM build and test local image for service (check localhost:8000)
docker build --rm --platform linux/amd64 -t repo1:service1 service1
docker run -d -p 8000:8000 repo1:service1
docker ps
docker stop cd77...

REM ===================================================
REM cleanup all stopped containers
docker ps -a
docker container prune
docker ps -a