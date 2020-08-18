from prometheus_client.core import REGISTRY
from systemd.journal import JournalHandler
import logging
from time import sleep
from datetime import datetime
import paramiko
import familyofmetrics

data = ''


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
        # checks if the connection is alive if not tries to reconnect
        if self.ssh.get_transport().is_active():
            # constantly registers the metrics constantly and works in their own threads
            REGISTRY.register(familyofmetrics.RxPacket(self.alias_name))
            REGISTRY.register(familyofmetrics.TxPacket(self.alias_name))
            REGISTRY.register(familyofmetrics.RxBytes(self.alias_name))
            REGISTRY.register(familyofmetrics.TxBytes(self.alias_name))
            REGISTRY.register(familyofmetrics.RxErrors(self.alias_name))
            REGISTRY.register(familyofmetrics.TxErrors(self.alias_name))
            REGISTRY.register(familyofmetrics.RxDrops(self.alias_name))
            REGISTRY.register(familyofmetrics.TxDrops(self.alias_name))
            REGISTRY.register(familyofmetrics.RxFrameErrors(self.alias_name))
            REGISTRY.register(familyofmetrics.RxOverErrors(self.alias_name))
            REGISTRY.register(familyofmetrics.RxCrcErrors(self.alias_name))
            REGISTRY.register(familyofmetrics.Collisions(self.alias_name))
            while True:
                data = self.collect(1)
                sleep(self.delay_time)
        else:
            self.log.info("Server is down. Reconnecting...")
            self.connect(0)
