FROM python:3

COPY . /app
COPY ./rpress/config/docker.py /app/rpress/config/running.py

# develop env only
#RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install -r /app/requirements.txt
RUN rm -rf /root/.cache/pip

WORKDIR /app
EXPOSE 5000

CMD script/fix-host-docker-internal-at-linux.sh && gunicorn rpress:app --worker-class gevent -u nobody -b :5000
