import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def check_md5(md5_str):
    if not os.path.exists(config.md5_path):
        open(config.md5_path,'w',encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path,'r',encoding='utf-8'):
            if line.strip()==md5_str:
                return True
        return False



def save_md5(md5_str):
    with open(config.md5_path,'a',encoding='utf-8') as f:
        f.write(md5_str+'\n')


def get_string_md5(str,encoding='utf-8'):
    str_bytes=str.encode(encoding)
    md5_obj=hashlib.md5()
    md5_obj.update(str_bytes)
    md5_hex=md5_obj.hexdigest()
    return md5_hex

    


class KnowledgeBaseService:
    def __init__(self):
        os.makedirs(config.persist_directory,exist_ok=True) # 确保数据库存在
        self.chroma=Chroma(
            collection_name=config.collection_name,
            embedding_function=config.embeddings,
            persist_directory=config.persist_directory,
        )
        self.splitter=RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=len,
            separators=config.separators,
        )


    def upload_by_str(self,data,filename):
        md5_hex=get_string_md5(data)
        if check_md5(md5_hex):
            return "文件已存在"

        if len(data)>config.max_split:
            knowledge_chunks=self.splitter.split_text(data)
        else:
            knowledge_chunks=[data]
        
        metadata={
            'source':filename,
            'create_time':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'operator':'aly',
        }

        self.chroma.add_texts(
            texts=knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks],
        )
        save_md5(md5_hex)
        return "文件上传成功"





if __name__ == '__main__':
    print(get_string_md5('123456'))