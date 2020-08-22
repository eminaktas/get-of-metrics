# get-of-metrics.py

Get of Metrics version 1

## Overview

get-of-metrics is a Python script for dealing the Broadcom switch metrics to extract from commandline, parse the metrics and create a *.prom file to be processed by Node Exporter, Prometheus and Grafana.

## Documentation

Detailed installation documentation for Node Exporter, Prometheus and Grafana can be found at documentation.docx

## Installation

Python 3.7 and above need to be installed.

argparse, paramiko, systemd, re, threading, datetime and time libraries are used in this script. argparse, re, threading, datetime and time are the standart libraries. paramiko and systemd need to be installed.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install 

```bash
pip install paramiko
pip install systemd
```
If you install with .deb (which is already provided) package it will install all Python packages by itself.

## Usage

Must be entered the alias_name, host_ip, user_name, user_password and directory_path in order to run the script. delay_time is optional but if not defined its default value is 5 seconds assuming the Node Exporter scrape time interval is 5 seconds. directory_path and time are common for all connections

```bash
pyhton3 get_of_metrics.py -a *host_name1* *host_name2* ... -i *host_ip1* *host_ip2* ... -u *user_name1* -u *user_name2* ... -p *user_password1* *user_password2* ... -d *directory_path* -t *time(in seconds)*
```

Performs installation.

```bash 
sudo apt install ./get-of-metrics.deb
```

Performs uninstallation.

```bash
sudo apt remove get-of-metrics
```

Required parameters to introduce machines in the setup. 

```bash
alias-name1 host user-name password
alias-name2 host user-name password
alias-name3 host user-name password
```

Tracking the life cycle of get-of-metrics service

```bash
sudo systemctl status get-of-metrics
```

Clears recorded logs.

```bash
sudo journalctl --vacuum-time=2d
```

Access to logs. -u access to our daemon log entries. We say to show us the entries from the last boot with -b.

```bash
journalctl -b -u get-of-metrics
```

## Required commands and information for creation dpkg/apt

Creating and copying required files and folders for installation

```bash
sudo mkdir ./get-of-metrics
sudo mkdir ./DEBIAN
sudo mkdir ./usr
sudo mkdir ./usr/bin
sudo mkdir ./var
sudo mkdir ./var/log
sudo mkdir ./var/log/get-of-metrics
sudo cp get-of-metrics.py ./usr/bin
```

The contents of the files are available in the ./get-of-metrics/DEBIAN folder.

```bash
sudo vi ./get-of-metrics/DEBIAN/preinst
sudo vi ./get-of-metrics/DEBIAN/prerm
sudo vi ./get-of-metrics/DEBIAN/postinst
sudo vi ./get-of-metrics/DEBIAN/control
```

It regulates the privileges of created preinst, prerm and postinst files. If it is not edited, it may fail while creating .deb.

```bash
sudo chmod 775 ./get-of-metrics/DEBIAN/preinst
sudo chmod 775 ./get-of-metrics/DEBIAN/prerm
sudo chmod 775 ./get-of-metrics/DEBIAN/postinst
```

Creates a deb file for installation.

```bash
dpkg-deb --build get-of-metrics
```
