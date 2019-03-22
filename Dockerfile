FROM python:3

COPY . /deploy/app

RUN pip install -r /deploy/app/requirements.txt
RUN rm -rf /root/.cache/pip

WORKDIR /deploy/app
EXPOSE 5000

CMD script/fix-host-docker-internal-at-linux.sh && gunicorn rpress:app --worker-class gevent -u nobody -b :5000
