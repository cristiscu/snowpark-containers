REM start Docker Desktop, then execute one by one in a Terminal window, in the app/ folder

REM see https://hub.docker.com/r/alpine/curl
docker pull alpine/curl

REM open the generated search.html file in a browser
docker run --rm alpine/curl -fsSL https://www.google.com/ > search.html

REM update with your actual repository path
docker tag alpine/curl yictmgu-xtractpro-std.registry.snowflakecomputing.com/test/public/repo/alpine-curl

docker login yictmgu-xtractpro-std.registry.snowflakecomputing.com -u cristiscu

docker push yictmgu-xtractpro-std.registry.snowflakecomputing.com/test/public/repo/alpine-curl
