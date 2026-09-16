from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, message_to_dict, messages_from_dict
import os
import json



def get_history(session_id):
    return FileChatMessageHistory(session_id,'./history')

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self, session_id: str, storage_path: str):
        self.session_id = session_id
        self.storage_path = storage_path
        # 拼接文件完整路径
        self.file_path = os.path.join(self.storage_path, self.session_id)
        # 创建父目录，存在则不报错
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

    @property
    def messages(self) -> list[BaseMessage]:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                message_data = json.load(f)
                return messages_from_dict(message_data)
        except FileNotFoundError:
            return []


    def add_messages(self, messages: list[BaseMessage]) -> None:
        """批量添加消息，合并原有消息并写入文件"""
        # 获取已有消息
        all_messages = list(self.messages)
        # 新消息追加到列表
        all_messages.extend(messages)
        # BaseMessage对象转字典列表
        new_messages = [message_to_dict(msg) for msg in all_messages]
        # 写入json文件
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(new_messages, f, ensure_ascii=False, indent=2)

    def clear(self) -> None:
        """清空该会话的历史。"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([], f)


