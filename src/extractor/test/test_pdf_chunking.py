from extractor.pdf_chunking import PDFChunking

from langchain_core.documents.base import Document
import os

class TestPDFChunking:
    filepath = './src/extractor/test/test.pdf'
    pdf_url = 'https://arxiv.org/pdf/1912.04977'
    os.system(f'curl -sSL -o {filepath} {pdf_url}')

    def test_get_chunk(self):
        docs = PDFChunking.get_chunk(self.filepath)

        assert type(docs) is list
        assert type(docs[0]) is Document

        os.remove(self.filepath)
