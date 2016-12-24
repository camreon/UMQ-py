FROM python:3.5

RUN pip install -r requirements.txt
CMD web: python app.py
