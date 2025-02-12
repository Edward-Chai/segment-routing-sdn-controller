"""
SRv6 Local: SID, bhvrK(action), bhvrV
SRv6 Encap: IPv6_dst, mode(encap,decap), segs_list

Test Path:
    - Shortest: 1 -> 2 -> 5 -> 6                Done!
    - SRv6(One way):     1(encap) -> 2 -> 3 -> 5 -> 6
"""

import paramiko
import logging

LOG = logging.getLogger('ryu.app.iproute2_utils')
LOG.setLevel(logging.INFO)

class iproute2_utils(object):

    clientInfo = {
        "hostname": None,
        "port": None,
        "username": None,
        "password": None
    }

    clientInfoList = []

    def insert_srv6_rule_local(self, match_fields):
        existence_flag = 0
        for count in range(len(self.clientInfoList)):
            if self.clientInfoList[count]['hostname'] == match_fields['host_ip']:
                existence_flag = 1
                self.clientInfo = self.clientInfoList[count]
        if existence_flag == 0:
            LOG.error("No host ip found!")
        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=self.clientInfo['hostname'],
                        port=self.clientInfo['port'],
                        username=self.clientInfo['username'],
                        password=self.clientInfo['password'])
            if match_fields['action'] == "encap":
                command = 'ip -6 route add '+ match_fields['seg'] + " encap seg6 mode " +match_fields['action']+ " segs " + match_fields['segs'] + " dev ens160"
                stdin, stdout, stderr = ssh.exec_command(command)
                print("stdout: ", stdout.read().decode())
                print("stdeer: ", stderr.read().decode())
            else:
                command = 'ip -6 route add '+ match_fields['seg'] + " encap seg6local action " + match_fields['action'] + " nh6 " + match_fields['params'] + " dev ens160"
                stdin, stdout, stderr = ssh.exec_command(command)
                print("stdout: ", stdout.read().decode())
                print("stdeer: ", stderr.read().decode())
            print("command: ", command)
            ssh.close()

    def __init__(self, **kwagrs):
        super(iproute2_utils, self).__init__()
        for key in self.clientInfo:
            self.clientInfo[key] = None

        ssh_configs = open("ssh_clients", "r")
        ssh_config = ssh_configs.readline()
        while ssh_config and ssh_config != '':
            configs = ssh_config.split()
            # LOG.info("Len(configs):%d, Content: ", len(configs), configs)
            clientinfo = {
                "hostname": configs[0],
                "port": configs[1],
                "username": configs[2],
                "password": configs[3].split("\n")[0]
            }
            self.clientInfoList.append(clientinfo)
            LOG.info("client info loaded:", clientinfo)
            ssh_config = ssh_configs.readline()
        ssh_configs.close()
        LOG.info("client info all loaded:", self.clientInfoList)

