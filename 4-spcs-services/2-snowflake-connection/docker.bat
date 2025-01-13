REM run these one by one in a terminal

docker build --rm --platform linux/amd64 -t sql-job .

docker run -it -e SNOWFLAKE_ACCOUNT -e SNOWFLAKE_USER -e SNOWFLAKE_PASSWORD sql-job

docker tag sql-job yictmgu-xtractpro-std.registry.snowflakecomputing.com/test/public/repo/sql-job

docker login yictmgu-xtractpro-std.registry.snowflakecomputing.com -u cristiscu

docker push yictmgu-xtractpro-std.registry.snowflakecomputing.com/test/public/repo/sql-job

docker rmi -f sql-job