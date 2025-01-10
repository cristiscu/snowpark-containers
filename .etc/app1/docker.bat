REM run these one by one in a terminal

REM build and test local image
docker build --rm --platform linux/amd64 -t repo1:app1 .
docker run -it -p 8000:8000 repo1:app1

REM tag + push image to Docker Hub
docker login
docker tag repo1:app1 cristiscu/repo1:app1
docker push cristiscu/repo1:app1

REM delete all containers and some images
docker container prune
docker images
docker rmi 4ad9