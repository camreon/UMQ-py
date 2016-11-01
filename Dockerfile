FROM p0bailey/docker-flask
ADD . /UMQ
WORKDIR /UMQ
RUN pip install -r requirements.txt
CMD python runserver.py
