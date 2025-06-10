import dashscope
from dashscope import Generation
import os

class AIAssistant:
    def __init__(self):
        # 从环境变量或 GUI 输入中获取 API 密钥
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("请设置 DASHSCOPE_API_KEY 环境变量或通过界面输入 API 密钥")
        dashscope.api_key = self.api_key

    def get_analysis(self, prompt):
        prompt += "\n请提供以下内容：\n"
        prompt += "1. 配置优化建议\n"
        prompt += "2. 日志中的错误分析\n"
        prompt += "3. 安全加固建议\n"
        prompt += "4. 性能优化方案"
        return self._call_qwen(prompt)

    def get_response(self, query):
        return self._call_qwen(query)

    def _call_qwen(self, prompt):
        try:
            response = Generation.call(
                model="qwen-max",  # 可选：qwen-plus, qwen-turbo 等
                prompt=prompt
            )
            return response.output.text
        except Exception as e:
            return f"调用 Qwen 模型失败：{str(e)}"
