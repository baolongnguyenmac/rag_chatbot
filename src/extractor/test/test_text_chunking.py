from extractor.text_chunking import TextChunking

from langchain_core.documents.base import Document
import os

class TestTextChunking:
    def test_get_pdf_chunk(self):
        filepath = './src/extractor/test/test.pdf'
        pdf_url = 'https://arxiv.org/pdf/1912.04977'
        os.system(f'curl -sSL -o {filepath} {pdf_url}')

        docs = TextChunking.get_pdf_chunk(filepath)

        assert type(docs) is list
        assert type(docs[0]) is Document

        os.remove(filepath)

    def test_get_srt_chunk(self):
        url = 'https://www.youtube.com/watch?v=qHGTs1NSB1s'

        
