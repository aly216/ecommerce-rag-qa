import config_data as config
from operator import itemgetter
from vector_stores import VectorStoreService
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from file_history_store import get_history


class RAGService(object):
    def __init__(self):
        self.vector_service=VectorStoreService(
            embedding=config.embeddings
        )
        self.prompt_template=ChatPromptTemplate.from_messages([
            ("system", "以我提供的已知信息为基础，简洁，专业地回答用户的问题，参考资料{context}"),
            MessagesPlaceholder("history"),
            ("user", "请回答用户的问题，：{input}"),
        ])
        self.chat_model=config.model
        self.chain=self.__get_chain()


    def __get_chain(self):
        retriever=self.vector_service.get_retriever()

        def format_documents(docs: list[Document]):
            if not docs:
                return "无相关文档"
            formatted_str=''
            for doc in docs:
                formatted_str+=f"文档片段：{doc.page_content}文档元数据：{doc.metadata}\n"
            return formatted_str

        chain=(
            RunnablePassthrough.assign(
                context=itemgetter("input") | retriever | format_documents
            )
            | self.prompt_template
            | self.chat_model
            | StrOutputParser()
        )

        chain_with_history=RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return chain_with_history


if __name__ == '__main__':
    session_config={
        'configurable':{
            'session_id':'user_001'
        }
    }
    rag_service=RAGService()
    results=rag_service.chain.invoke({"input":"我身高170cm,尺码推荐多少"}, session_config)
    print(results)
