FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app/
COPY ./umq/static/ /app/static/
