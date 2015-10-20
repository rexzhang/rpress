#!/bin/bash

#activate virtualenv
source vent/bin/activate

# Replace these three settings.
PROJECT_DIR="/home/rex/rpress"
FLASK_DIR="$PROJECT_DIR/rpress"
PIDFILE="$PROJECT_DIR/rPress.pid"
SOCKET="$PROJECT_DIR/rPress.sock"

# remove pidfile
cd $PROJECT_DIR
if [ -f $PIDFILE ]; then
    kill `cat $PIDFILE`
    rm -f -- $PIDFILE
fi

# start program
cd $FLASK_DIR
gunicorn -D -b unix:$SOCKET --pid $PIDFILE --log-level warning --log-file $PROJECT_DIR/log/gunicorn.log 'rpress:create_app(config_name="release")'
chmod 777 $SOCKET

#deactivate virtualenv
deactivate
