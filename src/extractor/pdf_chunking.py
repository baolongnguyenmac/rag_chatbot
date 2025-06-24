from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter as Splitter

from langchain_core.documents.base import Document

class PDFChunking:
    @staticmethod
    def get_chunk(filepath:str) -> list[Document]:
        loader:PyPDFLoader = PyPDFLoader(file_path=filepath)
        doc:list[Document] = loader.load()

        text_splitter:Splitter = Splitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
        chunks:list[Document] = text_splitter.split_documents(doc)
        return chunks
