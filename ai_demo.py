#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
端侧AI Demo - 客户端AI服务调用示例

功能说明：
1. 从配置文件读取AI服务的URL和密钥
2. 构建HTTP请求调用AI服务
3. 处理用户输入并获取AI响应
4. 包含错误处理和重试机制

使用方法：
1. 先编辑 config.py 文件，配置正确的url和key
2. 运行此脚本：python ai_demo.py
3. 输入问题，获取AI回答
4. 输入 'quit' 或 'exit' 退出程序

作者：AI Assistant
日期：2024
"""

import json
import time
import requests
from typing import Optional, Dict, Any

# 导入配置文件
import config


class AIClient:
    """
    AI客户端类
    
    负责与AI服务进行通信，包括：
    - 构建请求
    - 发送HTTP请求
    - 处理响应
    - 错误处理和重试
    """
    
    def __init__(self, api_url: str, api_key: str, model: str = "gpt-3.5-turbo", 
                 timeout: int = 30, max_retries: int = 3):
        """
        初始化AI客户端
        
        参数:
            api_url (str): AI服务的API地址
            api_key (str): API访问密钥
            model (str): 使用的模型名称，默认为"gpt-3.5-turbo"
            timeout (int): 请求超时时间（秒），默认30秒
            max_retries (int): 最大重试次数，默认3次
        """
        self.api_url = api_url
        self.api_key = api_key
        self.model = model
        self.timeout = timeout
        self.max_retries = max_retries
        
        # 设置请求头，包含认证信息
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # 存储对话历史，用于多轮对话
        self.conversation_history = []
    
    def _build_request_body(self, user_message: str) -> Dict[str, Any]:
        """
        构建请求体
        
        参数:
            user_message (str): 用户输入的消息
            
        返回:
            dict: 符合API要求的请求体字典
        """
        # 将用户消息添加到对话历史
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # 构建完整的请求体
        request_body = {
            "model": self.model,
            "messages": self.conversation_history,
            "temperature": 0.7,  # 控制回复的创造性，0-1之间
            "max_tokens": 1024   # 限制最大生成token数
        }
        
        return request_body
    
    def _send_request(self, request_body: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        发送HTTP请求到AI服务
        
        参数:
            request_body (dict): 请求体字典
            
        返回:
            dict or None: API响应数据，失败时返回None
        """
        try:
            # 发送POST请求
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=request_body,
                timeout=self.timeout
            )
            
            # 检查HTTP状态码
            if response.status_code == 200:
                return response.json()
            else:
                print(f"❌ 请求失败，状态码：{response.status_code}")
                print(f"错误信息：{response.text}")
                return None
                
        except requests.exceptions.Timeout:
            print("⏰ 请求超时，请检查网络连接")
            return None
        except requests.exceptions.ConnectionError:
            print("🔌 连接错误，请检查网络或API地址")
            return None
        except Exception as e:
            print(f"💥 发生未知错误：{str(e)}")
            return None
    
    def chat(self, user_message: str) -> Optional[str]:
        """
        与AI进行对话
        
        参数:
            user_message (str): 用户输入的消息
            
        返回:
            str or None: AI的回复内容，失败时返回None
        """
        # 构建请求体
        request_body = self._build_request_body(user_message)
        
        # 尝试发送请求，支持重试机制
        for attempt in range(self.max_retries):
            print(f"\n🔄 正在思考... (尝试 {attempt + 1}/{self.max_retries})")
            
            response_data = self._send_request(request_body)
            
            if response_data is not None:
                # 成功获取响应
                try:
                    # 解析AI回复内容
                    ai_response = response_data["choices"][0]["message"]["content"]
                    
                    # 将AI回复添加到对话历史
                    self.conversation_history.append({
                        "role": "assistant",
                        "content": ai_response
                    })
                    
                    return ai_response
                    
                except (KeyError, IndexError) as e:
                    print(f"⚠️ 响应格式异常：{str(e)}")
                    return None
            
            # 如果失败且还有重试机会，等待后重试
            if attempt < self.max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避：1s, 2s, 4s...
                print(f"😴 等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
        
        # 所有重试都失败
        print("❌ 所有重试都失败了，请稍后再试")
        return None
    
    def clear_history(self):
        """清空对话历史"""
        self.conversation_history = []
        print("🧹 对话历史已清空")


def print_welcome_message():
    """打印欢迎信息和使用说明"""
    print("=" * 60)
    print("🤖 端侧AI Demo - 智能对话助手")
    print("=" * 60)
    print("\n✨ 功能特点:")
    print("  • 支持多轮对话，记住上下文")
    print("  • 自动重试机制，提高稳定性")
    print("  • 友好的错误提示")
    print("\n📝 使用指南:")
    print("  • 直接输入问题与AI对话")
    print("  • 输入 'clear' 清空对话历史")
    print("  • 输入 'quit' 或 'exit' 退出程序")
    print("\n⚙️  当前配置:")
    print(f"  • API地址：{config.url}")
    print(f"  • 模型：{config.model}")
    print(f"  • 超时：{config.timeout}秒")
    print(f"  • 最大重试：{config.max_retries}次")
    print("=" * 60)


def main():
    """主函数 - 程序入口"""
    
    # 打印欢迎信息
    print_welcome_message()
    
    # 创建AI客户端实例
    # 从配置文件读取参数
    client = AIClient(
        api_url=config.url,
        api_key=config.key,
        model=config.model,
        timeout=config.timeout,
        max_retries=config.max_retries
    )
    
    # 主循环 - 持续接收用户输入
    while True:
        try:
            # 获取用户输入
            user_input = input("\n👤 您：").strip()
            
            # 检查是否为空输入
            if not user_input:
                continue
            
            # 检查退出命令
            if user_input.lower() in ['quit', 'exit']:
                print("\n👋 再见！祝您有美好的一天！")
                break
            
            # 检查清空历史命令
            if user_input.lower() == 'clear':
                client.clear_history()
                continue
            
            # 调用AI服务获取回复
            ai_response = client.chat(user_input)
            
            # 显示AI回复
            if ai_response:
                print(f"\n🤖 AI：{ai_response}")
            else:
                print("\n⚠️ 未能获取AI回复，请检查配置或网络连接")
                
        except KeyboardInterrupt:
            # 捕获Ctrl+C中断
            print("\n\n👋 程序被用户中断，再见！")
            break
        except EOFError:
            # 捕获EOF错误（如管道输入结束）
            print("\n\n👋 输入结束，程序退出")
            break


if __name__ == "__main__":
    """程序入口点"""
    main()
