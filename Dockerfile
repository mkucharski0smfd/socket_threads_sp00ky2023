FROM python:3.8.6
WORKDIR /socket_threads
COPY Backend/src/main/python/socket_threads .
CMD [ "python", "./backendServer.py" ]
