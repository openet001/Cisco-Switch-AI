# Cisco-Switch-AI
A tool application that automatically connects to Cisco switches via SSH and outputs configuration and logs. An intelligent network assistant that combines analysis with the domestic Qianwen big model.  
一个SSH自动连接思科交换机并输出配置和Log的工具应用。并结合国内千问大模型进行分析的智能网络助手。
# How to use 使用方法   
install python 3.11 or above  
From https://python.org 

I use windows 10 professinal test OK.
 
pip install -r requirements.txt.txt

get a API key from https://bailian.console.aliyun.com/ 
# Set your  DASHSCOPE_API_KEY 
in DOS command 
set set DASHSCOPE_API_KEY=You-qwen-API-key

or in Linux bash:
export DASHSCOPE_API_KEY *****

# RUN
D:test-py>python main.py

# UI images
in images directionary 

# BUG 
已实现的功能： 可以ssh登录思科交换机，取交换机配置， 可以调用千问大模型 对配置 进行 分析。 
目前已知问题：telnet 由于python 3.11以上版本 已认为不安全，我在测试中不断出错，只好放弃了telnet登录，  2. 显示show running-config不全， ， 欢迎大家提供建议
