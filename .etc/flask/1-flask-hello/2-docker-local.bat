REM start Docker Desktop, then execute one by one in a Terminal window, in the app/ folder

docker build --rm -t hello_image:local .

REM check at http://127.0.0.1:8000/
docker run -d -p 8000:8000 hello_image:local

docker ps

REM replace with container ID returned by docker run
docker stop b6a25af41503adbed3ded3487a57d8bc3fc1218cb3935df00ab3d343c7f64d8b

docker ps

docker ps --all

docker system prune

docker ps --all
