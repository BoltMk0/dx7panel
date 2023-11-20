FROM python:3.10

WORKDIR /app
COPY . ./server
RUN apt update && apt install build-essential libasound2-dev libjack-dev -y
RUN python3 -m pip install websockets rtmidi python-rtmidi pygame

CMD python3 -m server
