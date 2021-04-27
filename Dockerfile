FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /app/

# run without cache everytime
ADD "https://www.random.org/cgi-bin/randbyte?nbytes=10&format=h" skipcache
RUN pip install --upgrade youtube-dl
