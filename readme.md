# get-of-metrics.py

Get of Metrics version 3

## Overview

get-of-metrics is a Python script for dealing the Broadcom switch metrics to extract from commandline, parse the metrics and expose them to be processed by Prometheus and Grafana.

This version works as an Prometheus Exporter.

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

Step - 1 dpkg/apt

Creating and copying required files and folders for installation

```bash
mkdir ./get-of-metrics
mkdir ./get-of-metrics/DEBIAN
mkdir ./get-of-metrics/usr
mkdir ./get-of-metrics/usr/bin
mkdir ./get-of-metrics/usr/bin/get-of-metrics
mkdir ./get-of-metrics/etc
mkdir ./get-of-metrics/etc/systemd
mkdir ./get-of-metrics/etc/systemd/system
mkdir ./get-of-metrics/home/get-of-metrics
mkdir ./get-of-metrics/home/get-of-metrics/prom-files
mkdir ./get-of-metrics/var
mkdir ./get-of-metrics/var/log
mkdir ./get-of-metrics/var/log/get-of-metrics
cp ./get-of-metrics.py ./get-of-metrics/usr/bin/get-of-metrics
cp ./familyofmetrics.py ./get-of-metrics/usr/bin/get-of-metrics
cp ./getmetrics.py ./get-of-metrics/usr/bin/get-of-metrics
```

The contents of the files are available in the ./get-of-metrics/DEBIAN folder and ./get-of-metrics/etc/systemd/systemd/get-of-metrics.service.

```bash
vi ./get-of-metrics/etc/systemd/systemd/get-of-metrics.service
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

Required parameters to introduce machines in the setup. Use `connection-parameters.json` file to intruduce the remote machines and the delay time.

Step - 2 Docker

Dockerfile is provided in the file named `Dockerfile`. By using the docker file you can make create the docker image.

Builds the docker image. 

```bash
docker build -t get-of-metrics .
```
Runs the image.
`-d` runs as a deamon.
`--name` names the script.
`--privileged` gives access to all deviced. Needed to activate the service in conatiner otherwise it does not work.
`-v` in order to save, access and modify the datas.
`-p` expose the port to the port number on the left.
At the last of the command we give the image name which is `get-of-metrics`

```bash
docker run -d --name get-of-metrics --privileged -p 8000:8000 -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v ./file:/home/get-of-metrics -v ./logs:/var/log/get-of-metrics -v ./prom-files:/home/get-of-metrics/prom-files get-of-metrics
```

Getting acces to container

```bash
docker exec -it get-of-metrics bash
```
Useful control mechanisim for the script in the container.

Tracking the life cycle of get-of-metrics service

```bash
systemctl status get-of-metrics
```

Clears recorded logs. 

```bash
journalctl --vacuum-time=2d
```

Access to logs. -u access to our daemon log entries. -b shows us the entries from the last boot.

```bash
journalctl -b -u get-of-metrics
```