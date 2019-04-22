FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --upgrade

COPY . /app/
COPY umq/static /app/umq/static/
