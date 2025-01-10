REM see https://hub.docker.com/r/jupyter/datascience-notebook/tags (8.31 GB!)

docker pull jupyter/datascience-notebook:x86_64-ubuntu-22.04

docker images

docker login -u cristiscu yictmgu-xtractpro-std.registry.snowflakecomputing.com

docker tag jupyter/datascience-notebook:x86_64-ubuntu-22.04 yictmgu-xtractpro-std.registry.snowflakecomputing.com/test2/public/repo2/jupyter:v1

docker push yictmgu-xtractpro-std.registry.snowflakecomputing.com/test2/public/repo2/jupyter:v1

REM cleanup (save almost 17 GB!)

docker rmi yictmgu-xtractpro-std.registry.snowflakecomputing.com/test2/public/repo2/jupyter:v1

docker rmi jupyter/datascience-notebook:x86_64-ubuntu-22.04
