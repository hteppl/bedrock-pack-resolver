FROM python:3.11-slim-bookworm

ADD requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ADD source/* /
WORKDIR ./
ENTRYPOINT python3 main.py