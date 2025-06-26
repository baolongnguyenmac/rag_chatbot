from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter as Splitter
from langchain_core.documents.base import Document

import pysrt

class TextChunking:
    @staticmethod
    def get_pdf_chunk(filepath:str) -> list[Document]:
        loader:PyPDFLoader = PyPDFLoader(file_path=filepath)
        doc:list[Document] = loader.load()

        text_splitter:Splitter = Splitter(chunk_size=1000, chunk_overlap=200, add_start_index=True)
        chunks:list[Document] = text_splitter.split_documents(doc)
        return chunks

    @staticmethod
    def get_srt_chunk(filepath:str) -> list[Document]:
        trans = pysrt.open(filepath)
        docs = []
        for transcript in trans:
            duration = f"Timestamp Start: {str(transcript.start)}; Timestamp End: {str(transcript.end)}."
            content = duration + transcript.text
            docs.append(Document(page_content=content))

        return docs
