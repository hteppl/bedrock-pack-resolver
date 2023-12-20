FROM python:3.11-slim-bookworm

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

ADD requirements.txt /source/requirements.txt
RUN pip3 install -r requirements.txt

ENTRYPOINT cd /source/ && python3 main.py