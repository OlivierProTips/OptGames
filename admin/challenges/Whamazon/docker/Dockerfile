FROM python:3.11-slim

RUN apt update && apt install socat -y

WORKDIR /challenge
COPY app/main.py .
USER nobody

ENTRYPOINT ["socat", "-dd", "TCP-LISTEN:80,reuseaddr,fork", "exec:python -u /challenge/main.py"]