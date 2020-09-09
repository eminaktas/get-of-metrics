#!/usr/bin/python3

import threading
import json
import logging
import paramiko
from time import sleep
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
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
DEVICE = 'device'
DESCRIPTION = 'Custom metrics'
THREAD_DESCRIPTION = 'Custom metric thread'
ALLOW = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'


class Collector(object):
    def __init__(self, alias_name=''):
        self.alias_name = alias_name
        # replaces the alias name with '_' for every none allow character.
        self.node_name = sub('[^%s]' % ALLOW, '_', alias_name).lower()

    def collect(self):
        # metric list to be exposed
        metrics = {
            RX_PACKETS: GaugeMetricFamily('%s_%s' % (RX_PACKETS, self.node_name), DESCRIPTION, labels=[DEVICE]),
            TX_PACKETS: GaugeMetricFamily('%s_%s' % (TX_PACKETS, self.node_name), DESCRIPTION, labels=[DEVICE]),
            RX_BYTES: GaugeMetricFamily('%s_%s' % (RX_BYTES, self.node_name), DESCRIPTION, labels=[DEVICE]),
            TX_BYTES: GaugeMetricFamily('%s_%s' % (TX_BYTES, self.node_name), DESCRIPTION, labels=[DEVICE]),
            RX_ERRORS: GaugeMetricFamily('%s_%s' % (RX_ERRORS, self.node_name), DESCRIPTION, labels=[DEVICE]),
            TX_ERRORS: GaugeMetricFamily('%s_%s' % (TX_ERRORS, self.node_name), DESCRIPTION, labels=[DEVICE]),
            RX_DROPS: GaugeMetricFamily('%s_%s' % (RX_DROPS, self.node_name), DESCRIPTION, labels=[DEVICE]),
            TX_DROPS: GaugeMetricFamily('%s_%s' % (TX_DROPS, self.node_name), DESCRIPTION, labels=[DEVICE]),
            RX_FRAME_ERR: GaugeMetricFamily('%s_%s' % (RX_FRAME_ERR, self.node_name), DESCRIPTION, labels=[DEVICE]),
            RX_OVER_ERR: GaugeMetricFamily('%s_%s' % (RX_OVER_ERR, self.node_name), DESCRIPTION, labels=[DEVICE]),
            RX_CRC_ERR: GaugeMetricFamily('%s_%s' % (RX_CRC_ERR, self.node_name), DESCRIPTION, labels=[DEVICE]),
            COLLISIONS: GaugeMetricFamily('%s_%s' % (COLLISIONS, self.node_name), DESCRIPTION, labels=[DEVICE])
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
        # (?=word|word|..) matches the words in the set.
        regex = r"\s(?!mac|config|state|speed)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, data)
        port = 'port'
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            else:
                metrics[key].add_metric([port], float(value))
        for _ in metrics:
            yield metrics[_]


class GetMetrics:
    def __init__(self, alias_name, ip, user_name, user_password, delay_time):
        self.alias_name = alias_name
        self.ip = ip
        self.user_name = user_name
        self.user_password = user_password
        self.delay_time = delay_time
        self.ssh = paramiko.SSHClient()
        self.log = logging.getLogger(ip)
        self.log.addHandler(logging.StreamHandler())
        self.log.setLevel(logging.INFO)

    # connect function, to establish connection and reconnection. If in the first connection, an error occurs script
    # will stop running. If the connection lost while script running. It tries to reconnect with 60 seconds intervals.
    # set_connect is set to 1 to say this is the first connection. With this way, if connection lost, it will enter
    # the reconnection phase while the script running.
    def connect(self, set_connect):
        status_code = 0
        connect_error_msg1 = None
        connect_error_msg2 = None
        try:
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.ip, username=self.user_name, password=self.user_password)
            self.log.info("Connected to %s" % self.ip)
        except paramiko.AuthenticationException:
            connect_error_msg1 = 'Connect Error: Failed to connect'
            connect_error_msg2 = 'due to wrong username/password'
            self.log.info("Failed to connect to %s due to wrong username/password" % self.ip)
            status_code = 1
        except Exception as e:
            self.log.info('Not connected to %s' % self.ip)
            connect_error_msg1 = 'Connect Error:'
            connect_error_msg2 = str(e)
            if set_connect == 1:
                status_code = 2
            else:
                connect_error_msg1 = 'Reconnect Error:'
                sleep(60)
        finally:
            if status_code != 0:
                self.save_log(connect_error_msg1, connect_error_msg2)
                exit(status_code)

    # collect function, executing the shell code and extracting the output
    def collect(self, set_connect):
        SHELL_CODE = 'client_port_table_dump --stats'
        try:
            # the data is in std_out
            std_in, std_out, std_err = self.ssh.exec_command(SHELL_CODE)
            exit_status = std_out.channel.recv_exit_status()
            # if exit_status is 0, it means everything is ok
            if exit_status == 0:
                out = ''.join(std_out.readlines())
                return str(out)
            # if not, there is a problem.
            else:
                err = ''.join(std_err.readlines())
                exit_status_error = std_err.channel.recv_exit_status()
                connect_error_msg1 = 'Collect Error: %s' % str(err)
                connect_error_msg2 = 'stdError Return Code: %s' % str(exit_status_error)
                connect_error_msg3 = 'stdOut Return Code: %s' % str(exit_status)
                self.save_log(connect_error_msg1, connect_error_msg2)
                self.save_log(connect_error_msg1, connect_error_msg3)
                pass
        except Exception as e:
            connect_error_msg1 = 'Collect Error:'
            connect_error_msg2 = str(e)
            self.save_log(connect_error_msg1, connect_error_msg2)
            self.connect(set_connect)

    # save_log, to record the error that occurs in the functions
    def save_log(self, err_msg1, err_msg2):
        error_log_file = None
        try:
            error_log_file = open('/var/log/get-of-metrics/errors_%s.log' % self.alias_name, 'a+')
            error_log_file.write('%s %s %s\n' % (str(datetime.now()), err_msg1, err_msg2))
        finally:
            error_log_file.close()

    # execute function to execute the all the function in the exact order and checks the connection and output
    def execute(self):
        global data
        self.connect(1)
        # checks if the connection is alive if not tries to reconnect
        if self.ssh.get_transport().is_active():
            # constantly registers the metrics constantly and works in their own threads
            REGISTRY.register(Collector(self.alias_name))
            while True:
                data = self.collect(1)
                sleep(self.delay_time)
        else:
            self.log.info("Server is down. Reconnecting...")
            self.connect(0)


