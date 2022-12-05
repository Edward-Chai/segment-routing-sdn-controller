import paramiko
import logging

LOG = logging.getLogger('ryu.app.iproute2_utils')
LOG.setLevel(logging.INFO)

class iproute2_utils(object):

    # clientInfo = {
    #     "hostname": None,
    #     "port": None,
    #     "username": None,
    #     "password": None
    # }

    clientInfoList = []

    def insert_srv6_rule_local(self, command):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname='131.113.71.192', port=22, username='root', password='Zhaizehua960929')
        stdin, stdout, stderr = ssh.exec_command('ps -ef | grep test')
        print(stdout.read().decode())
        ssh.close()

    def __init__(self, **kwagrs):
        super(iproute2_utils, self).__init__()

        ssh_configs = open("ssh_clients", "r")
        ssh_config = ssh_configs.readline()
        while ssh_config:
            configs = ssh_config.split('\t')
            clientinfo = {
                "hostname": configs[0],
                "port": configs[1],
                "username": configs[2],
                "password": configs[3]
            }
            self.clientInfoList.append(clientinfo)
            print("client info loaded:", clientinfo)
        print("client info all loaded:", self.clientInfoList)

