import paramiko
import time
import re
import os

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
        
        # 禁用分页并设置终端宽度
        chan.send('terminal length 0\n')
        time.sleep(0.5)
        chan.send('terminal width 300\n')
        time.sleep(0.5)
        
        # 清空缓冲区
        while chan.recv_ready():
            chan.recv(9999)
        
        self.connected = True

    def send_command(self, command):
        if not self.connected:
            raise Exception("未连接到设备")

        chan = self.conn.invoke_shell()
        chan.send(command + '\n')
        
        output = ""
        start_time = time.time()
        while True:
            if chan.recv_ready():
                chunk = chan.recv(9999).decode()
                output += chunk
                
                # 自动翻页（兼容多种分页提示符）
                if re.search(r'--[\s\-]*more[\s\-]*--', chunk, re.IGNORECASE):
                    chan.send(' ')
                    time.sleep(0.5)
                
                start_time = time.time()  # 重置计时器
            elif time.time() - start_time > 5:  # 等待 5 秒后无新数据，视为结束
                break
            else:
                time.sleep(0.1)
        
        # 过滤 ANSI 转义码（如颜色控制）
        ansi_escape = re.compile(r'\x1B$$[0-9;]*[A-Za-z]')
        output = ansi_escape.sub('', output)
        
        return output

    def get_running_config(self):
        return self.send_command("show running-config")

    def get_logging(self):
        return self.send_command("show logging")

    def get_interface_status(self):
        return self.send_command("show interface status")

    def get_cdp_neighbors(self):
        return self.send_command("show cdp neighbors")
