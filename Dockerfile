FROM tiangolo/uwsgi-nginx-flask:python3.6

ENV LISTEN_PORT 8080
EXPOSE 8080

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app
