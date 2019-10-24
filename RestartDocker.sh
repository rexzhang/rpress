docker container stop rpress
docker container rm rpress

docker run -dit -p 127.0.0.1:5000:5000 -v /Users/rex/TEMP/rpress-settings/:/app/rpress/config/settings --name rpress --restart unless-stopped ray1ex/rpress
