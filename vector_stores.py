from langchain_chroma import Chroma
import config_data as config


class VectorStoreService(object):
    def __init__(self,embedding):
        self.embedding=embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            persist_directory=config.persist_directory,
            embedding_function=self.embedding
        )


    def get_retriever(self):
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})



if __name__ == '__main__':
    vector_store_service = VectorStoreService(config.embeddings)
    retriever = vector_store_service.get_retriever()
    results = retriever.invoke("你好")
    print(results)