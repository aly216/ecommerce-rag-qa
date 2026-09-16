# 电商商品知识库 RAG 问答系统

基于 LangChain + Chroma 的电商商品咨询「检索增强生成（RAG）」问答系统，支持多轮对话与知识库在线更新，覆盖尺码、颜色、洗涤养护等高频咨询。

## 功能

- 使用 LCEL 搭建 RAG 链（检索 → 上下文组装 → Prompt → DeepSeek → 输出解析），支持流式输出
- 基于 Chroma 实现语义检索与文本切分（chunk 1000 / overlap 100），通过 MD5 指纹去重避免重复入库
- 自定义 `FileChatMessageHistory` 实现多会话历史持久化，结合 `RunnableWithMessageHistory` 支持多轮记忆
- 双应用架构：问答端 `app.qa.py` 流式对话、管理端 `app_file_uploader.py` 文件上传增量更新，无需改代码即可扩充知识
- 基于 Streamlit 的 Web 界面

## 目录结构

```
RAG项目/
├── app.qa.py                # 问答端：Streamlit 多轮对话
├── app_file_uploader.py     # 管理端：文件上传增量更新知识库
├── rag.py                   # LCEL RAG 链 + 多轮记忆
├── knowledge_base.py        # 知识库服务（切分 + 入库 + MD5 去重）
├── vector_stores.py         # Chroma 向量库封装
├── file_history_store.py    # 自定义文件聊天历史
├── config_data.py           # 配置（模型 / 向量化 / 切分参数）
└── data/                    # 知识库文档（尺码 / 洗涤 / 颜色）
```

## 技术栈

- Python
- LangChain —— LCEL、RunnableWithMessageHistory
- Chroma —— 向量数据库；阿里云百炼 text-embedding-v3 —— 文本向量化
- DeepSeek —— 对话模型
- Streamlit —— Web 界面

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

复制 `.env.example` 为 `.env`，填入 DeepSeek 与阿里云百炼密钥：

```bash
cp .env.example .env
```

### 3. 入库知识

运行管理端，上传 `data/` 目录下的 `.txt` 文件（或你自己的商品知识文档）：

```bash
streamlit run app_file_uploader.py
```

### 4. 启动问答

```bash
streamlit run app.qa.py
```

## 注意事项

- **密钥安全**：API Key 放在 `.env` 中，已加入 `.gitignore`，请勿提交到仓库。
- **首次使用**：需先在步骤 3 入库知识，问答端才能检索到内容。
- 对话历史默认持久化到 `history/`（已 gitignore）。
