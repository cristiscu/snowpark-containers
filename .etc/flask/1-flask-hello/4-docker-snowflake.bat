REM execute one by one in a Terminal window, in the app/ folder

REM replace with the repository_url value from your SHOW REPOSITORIES result
docker build --rm -t yictmgu-xtractpro-std.registry.snowflakecomputing.com/hello_db/public/hello_repo/hello_image .

docker login yictmgu-xtractpro-std.registry.snowflakecomputing.com -u cristiscu

docker push yictmgu-xtractpro-std.registry.snowflakecomputing.com/hello_db/public/hello_repo/hello_image
