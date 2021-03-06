#  from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient

def createSSHClient(server, port, user, password):
    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(AutoAddPolicy())

    client.connect(
            server,
            port,
            user,
            password)
    return client
