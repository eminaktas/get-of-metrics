FROM python:3-slim

LABEL mainainer="Emin Aktas<eminaktas34@gmail.com>"
LABEL version="3.0.0"
LABEL description="Get of Metrics Docker Image for get-of-metrics Exporter"

WORKDIR /get-of-metrics

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./get-of-metrics.py ./

COPY ./connection-parameters.json ./

CMD [ "python", "-u", "./get-of-metrics.py"]
     
EXPOSE 8000