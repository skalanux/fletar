FROM python:3.11
WORKDIR /app

COPY ./app app
RUN pip3 install -r app/requirements.txt


EXPOSE 8000
