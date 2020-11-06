#!/usr/bin/python3

import threading
import json
import logging
import paramiko
import argparse
from time import sleep
from prometheus_client import start_http_server
from prometheus_client.core import REGISTRY, CounterMetricFamily
from datetime import datetime
from re import finditer, sub

data = ''
ALIAS = "alias"
HOST = "host"
HOSTS = "hosts"
USER_NAME = "user"
USER_PASSWORD = "password"
DELAY_TIME = "delay"
PORT = "port"
RX_PACKETS = 'rx_packets'
TX_PACKETS = 'tx_packets'
RX_BYTES = 'rx_bytes'
TX_BYTES = 'tx_bytes'
RX_ERRORS = 'rx_errors'
TX_ERRORS = 'tx_errors'
RX_DROPS = 'rx_drops'
TX_DROPS = 'tx_drops'
RX_FRAME_ERR = 'rx_frame_err'
RX_OVER_ERR = 'rx_over_err'
RX_CRC_ERR = 'rx_crc_err'
COLLISIONS = 'collisions'
NODE_NAME = 'node_name'
DEVICE = 'device'
DESCRIPTION = 'Custom metrics'

class Collector(object):
    def __init__(self, alias_name=''):
        self.alias_name = alias_name
        self.log = logging.getLogger(alias_name)
        self.log.addHandler(logging.StreamHandler())
        self.log.setLevel(logging.INFO)

    def collect(self):
        # metric list to be exposed
        metrics = {
            TX_PACKETS: CounterMetricFamily(TX_PACKETS, DESCRIPTION, labels=[NODE_NAME, DEVICE]),
            RX_PACKETS: CounterMetricFamily(RX_PACKETS, DESCRIPTION, labels=[NODE_NAME, DEVICE]),
            RX_BYTES: CounterMetricFamily(RX_BYTES, DESCRIPTION, labels=[NODE_NAME, DEVICE]),
            TX_BYTES: CounterMetricFamily(TX_BYTES, DESCRIPTION, labels=[NODE_NAME, DEVICE]),
            RX_ERRORS: CounterMetricFamily(RX_ERRORS, DESCRIPTION, labels=[NODE_NAME, DEVICE]),
            TX_ERRORS: CounterMetricFamily(TX_ERRORS, DESCRIPTION, labels=[NODE_NAME, DEVICE]),
            RX_DROPS: CounterMetricFamily(RX_DROPS, DESCRIPTION, labels=[NODE_NAME, DEVICE]),
            TX_DROPS: CounterMetricFamily(TX_DROPS, DESCRIPTION, labels=[NODE_NAME, DEVICE]),
            RX_FRAME_ERR: CounterMetricFamily(RX_FRAME_ERR, DESCRIPTION, labels=[NODE_NAME, DEVICE]),
            RX_OVER_ERR: CounterMetricFamily(RX_OVER_ERR, DESCRIPTION, labels=[NODE_NAME, DEVICE]),
            RX_CRC_ERR: CounterMetricFamily(RX_CRC_ERR, DESCRIPTION, labels=[NODE_NAME, DEVICE]),
            COLLISIONS: CounterMetricFamily(COLLISIONS, DESCRIPTION, labels=[NODE_NAME, DEVICE])
        }
        # Regex (Regular Expression) allows us to find and group the parts of the content that meet certain rules.
        # The finditer in the re library scans left-to-right, and matches are returned in the order found
        # As a result, key and value are obtained with match.group(1) and match.group(2).
        # Also, finditer saves time and memory. To see how the regex expression reacts to the .prom file content
        # check the link : regex101.com/r/biJY82/3
        # This regex expression finds "key = value" strings and groups them.
        # "[]" matches a single character present in the set such [\w. ].
        # "\w" matches any word character (equal to [a-zA-Z0-9_]).
        # "+" matches between one and unlimited times, as many times as possible, giving back as needed (greedy).
        # "\s" matches any whitespace character (equal to [\r\n\t\f\v ]).
        # (?!word|word|..) matches the words in the set.
        regex = r"\s(?!mac|config|state|speed)(\w+)\s=\s([\w.]+)"
        # logs the output data from switch
        self.save_output()
        try:
            matches = finditer(regex, data)
            port = 'port'
            for match in matches:
                key = match.group(1)
                value = match.group(2)
                if key == 'index':
                    port = 'port%s' % value
                # otherwise, it writes the metrics in the .prom file
                else:
                    metrics[key].add_metric([self.alias_name, port], float(value))
            for _ in metrics:
                yield metrics[_]
        except Exception as e:
            connect_error_msg1 = 'Regex Error:'
            self.save_log(connect_error_msg1, data)
            self.save_log(connect_error_msg1, e)
            self.log.info('%s %s' %(connect_error_msg1, e))

    # save_log, to record the error that occurs in the functions
    def save_log(self, err_msg1, err_msg2):
        try:
            error_log_file = open('/get-of-metrics/logs/regex_errors_%s.log' % self.alias_name, 'a+')
            error_log_file.write('%s %s %s\n' % (str(datetime.now()), err_msg1, err_msg2))
        finally:
            error_log_file.close()

    # save_output to record the last output from switch
    def save_output(self):
        try:
            output_log_file = open('/get-of-metrics/logs/output_log_%s.log' % self.alias_name, 'w+')
            output_log_file.write('%s:\n%s\n' % (str(datetime.now()), data))
        finally:
            output_log_file.close()

