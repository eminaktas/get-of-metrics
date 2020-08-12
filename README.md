# get_of_metrics.py

Get of Metrics for Prometheus, Node Exporter and Grafana

## Overview

get_of_metrics is a Python script for dealing the Broadcom switch metrics to extract from commandline, parse the metrics and create a *.prom file to be processed by Node Exporter, Prometheus and Grafana.

## Documentation

Detailed documentation can be found at documentation.docx

## Installation

Python 3.7 and above need to be installed.

argparse, paramiko, datetime and time libraries are used in this script. argparse, datetime and time are the standart libraries paramiko need to be installed.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install 

```bash
pip install paramiko
```

## Usage

Must be entered the alias_name, host_ip, user_name, user_password and directory_path in order to run the script. delay_time is optional but if not defined its default value is 4.9 seconds assuming the Node Exporter scrape time interval is 5 seconds. directory_path and time are common for all connections

```bash
pyhton3 get_of_metrics.py -a *host_name1* *host_name2* ... -i *host_ip1* *host_ip2* ... -u *user_name1* -u *user_name2* ... -p *user_password1* *user_password2* ... -d *directory_path* -t *time(in seconds)*
```

