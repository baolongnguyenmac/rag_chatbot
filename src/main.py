from chat_rag import ChatRAG
from tools.tavily_search import TavilySearcher

from langchain_core.messages import SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from dotenv import load_dotenv

class Main(ChatRAG):
    def __init__(self, collection_name, persist_directory):
        super().__init__(collection_name, persist_directory)
        self.search_tool = TavilySearcher(max_results=10)

    def init_graph(self):
        retrieve = self.vector_db.get_db_searcher(k=10)
        search = self.search_tool.get_tavily_searcher()

        memory = MemorySaver()
        sys_prompt = '''
You are a helpful bot that assists me to read research paper in PDF file. But, in case you can't find the information to answer my question, you could perform search on the internet. You are provided tools in the XML tag: <tools></tools>. You have to decide which tool to use at the runtime.

<tools>
    `tavily_search`: Search the query on the internet
    `retrieve`: Retrieve the text from vector database and return the answer corresponding to my question
</tools>

When you call a tool, you should tell user about that in the output by adding a prefix (e.g., [tool_name]) to the final answer. For example, if you decide to call `tavily_search`, the your final answer should look like:
    [tavily_search] - <your answer>

Now, you will perform your task
'''
        return create_react_agent(
            model=self.llm,
            tools=[retrieve, search],
            checkpointer=memory,
            # prompt=SystemMessage("You always try your best to answer the query. Answer the question via retrieval if and only if needed (when the query is about the content in documents).")
            prompt=SystemMessage(sys_prompt)
        )

if __name__=='__main__':
    load_dotenv()
    config = {"configurable": {"thread_id": "chatbot_2"}}

    chatbot = Main(
        collection_name='federated_learning',
        persist_directory='./data/db'
    )

    chatbot.chat_gradio(config)