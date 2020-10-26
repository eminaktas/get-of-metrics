FROM python:3-slim

ENV ALIAS=default-alias
ENV HOST=default-host
ENV USER=default-user
ENV PASSWORD=default-password
ENV DELAY=1

LABEL mainainer="Emin Aktas<eminaktas34@gmail.com>"
LABEL version="1.0.0"
LABEL description="Get of Metrics Docker Image for get-of-metrics script"

WORKDIR /get-of-metrics

RUN mkdir ./logs

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt

COPY ./get-of-metrics.py ./

VOLUME [ "/get-of-metrics/logs" ]

CMD python3 ./get-of-metrics.py -a $ALIAS -i $HOST -u $USER -p $PASSWORD -t $DELAY