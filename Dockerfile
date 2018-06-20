FROM python:3

COPY ./requirements /deploy/app/requirements
COPY ./requirements.txt /deploy/app/requirements.txt
RUN pip install -r /deploy/app/requirements.txt

COPY ./rpress /deploy/app/rpress

COPY ./migrations /deploy/app/migrations
COPY ./manage.py /deploy/app/manage.py

WORKDIR /deploy/app
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", ":5000", "rpress:app"]
