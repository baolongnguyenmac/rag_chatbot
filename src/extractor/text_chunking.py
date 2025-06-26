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

        for idx, transcript in enumerate(trans):
            # create the overlap area with neighbor scripts
            augmented_context = None
            if idx == 0:
                augmented_context = ' '.join([transcript.text, trans[idx+1].text[:len(trans[idx+1].text)//2]])
            elif idx == len(trans)-1:
                augmented_context = ' '.join([trans[idx-1].text[len(trans[idx-1].text)//2:], transcript.text])
            else:
                augmented_context = ' '.join([trans[idx-1].text[len(trans[idx-1].text)//2:], transcript.text, trans[idx+1].text[:len(trans[idx+1].text)//2]])

            content = f'''
DURATION:
    Start timestamp: {str(transcript.start)}
    End timestamp: {str(transcript.end)}
SUBTITLE: {augmented_context}
            '''
            docs.append(Document(page_content=content))

        return docs
