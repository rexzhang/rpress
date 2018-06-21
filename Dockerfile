FROM python:3

COPY ./requirements /deploy/app/requirements
COPY ./requirements.txt /deploy/app/requirements.txt
RUN pip install -r /deploy/app/requirements.txt

COPY ./rpress /deploy/app/rpress

COPY ./migrations /deploy/app/migrations
COPY ./manage.py /deploy/app/manage.py
COPY ./script /deploy/app/script

WORKDIR /deploy/app
EXPOSE 5000

CMD script/fix-host-docker-internal-at-linux.sh && gunicorn -w 3 -b :5000 rpress:app
