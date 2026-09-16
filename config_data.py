import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

# 从项目目录 .env 加载 API Key，避免在代码中硬编码
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))



md5_path='./md5.text'


#Chroma
collection_name="rag"
persist_directory='./chroma_db'


#TextSplitter
chunk_size=1000
chunk_overlap=100
separators=['\n\n','\n',' ','','。','!','?',';',',']
max_split=1000




#Retriever
similarity_threshold=1



embeddings = OpenAIEmbeddings(
    model="text-embedding-v3",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.environ.get("DASHSCOPE_API_KEY", ""),
    check_embedding_ctx_length=False,  # 关掉 token 预处理，直接发原始文本
    chunk_size=10,  # 百炼 text-embedding-v3 单次最多 10 条，分批发送
)


model = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.environ.get("DEEPSEEK_API_KEY", ""),
    base_url="https://api.deepseek.com/v1",
    temperature=0
)



session_config={
        'configurable':{
            'session_id':'user_001'
        }
    }