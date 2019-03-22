#!/usr/bin/env bash

docker pull python:3

docker build -t ray1ex/rpress .
docker rmi -f $(docker images -qa -f "dangling=true")

docker run -dit -p 127.0.0.1:5000:5000 --restart unless-stopped ray1ex/rpress
