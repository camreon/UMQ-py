FROM python:3.5-onbuild
ADD . /UMQ
WORKDIR /UMQ
RUN pip install -r requirements.txt
CMD web: gunicorn UMQ.wsgi:app
