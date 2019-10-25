# rPress
A multi-site and multi-user blog system.


## Deploy

create deploy settings file
```shell script
mkdir rpress_settings
cd rpress_settings
cp deploy/docker/setting/__init__.py rpress_settings
```

create and start docker container
```shell script
docker pull ray1ex/rpress
export RPRESS_SETTINGS="rpress_settings"
./scrpit/RestartDocker.sh
```

## Develop

create develop settings file
```shell script
cp rpress/config/running.py.sample rpress/config/running.py
```

run develop server
```shell script
./manage.py run
```
