#!/usr/bin/python3

from time import sleep
from systemd.journal import JournalHandler
import threading
import json
from prometheus_client import start_http_server
import getmetrics
import logging

data = ""
ALIAS = "alias"
HOST = "host"
HOSTS = "hosts"
USER_NAME = "user"
USER_PASSWORD = "password"
DELAY_TIME = "delay"
PORT = "port"


# the main function to execute the all the function in the exact order and checks the connection and output
if __name__ == "__main__":
    log_connection = logging.getLogger('Connection Info')
    log_connection.addHandler(JournalHandler())
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
        c = getmetrics.GetMetrics(_alias, _host, _user, _psw, _time)
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