# parse_args function allows us to control the script and get the parameters in commandline
def parse_args():
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument("-t", dest=DELAY_TIME, required=False, help="<Optional> Enter a delay time. Every time "
                                                                           "it waits for the next scraping. Default "
                                                                           "value is 5 seconds ",
                               default=5, type=float)
    argument_parser = argparse.ArgumentParser(
        description="This Python script enables to scrape and parse the scaled data from Broadcom switches for "
                    "Prometheus and Node Exporter. Based on github.com/Broadcom-Switch/of-dpa. "
                    "Saves the files as _*alias_name*_.prom and in specified directory or if not "
                    "specified the directory, the same directory where the script placed. "
                    "Host Name, Host HOST, Username and User Password must be entered to run the script "
                    "It has a time delay to wait for the next scraping and default delay is 5 seconds "
                    "The directory must be created before the script run. Because Node Exporter will read the "
                    "directory you defined in the Node Exporter config file.", parents=[parent_parser])
    argument_parser.add_argument("-a", dest=ALIAS, required=True, help="<Required> Enter a alias name",
                                 type=str)
    argument_parser.add_argument("-i", dest=HOST, required=True, help="<Required> Enter a host ip or host name",
                                 type=str)
    argument_parser.add_argument("-u", dest=USER_NAME, required=True, help="<Required> Enter the root username",
                                 type=str)
    argument_parser.add_argument("-p", dest=USER_PASSWORD, required=True,
                                 help="<Required> Enter the user password",
                                 type=str)

    args = vars(argument_parser.parse_args())
    return args

class GetMetrics:
    def __init__(self, alias_name, ip, user_name, user_password, delay_time):
        self.alias_name = alias_name
        self.ip = ip
        self.user_name = user_name
        self.user_password = user_password
        self.delay_time = delay_time
        self.ssh = paramiko.SSHClient()
        self.log = logging.getLogger(alias_name)
        self.log.addHandler(logging.StreamHandler())
        self.log.setLevel(logging.INFO)

    # connect function, to establish connection and reconnection. If in the first connection, an error occurs script
    # will stop running. If the connection lost while script running. It tries to reconnect with 60 seconds intervals.
    # set_connect is set to 1 to say this is the first connection. With this way, if connection lost, it will enter
    # the reconnection phase while the script running.
    def connect(self, set_connect):
        status_code = 3
        try:
            # in reconnection, close the session
            if set_connect == 0:
                self.log.info("Connection manually closed")
                self.ssh.close()
            # connects to the server via ssh
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.ip, username=self.user_name, password=self.user_password)
        except paramiko.AuthenticationException:
            connect_error_msg1 = 'Connect Error: Failed to connect'
            connect_error_msg2 = 'due to wrong username/password'
            self.log.info("Failed to connect to %s due to wrong username/password" % self.ip)
            status_code = 1
            self.ssh.close()
        except Exception as e:
            self.log.info('Not connected to %s' % self.ip)
            connect_error_msg1 = 'Connect Error:'
            connect_error_msg2 = str(e)
            self.ssh.close()
            if set_connect == 1:
                status_code = 1
            else:
                status_code = 0
                connect_error_msg1 = 'Reconnect Error:'
                self.log.info("Server is down. Reconnecting...")
                sleep(60)
        finally:
            if status_code == 1:
                self.save_log(connect_error_msg1, connect_error_msg2)
                exit(status_code)
            elif status_code == 0: 
                self.save_log(connect_error_msg1, connect_error_msg2) 
            else:
                if set_connect == 1:
                    self.log.info("Connected to %s" % self.ip)
                    self.log.info("Scraping the metrics has been initialized...")
                elif set_connect == 0:
                    self.log.info("Reconnected")

    # collect function, executing the shell code and extracting the output
    def collect(self, set_connect):
        SHELL_CODE = 'client_port_table_dump --stats'
        try:
            # the data is in std_out
            std_in, std_out, std_err = self.ssh.exec_command(SHELL_CODE, timeout=10)
            # wait for the given time, and it is important that we have to put the delay here to get the data
            # https://stackoverflow.com/a/32758464/14091937
            sleep(self.delay_time)
            # if exit_status is 0, it means command executed successfully
            if (out := ''.join(std_out.readlines())) != "None": 
                return out
            # if not, there is a problem.
            else:
                err = ''.join(std_err.readlines())
                connect_error_msg1 = 'Collect Error: %s' % str(err)
                connect_error_msg2 = 'stdError Return Code'
                self.save_log(connect_error_msg1, connect_error_msg2)
        except Exception as e:
            connect_error_msg1 = 'Collect Error:'
            connect_error_msg2 = str(e)
            self.save_log(connect_error_msg1, connect_error_msg2)
            # reconnection
            self.connect(0)

    # save_log, to record the error that occurs in the functions
    def save_log(self, err_msg1, err_msg2):
        try:
            error_log_file = open('/get-of-metrics/logs/errors_%s.log' % self.alias_name, 'a+')
            error_log_file.write('%s %s %s\n' % (str(datetime.now()), err_msg1, err_msg2))
        finally:
            error_log_file.close()

    # execute function to execute the all the function in the exact order and checks the connection and output
    def execute(self):
        global data
        self.connect(1)
        # constantly registers the metrics constantly and works in their own threads
        REGISTRY.register(Collector(self.alias_name))
        while True:
            data = self.collect(0)
            sleep(self.delay_time)

# the main function to execute the all the function in the exact order and checks the connection and output
if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(8080)
    connection_list = parse_args()
    GetMetrics(connection_list[ALIAS], connection_list[HOST], connection_list[USER_NAME], \
        connection_list[USER_PASSWORD], connection_list[DELAY_TIME]).execute()