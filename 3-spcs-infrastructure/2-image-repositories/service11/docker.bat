REM run these one by one in a terminal

docker login yictmgu-xtractpro-std.registry.snowflakecomputing.com -u cristiscu

docker build --rm --platform linux/amd64 -t service11 .

docker images

docker run -d -p 8000:8000 service11

docker tag service11 yictmgu-xtractpro-std.registry.snowflakecomputing.com/test/public/repo/service11

docker push yictmgu-xtractpro-std.registry.snowflakecomputing.com/test/public/repo/service11

docker stop service11
