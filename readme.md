# get-of-metrics.py

Get of Metrics version 2

## Overview

get-of-metrics is a Python script for dealing the Broadcom switch metrics to extract the metrics from command line, parse the metrics and create a *.prom file for metrics to be processed by Node Exporter, Prometheus. Finally, visualize the metrics with Grafana.

This version include automated installation for Python script, Node Exporter, Prometheus and Grafana installation within Dockerfile.

Required parameters to introduce machines in the setup. Use "connection-parameters.json" file to intruduce the remote machines and the delay time.

## Installation

Dockerfile is provided in the file named `Dockerfile`. By using the docker file you can create the docker image.

Builds the docker image. 

```bash
docker build -t get-of-metrics .
```
Runs the image.

`-d` runs as a deamon.
`--name` names the script.
`--privileged` gives access to all deviced. Needed to activate the service in conatiner otherwise it does not work.
`-v` in order to save, access and modify the datas.
At the last of the command we give the image name which is `get-of-metrics`

```bash
docker run -d --name get-of-metrics --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v ./file:/home/get-of-metrics -v ./logs:/var/log/get-of-metrics -v ./prom-files:/home/get-of-metrics/prom-files get-of-metrics
```

Getting acces to container

```bash
docker exec -it get-of-metrics bash
```

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

## Required commands and information for creation and installation dpkg/apt (Note: get-of-metrics.deb package is already provided in the files)

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
