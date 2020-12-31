FROM python:3.8.6
WORKDIR /socket_threads
COPY src/ .
CMD [ "python", "./server.py" ]
