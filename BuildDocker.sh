docker container stop rpress
docker container rm rpress

docker pull python:3
docker build -t ray1ex/rpress .
docker rmi -f $(docker images -qa -f "dangling=true")
