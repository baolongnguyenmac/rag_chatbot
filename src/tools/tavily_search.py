from langchain_tavily import TavilySearch

from dotenv import load_dotenv
load_dotenv()

class TavilySearcher:
    def __init__(self, max_results:int):
        self.searcher = TavilySearch(max_results=max_results)

    def get_tavily_searcher(self):
        return self.searcher

if __name__=='__main__':
    tester = TavilySearcher(3)
    searcher = tester.get_tavily_searcher()
    print(searcher.invoke('Federated learning'))
