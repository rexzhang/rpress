#!/usr/bin/env bash

docker build -t ray1ex/rpress .
docker rmi -f $(docker images -qa -f "dangling=true")

docker run -dit -p 127.0.0.1:10000:5000 --restart unless-stopped ray1ex/rpress
