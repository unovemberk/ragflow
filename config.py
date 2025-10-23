import os

# MySQL数据库配置
MYSQL_CONFIG = {
    "host": "192.168.35.22",
    "port": 3306,
    "user": "root",
    "password": "123456",
    "database": "rag_chat_db",
    "echo": True
}

# 底层服务地址配置
SERVICE_CONFIG = {
    "ragflow": {
        "base_url": "http://192.168.29.130:8000",
        "knowledge_base_id": "d734b0e8af1d11f0bcb2cef0f93a59bc"  # Ragflow知识库ID
    },
    "ollama": {
        "base_url": "http://192.168.35.22:11434",
        "default_model": "qwen:7b-chat"  # Ollama模型名
    },
    "xinference": {
        "base_url": "http://192.168.35.22:9997",
        "default_model": "baichuan2"  # Xinference模型名
    }
}

# 接口前缀
API_PREFIX = "/api/v1"