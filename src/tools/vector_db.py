# chunking
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter as Splitter

# embedding and storing
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma.vectorstores import Chroma
from langchain_core.documents.base import Document

# tool
from langchain_core.tools import tool

class VectorDB:
    def __init__(self, collection_name:str, persist_directory:str) -> None:
        self.vector_store:Chroma = Chroma(
            collection_name=collection_name,
            embedding_function=GoogleGenerativeAIEmbeddings(model="models/text-embedding-004"),
            persist_directory=persist_directory
        )

    def get_chunk(self, filepath:str) -> list[Document]:
        loader:PyPDFLoader = PyPDFLoader(file_path=filepath)
        doc:list[Document] = loader.load()

        text_splitter:Splitter = Splitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
        chunks:list[Document] = text_splitter.split_documents(doc)
        return chunks

    def add_doc(self, filepath:str) -> None:
        print(f'Import {filepath.split("/")[-1]}')
        chunks:list[Document] = self.get_chunk(filepath)

        # hash content of chunk to obtain an unique id
        ids = [str(hash(doc.page_content)) for doc in chunks]
        self.vector_store.add_documents(documents=chunks, ids=ids)

        print(f'{filepath.split("/")[-1]} imported!')
        print('~'*80)

    def similarity_search(self, query:str, k:int) -> list[Document]:
        return self.vector_store.similarity_search(query=query, k=k)

    def get_db_searcher(self, k:int):
        """return a semantic search tool that searches for relevant documents in vector db with a given query

        Args:
            k (int): number of return documents

        Returns:
            retrieve: a function
        """

        @tool(response_format='content_and_artifact')
        def retrieve(query:str) -> tuple[str, list[Document]]:
            """Search for relevant contents in vector database with a given query

            Args:
                query (str): Query

            Returns:
                content (str): A string of relevant content
                relevant_docs (list[Document]): a list of relevant documents
            """
            print(f'Get data with {query}')
            relevant_docs = self.vector_store.similarity_search(query=query, k=k)
            content = '\n\n'.join([doc.page_content for doc in relevant_docs])
            print('~'*80)
            return content, relevant_docs

        return retrieve
