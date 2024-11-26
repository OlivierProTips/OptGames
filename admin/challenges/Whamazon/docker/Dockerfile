FROM python:3.11-alpine

RUN apk update --no-cache && apk add --no-cache socat

WORKDIR /challenge
COPY app/main.py .
USER nobody

ENTRYPOINT ["socat", "-dd", "TCP-LISTEN:80,reuseaddr,fork", "exec:python -u /challenge/main.py"]