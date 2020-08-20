# get-of-metrics.py

Get of Metrics version 2

## Overview

get-of-metrics is a Python script for dealing the Broadcom switch metrics to extract the metrics from command line, parse the metrics and create a *.prom file for metrics to be processed by Node Exporter, Prometheus. Finally, visualize the metrics with Grafana.

In this version, used Docker Compose to run Node Exporter, Prometheus, Grafana and the script.

## Documentation

Detailed installation can be found at installation.docx

## Installation

Python 3.7 and above need to be installed.

paramiko and systemd need to be installed.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install 

```bash
pip install paramiko
pip install systemd
```

## Usage

## Required commands and information for creation and installation dpkg/apt

Step - 1 `dpkg/apt`

Creating and copying required files and folders for installation

```bash
mkdir ./get-of-metrics
mkdir ./get-of-metrics/DEBIAN
mkdir ./get-of-metrics/usr
mkdir ./get-of-metrics/usr/bin
mkdir ./get-of-metrics/etc
mkdir ./get-of-metrics/etc/systemd
mkdir ./get-of-metrics/etc/systemd/system
mkdir ./get-of-metrics/home/get-of-metrics
mkdir ./get-of-metrics/home/get-of-metrics/prom-files
mkdir ./get-of-metrics/var
mkdir ./get-of-metrics/var/log
mkdir ./get-of-metrics/var/log/get-of-metrics
cp ./get-of-metrics.py ./get-of-metrics/usr/bin
```

The contents of the files are available in the ./get-of-metrics/DEBIAN and ./get-of-metrics/etc/systemd/system folder.

```bash
vi ./get-of-metrics/etc/systemd/system
vi ./get-of-metrics/DEBIAN/prerm
vi ./get-of-metrics/DEBIAN/control
```

Regulates the privileges of created prerm. If it is not edited, it may fail while creating .deb.

```bash
chmod 775 ./get-of-metrics/DEBIAN/prerm
```

Creates a deb file for installation.

```bash
dpkg-deb --build get-of-metrics
```

"get-of-metrics.deb" file already provided. So you don't have to go through all the steps above.

Performs installation.

```bash 
apt install ./get-of-metrics.deb
```

Performs uninstallation.

```bash
apt remove get-of-metrics
```

Required parameters to introduce machines in the setup. Use "connection-parameters.json" file to intruduce the remote machines and the delay time.

## Docker Compose
Step - 2 `Docker`

Docker Compose is provided in the file named `docker-compose.yml`.

Builds and runs the docker compose. 

```bash
docker-compose -f 
```

Getting acces to containers

```bash
docker exec -it custom-metrics sh
docker exec -it grafana sh
docker exec -it prometheus sh
docker exec -it node-exporter sh
```
