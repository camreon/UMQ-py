FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app/
COPY umq/static /app/umq/static/

# run without cache everytime
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN pip install --upgrade youtube-dl
