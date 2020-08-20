#!/usr/bin/python3

from datetime import datetime
from time import sleep
from re import finditer
from systemd.journal import JournalHandler
import paramiko
import threading
import logging
import json

ALIAS = "alias"
HOST = "host"
USER_NAME = "user"
USER_PASSWORD = "password"
DELAY_TIME = "delay"


class GetMetrics:
    def __init__(self, alias_name, ip, user_name, user_password, delay_time):
        self.alias_name = alias_name
        self.ip = ip
        self.user_name = user_name
        self.user_password = user_password
        self.directory = '/home/get-of-metrics/prom-files/'
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

    # collect function, executing the shellcode and extracting the output
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

    # parse function, to parse the output and save parsed output in .prom file
    def parse(self, data):
        connect_error_msg1 = None
        connect_error_msg2 = None
        status_code = False
        prom_file = 0
        try:
            prom_file = open('%s_%s_.prom' % (self.directory, self.alias_name), 'w+')
            # HELP is important to be able to see the metrics on the node_exporter's metric page.
            prom_file.write('# HELP rx_packets reads the metrics from files\n'
                            '# HELP tx_packets reads the metrics from files\n'
                            '# HELP rx_bytes reads the metrics from files\n'
                            '# HELP tx_bytes reads the metrics from files\n'
                            '# HELP rx_errors reads the metrics from files\n'
                            '# HELP tx_errors reads the metrics from files\n'
                            '# HELP rx_drops reads the metrics from file\n'
                            '# HELP tx_drops reads the metrics from file\n'
                            '# HELP rx_frame_err reads the metrics from file\n'
                            '# HELP rx_over_err reads the metrics from file\n'
                            '# HELP rx_crc_err reads the metrics from file\n'
                            '# HELP collisions reads the metrics from file\n')
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
            # (?!word|word|..) does not match the words in the set.
            regex = r"\s(?!mac|config|state|speed)(\w+)\s=\s([\w.]+)"
            matches = finditer(regex, data)
            port = 'port'
            # parses the data key is for metric name and value is the metric value
            for match in matches:
                key = match.group(1)
                value = match.group(2)
                # if true, it will update the index value
                if key == 'index':
                    port = 'port%s' % value
                # otherwise, it writes the metrics in the .prom file
                else:
                    prom_file.write('%s{node_name="%s",device="%s"} %s\n' % (key, self.alias_name, port, value))
        except FileNotFoundError:
            self.log.info("The directory doesn't exist: %s" % self.directory)
            connect_error_msg1 = "Parse Error: The directory doesn't exist: %s." % self.directory
            connect_error_msg2 = "It must be already created and should be pointed to Node Exporter"
            status_code = 1
        except PermissionError:
            self.log.info("The user doesn't have the permission to interfere the filesystem")
            connect_error_msg1 = "The user doesn't have the permission to interfere the filesystem"
            connect_error_msg2 = ""
            status_code = 2
        except Exception as e:
            connect_error_msg1 = 'Parse Error:'
            connect_error_msg2 = str(e)
            status_code = 3
        finally:
            prom_file.close()
            if status_code != 0:
                self.save_log(connect_error_msg1, connect_error_msg2)
                exit(status_code)

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
        self.connect(1)
        while 1:
            # checks if the connection is alive if not tries to reconnect
            if self.ssh.get_transport().is_active():
                output_data = self.collect(1)
                # double check for the output_data if it is empty or not
                if output_data is not None:
                    self.parse(output_data)
                    sleep(self.delay_time)
                else:
                    pass
            else:
                self.log.info("Server is down. Reconnecting...")
                self.connect(0)


# the main function to execute the all the function in the exact order and checks the connection and output
if __name__ == "__main__":
    log_connection = logging.getLogger('Connection Info')
    log_connection.addHandler(JournalHandler())
    log_connection.setLevel(logging.INFO)
    HOSTS = 'hosts'
    with open('/home/get-of-metrics/connection-parameters.json', 'r+') as jsonfile:
        connection_objects = json.load(jsonfile)
        jsonfile.close()
    _time = float(connection_objects[DELAY_TIME])
    connection_list = connection_objects[HOSTS]
    thread_len = len(connection_list)
    for j in connection_list:
        _alias = j[ALIAS]
        _host = j[HOST]
        _user = j[USER_NAME]
        _psw = j[USER_PASSWORD]
        c = GetMetrics(_alias, _host, _user, _psw, _time)
        thread = threading.Thread(name=('%s(%s)' % (_alias, _host)), target=c.execute)
        thread.start()
    sleep(60)
    number_of_run = 0
    while 1:
        number_of_run = 0
        for k in threading.enumerate():
            if 'Thread' == k.__class__.__name__:
                number_of_run = number_of_run + 1
        log_connection.info('%s connection has been established out of %s' % (number_of_run, thread_len))
        sleep(600)
