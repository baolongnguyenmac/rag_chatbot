from tools.vector_db import VectorDB
from langchain_core.documents.base import Document

from shutil import rmtree

import os
from dotenv import load_dotenv
load_dotenv()

class TestVectorDB:
    persist_directory='./src/tools/test/assets'
    collection_name='test'
    vector_db = VectorDB(
        collection_name=collection_name,
        persist_directory=persist_directory
    )

    filepath = './src/tools/test/assets/test.pdf'
    pdf_url = 'https://arxiv.org/pdf/1912.04977'
    os.system(f'curl -sSL -o {filepath} {pdf_url}')

    def test_get_chunk(self):
        # filepath = './data/2021 survey FL.pdf'
        docs = self.vector_db.get_chunk(self.filepath)

        assert type(docs) is list
        assert type(docs[0]) is Document

    def test_add_doc(self):
        # TODO test id
        # self.vector_db.vector_store.get_by_ids('id') == chunk.page_content

        self.vector_db.add_doc(self.filepath)

    def test_similarity_search(self):
        query = 'Federated learning'
        k = 10
        relevant_docs = self.vector_db.similarity_search(query, k)

        assert len(relevant_docs) == k
        assert type(relevant_docs) is list
        assert type(relevant_docs[0]) is Document

    def test_remove_collection(self):
        rmtree(self.persist_directory)

if __name__=='__main__':
    tester = TestVectorDB()
    tester.test_remove_collection()
