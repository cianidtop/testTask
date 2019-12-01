FROM python:3
ENV PYTHONUNBUFFERED 1
ADD ./testTask /app
WORKDIR ./app

RUN pip install -r requirements.txt

