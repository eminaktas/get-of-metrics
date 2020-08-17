#!/usr/bin/python3

from datetime import datetime
from time import sleep
from re import finditer
from systemd.journal import JournalHandler
import paramiko
import threading
import json
from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY

data = ''
ALIAS = "alias"
HOST = "host"
USER_NAME = "user"
USER_PASSWORD = "password"
DELAY_TIME = "delay"


class RxPacket(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=rx_packets|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, data)
        port = 'port'
        metric = GaugeMetricFamily('rx_packets', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_packets':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class TxPacket(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=tx_packets|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, data)
        port = 'port'
        metric = GaugeMetricFamily('tx_packets', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'tx_packets':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class RxBytes(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=rx_bytes|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, data)
        port = 'port'
        metric = GaugeMetricFamily('rx_bytes', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_bytes':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class TxBytes(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=tx_bytes|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, data)
        port = 'port'
        metric = GaugeMetricFamily('tx_bytes', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'tx_bytes':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class RxErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=rx_errors|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, data)
        port = 'port'
        metric = GaugeMetricFamily('rx_errors', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_errors':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class TxErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=tx_errors|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, data)
        port = 'port'
        metric = GaugeMetricFamily('tx_errors', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'tx_errors':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class RxDrops(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=rx_drops|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, data)
        port = 'port'
        metric = GaugeMetricFamily('rx_drops', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_drops':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class TxDrops(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=tx_drops|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, data)
        port = 'port'
        metric = GaugeMetricFamily('tx_drops', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'tx_drops':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class RxFrameErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=rx_frame_err|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, data)
        port = 'port'
        metric = GaugeMetricFamily('rx_frame_err', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_frame_err':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class RxOverErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=rx_over_err|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, data)
        port = 'port'
        metric = GaugeMetricFamily('rx_over_err', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_over_err':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class RxCrcErrors(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=rx_crc_err|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, data)
        port = 'port'
        metric = GaugeMetricFamily('rx_crc_err', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'rx_crc_err':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class Collisions(object):
    def __init__(self, alias_name):
        self.alias_name = alias_name

    def collect(self):
        regex = r"\s(?=collisions|index)(\w+)\s=\s([\w.]+)"
        matches = finditer(regex, data)
        port = 'port'
        metric = GaugeMetricFamily('collisions', 'Custom metrics', labels=['node_name', 'device'])
        for match in matches:
            key = match.group(1)
            value = match.group(2)
            # if true, it will update the index value
            if key == 'index':
                port = 'port%s' % value
            # otherwise, it writes the metrics in the .prom file
            elif key == 'collisions':
                metric.add_metric([self.alias_name, port], value)
        yield metric


class GetMetrics:
    def __init__(self, alias_name, ip, user_name, user_password, delay_time):
        self.alias_name = alias_name
        self.ip = ip
        self.user_name = user_name
        self.user_password = user_password
        self.delay_time = delay_time
        self.ssh = paramiko.SSHClient()
        self.log = logging.getLogger(ip)
        self.log.addHandler(JournalHandler())
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
        while 1:
            # checks if the connection is alive if not tries to reconnect
            if self.ssh.get_transport().is_active():
                # registers the metrics constantly and
                REGISTRY.register(RxPacket(self.alias_name))
                REGISTRY.register(TxPacket(self.alias_name))
                REGISTRY.register(RxBytes(self.alias_name))
                REGISTRY.register(TxBytes(self.alias_name))
                REGISTRY.register(RxErrors(self.alias_name))
                REGISTRY.register(TxErrors(self.alias_name))
                REGISTRY.register(RxDrops(self.alias_name))
                REGISTRY.register(TxDrops(self.alias_name))
                REGISTRY.register(RxFrameErrors(self.alias_name))
                REGISTRY.register(RxOverErrors(self.alias_name))
                REGISTRY.register(RxCrcErrors(self.alias_name))
                REGISTRY.register(Collisions(self.alias_name))
                while True:
                    data = self.collect(1)
                    sleep(1)
            else:
                self.log.info("Server is down. Reconnecting...")
                self.connect(0)


# the main function to execute the all the function in the exact order and checks the connection and output
if __name__ == "__main__":
    # Start up the server to expose the metrics.
    start_http_server(8000)
    log_connection = logging.getLogger('Connection Info')
    log_connection.addHandler(JournalHandler())
    log_connection.setLevel(logging.INFO)
    with open('/home/get-of-metrics/connection-parameters.json', 'r+') as json_file:
        connection_objects = json.load(json_file)
    thread_len = len(connection_objects)
    for j in connection_objects:
        _alias = j[ALIAS]
        _host = j[HOST]
        _user = j[USER_NAME]
        _psw = j[USER_PASSWORD]
        c = GetMetrics(_alias, _host, _user, _psw, _time)
        thread = threading.Thread(name=('%s(%s)' % (_alias, _host)), target=c.execute())
        thread.start()
    sleep(60)
    number_of_run = 0
    while True:
        number_of_thread = 0
        for k in threading.enumerate():
            if 'Thread' == k.__class__.__name__:
                number_of_run = number_of_run + 1
        log_connection.info('%s connection has been established out of %s' % (number_of_thread, thread_len))
        sleep(6000)
