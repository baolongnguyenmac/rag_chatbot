from chatbot import ChatBot
from tools.tavily_search import TavilySearcher

from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage

from dotenv import load_dotenv

class ChatSearch(ChatBot):
    def __init__(self, max_results:int):
        super().__init__()
        self.tool = TavilySearcher(max_results=max_results).get_tavily_searcher()

    def init_graph(self) -> CompiledStateGraph:
        memory = MemorySaver()
        agent:CompiledStateGraph = create_react_agent(
            model=self.llm,
            tools=[self.tool],
            checkpointer=memory,
            prompt=SystemMessage(content="You talk like a scumbag but you always try your best to respond to any query from user")
        )
        return agent

if __name__=='__main__':
    load_dotenv()

    config = {"configurable": {"thread_id": "chatbot_2"}}

    chat_search = ChatSearch(max_results=10)
    chat_search.chat_gradio(config)
