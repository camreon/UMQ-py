FROM p0bailey/docker-flask
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python app/app.py
