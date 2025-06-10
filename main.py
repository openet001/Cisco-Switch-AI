import tkinter as tk
from tkinter import ttk, messagebox
from utils.network import SwitchManager
from utils.ai_helper import AIAssistant
import threading

class NetworkAIGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("智能网络设备管理系统")
        self.root.geometry("1200x800")
        
        # 初始化模块
        self.switch_manager = SwitchManager()
        self.ai_assistant = AIAssistant()
        
        self.create_widgets()
        self.load_switches()

    def create_widgets(self):
        # 主框架
        main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧面板（交换机列表）
        left_frame = ttk.Frame(main_frame)
        main_frame.add(left_frame, weight=2)
        
        ttk.Label(left_frame, text="交换机列表").pack(pady=5)
        self.switch_listbox = tk.Listbox(left_frame)
        self.switch_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.switch_listbox.bind('<<ListboxSelect>>', self.on_switch_select)

        # 中间面板（设备信息）
        mid_frame = ttk.Frame(main_frame)
        main_frame.add(mid_frame, weight=3)
        
        ttk.Label(mid_frame, text="设备信息").pack(pady=5)
        self.device_info = tk.Text(mid_frame, wrap=tk.NONE)
        self.device_info.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 右侧面板（AI助手）
        right_frame = ttk.Frame(main_frame)
        main_frame.add(right_frame, weight=3)
        
        ttk.Label(right_frame, text="AI智能助手").pack(pady=5)
        
        self.ai_input = tk.Entry(right_frame)
        self.ai_input.pack(fill=tk.X, padx=5, pady=5)
        self.ai_input.bind('<Return>', self.on_ai_query)
        
        self.ai_output = tk.Text(right_frame, wrap=tk.WORD)
        self.ai_output.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 按钮框架
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(btn_frame, text="连接设备", command=self.connect_device).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="获取配置", command=self.get_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="获取日志", command=self.get_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="AI分析", command=self.analyze_with_ai).pack(side=tk.LEFT, padx=5)

    def load_switches(self):
        try:
            with open('swlist.txt', 'r') as f:
                for line in f:
                    if line.strip():
                        self.switch_listbox.insert(tk.END, line.strip())
        except FileNotFoundError:
            messagebox.showerror("错误", "未找到交换机列表文件swlist.txt")

    def on_switch_select(self, event):
        selection = self.switch_listbox.curselection()
        if selection:
            self.selected_switch = self.switch_listbox.get(selection[0])
            self.update_device_info()

    def update_device_info(self):
        self.device_info.delete(1.0, tk.END)
        self.device_info.insert(tk.END, f"已选设备：{self.selected_switch}\n")
        self.device_info.insert(tk.END, "状态：等待连接...\n")

    def connect_device(self):
        if not hasattr(self, 'selected_switch'):
            messagebox.showwarning("警告", "请先选择一个交换机")
            return
            
        thread = threading.Thread(target=self._connect_thread)
        thread.start()

    def _connect_thread(self):
        try:
            switch_info = self.selected_switch.split(',')
            ip, method, user, pwd, enable = switch_info
            self.switch_manager.connect(ip, method, user, pwd, enable)
            self.root.after(100, lambda: self.device_info.insert(tk.END, "连接成功！\n"))
        except Exception as e:
            self.root.after(100, lambda: messagebox.showerror("连接失败", str(e)))

    def get_config(self):
        if not self.switch_manager.connected:
            messagebox.showwarning("警告", "请先连接设备")
            return
            
        thread = threading.Thread(target=self._get_config_thread)
        thread.start()

    def _get_config_thread(self):
        config = self.switch_manager.get_running_config()
        self.root.after(100, lambda: self.device_info.insert(tk.END, "当前配置：\n" + config[:200] + "...\n"))

    def get_logs(self):
        if not self.switch_manager.connected:
            messagebox.showwarning("警告", "请先连接设备")
            return
            
        thread = threading.Thread(target=self._get_logs_thread)
        thread.start()

    def _get_logs_thread(self):
        logs = self.switch_manager.get_logging()
        self.root.after(100, lambda: self.device_info.insert(tk.END, "最新日志：\n" + logs[:200] + "...\n"))

    def analyze_with_ai(self):
        if not self.switch_manager.connected:
            messagebox.showwarning("警告", "请先连接设备")
            return
            
        prompt = "请分析以下网络设备信息并提供优化建议：\n"
        prompt += "1. 运行配置\n" + self.switch_manager.get_running_config()[:1000] + "\n"
        prompt += "2. 最新日志\n" + self.switch_manager.get_logging()[:1000] + "\n"
        
        thread = threading.Thread(target=self._ai_analysis_thread, args=(prompt,))
        thread.start()

    def _ai_analysis_thread(self, prompt):
        response = self.ai_assistant.get_analysis(prompt)
        self.root.after(100, lambda: self.ai_output.insert(tk.END, response + "\n"))

    def on_ai_query(self, event):
        user_query = self.ai_input.get()
        if user_query:
            thread = threading.Thread(target=self._ai_query_thread, args=(user_query,))
            thread.start()
            self.ai_input.delete(0, tk.END)

    def _ai_query_thread(self, query):
        response = self.ai_assistant.get_response(query)
        self.root.after(100, lambda: self.ai_output.insert(tk.END, f"Q: {query}\nA: {response}\n\n"))

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkAIGUI(root)
    root.mainloop()
