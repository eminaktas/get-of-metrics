from datetime import datetime
from time import sleep
from argparse import ArgumentParser
from re import finditer
import paramiko

# ssh is global variable because it is used in multiple function
ssh = paramiko.SSHClient()
# set_connect is set to 1 to say this is the first connection.
# With this way, if connection lost, it will enter the reconnection phase while the script running.
set_connect = 1


# parse_args function allows us to control the script and get the parameters in commandline
def parse_args():
    HOST_NAME = "host_name"
    IP = "host_ip"
    USER_NAME = "user_name"
    USER_PASSWORD = "user_password"
    DIRECTORY = "directory_path"
    DELAY_TIME = "delay_time"
    argument_parser = ArgumentParser(
        description="This Python script enables to scrape and parse the scaled data from Broadcom switches for "
                    "Prometheus and Node Exporter. Based on github.com/Broadcom-Switch/of-dpa. "
                    "Saves the files as _*host_name*_.prom and in specified directory or if not "
                    "specified the directory, the same directory where the script placed. "
                    "Host Name, Host IP, Username and User Password must be entered to run the script "
                    "It has a time delay to wait for the next scraping and default delay is 4.9 seconds "
                    "The directory must be created before the script run. Because Node Exporter will read the "
                    "directory you defined in the Node Exporter config file.")
    argument_parser.add_argument("-n", '--' + HOST_NAME, required=True, help="(Mandatory) Enter a host name",
                                 type=str)
    argument_parser.add_argument("-i", '--' + IP, required=True, help="(Mandatory) Enter a host ip",
                                 type=str)
    argument_parser.add_argument("-u", '--' + USER_NAME, required=True, help="(Mandatory) Enter the root username",
                                 type=str)
    argument_parser.add_argument("-p", '--' + USER_PASSWORD, required=True, help="(Mandatory) Enter the user password",
                                 type=str)
    argument_parser.add_argument("-d", '--' + DIRECTORY, required=False,
                                 help="(Optional) Enter a directory to save the file if not it saves the files in the "
                                      "same directory where script placed", default="", type=str)
    argument_parser.add_argument("-t", '--' + DELAY_TIME, required=False, help="(Optional) Enter a delay time. Every "
                                                                               "time it waits for the next scraping. "
                                                                               "Default value is 4.9 seconds ",
                                 default=4.9, type=float)

    args = vars(argument_parser.parse_args())
    return args[HOST_NAME], args[IP], args[USER_NAME], args[USER_PASSWORD], args[DIRECTORY], args[DELAY_TIME]


# connect function, to establish connection and reconnection. If in the first connection, an error occurs script will
# stop running. If the connection lost while script running. It tries to reconnect with 60 seconds intervals.
def connect(host_name, host_ip, user_name, user_password):
    status_code = 0
    connect_error_msg1 = None
    connect_error_msg2 = None
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host_ip, username=user_name, password=user_password)
        print("Connected to %s" % host_ip)
    except paramiko.AuthenticationException:
        connect_error_msg1 = 'Connect Error: Failed to connect'
        connect_error_msg2 = 'due to wrong username/password'
        print("Failed to connect to %s due to wrong username/password" % host_ip)
        status_code = 1
    except Exception as e:
        connect_error_msg1 = 'Connect Error:'
        connect_error_msg2 = str(e)
        if set_connect == 1:
            status_code = 2
        else:
            connect_error_msg1 = 'Reconnect Error:'
            sleep(60)
    finally:
        if status_code != 0:
            save_log(host_name, connect_error_msg1, connect_error_msg2)
            exit(status_code)


# collect function, executing the shellcode and extracting the output
def collect(host_name, host_ip, user_name, user_password):
    SHELL_CODE = 'client_port_table_dump --stats'
    try:
        # the data is in std_out
        std_in, std_out, std_err = ssh.exec_command(SHELL_CODE)
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
            save_log(host_name, connect_error_msg1, connect_error_msg2)
            save_log(host_name, connect_error_msg1, connect_error_msg3)
            pass
    except Exception as e:
        connect_error_msg1 = 'Collect Error:'
        connect_error_msg2 = str(e)
        save_log(host_name, connect_error_msg1, connect_error_msg2)
        connect(host_name, host_ip, user_name, user_password)


# parse function, to parse the output and save parsed output in .prom file
def parse(data, node_name, directory_path):
    connect_error_msg1 = None
    connect_error_msg2 = None
    status_code = False
    prom_file = 0
    try:
        prom_file = open('%s_%s_.prom' % (directory_path, node_name), 'w+')
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
                prom_file.write('%s{node_name="%s",device="%s"} %s\n' % (key, node_name, port, value))
        print('PROM file has been written for', node_name, datetime.now())
    except FileNotFoundError:
        print("The directory doesn't exist: %s" % directory_path)
        connect_error_msg1 = "Parse Error: The directory doesn't exist: %s." % directory_path
        connect_error_msg2 = "It must be already created and should be pointed to Node Exporter"
        status_code = 1
    except PermissionError:
        print("The user doesn't have the permission to interfere the filesystem")
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
            save_log(node_name, connect_error_msg1, connect_error_msg2)
            exit(status_code)


# save_log, to record the error that occurs in the functions
def save_log(host_name, err_msg1, err_msg2):
    error_log_file = None
    try:
        error_log_file = open('errors_%s.log' % host_name, 'a+')
        error_log_file.write('%s %s %s\n' % (str(datetime.now()), err_msg1, err_msg2))
    finally:
        error_log_file.close()


# the main function to execute the all the function in the exact order and checks the connection and output
if __name__ == "__main__":
    name, ip, u_name, u_password, path, delay_time = parse_args()
    connect(name, ip, u_name, u_password)
    while 1:
        # checks if the connection is alive if not tries to reconnect
        if ssh.get_transport().is_active():
            output_data = collect(name, ip, u_name, u_password)
            # double check for the output_data if it is empty or not
            if output_data is not None:
                parse(output_data, name, path)
                sleep(delay_time)
            else:
                pass
        else:
            set_connect = 0
            print("Server is down. Reconnecting...")
            connect(name, ip, u_name, u_password)
