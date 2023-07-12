FROM python:3.8.17-slim-bookworm

RUN apt-get update && apt-get install -y ffmpeg

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY src/main.py /app/src/
COPY src/cogs /app/src/cogs/

WORKDIR /app/src

VOLUME /app/src/config

CMD ["python", "main.py"]
