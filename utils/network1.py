import paramiko
import time

class SwitchManager:
    def __init__(self):
        self.connected = False
        self.conn = None
        self.ip = None

    def connect(self, ip, method, username, password, enable_pwd):
        self.ip = ip
        if method.lower() != 'ssh':
            raise ValueError("仅支持 SSH 连接方式")
        self._connect_ssh(ip, username, password, enable_pwd)

    def _connect_ssh(self, ip, username, password, enable_pwd):
        self.conn = paramiko.SSHClient()
        self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.conn.connect(ip, username=username, password=password)
        
        chan = self.conn.invoke_shell()
        chan.send('enable\n')
        time.sleep(1)
        chan.send(enable_pwd + '\n')
        time.sleep(1)
        chan.send('terminal length 0\n')
        time.sleep(1)
        chan.recv(9999)  # 清空缓冲区
        self.connected = True

    def send_command(self, command):
        if not self.connected:
            raise Exception("未连接到设备")
            
        # 强制使用 SSH 连接
        chan = self.conn.invoke_shell()
        chan.send(command + '\n')
        time.sleep(2)
        output = chan.recv(9999).decode()
        while self._has_more_output(chan):
            output += chan.recv(9999).decode()
        return output

    def _has_more_output(self, chan):
        import select
        return chan.recv_ready()

    def get_running_config(self):
        return self.send_command("show running-config")

    def get_logging(self):
        return self.send_command("show logging")

    def get_interface_status(self):
        return self.send_command("show interface status")

    def get_cdp_neighbors(self):
        return self.send_command("show cdp neighbors")