# the main function to execute the all the function in the exact order and checks the connection and output
if __name__ == "__main__":
    log_connection = logging.getLogger('Connection Info')
    log_connection.addHandler(logging.StreamHandler())
    log_connection.setLevel(logging.INFO)
    with open('/home/get-of-metrics/connection-parameters.json', 'r+') as json_file:
        connection_objects = json.load(json_file)
        json_file.close()
    # Start up the server to expose the metrics.
    start_http_server(int(connection_objects[PORT]))
    _time = float(connection_objects[DELAY_TIME])
    connection_list = connection_objects[HOSTS]
    thread_len = len(connection_list)
    for j in connection_list:
        _alias = j[ALIAS]
        _host = j[HOST]
        _user = j[USER_NAME]
        _psw = j[USER_PASSWORD]
        c = GetMetrics(_alias, _host, _user, _psw, _time)
        thread = threading.Thread(name=('%s %s(%s)' % (THREAD_DESCRIPTION, _alias, _host)), target=c.execute)
        thread.start()
    log_connection.info('After 60 seconds, it shows a message for number of connection established')
    sleep(60)
    while True:
        number_of_thread = 0
        for k in threading.enumerate():
            if k.name.startswith(THREAD_DESCRIPTION):
                number_of_thread = number_of_thread + 1
        log_connection.info('%s connection has been established out of %s' % (number_of_thread, thread_len))
        sleep(1800)
