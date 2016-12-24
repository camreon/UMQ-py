FROM python:3.5

ADD . /web

RUN pip install -r requirements.txt
WORKDIR ./web
CMD web: python app.py
