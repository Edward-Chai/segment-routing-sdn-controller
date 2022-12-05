import paramiko

class iproute2_utils(object):

    clientInfo = {
        "hostname": None,
        "port": None,
        "username": None,
        "password": None
    }

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