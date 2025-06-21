from tools.vector_db import VectorDB
from chatbot import ChatBot

from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

import time
import gradio as gr
from dotenv import load_dotenv


class ChatRAG(ChatBot):
    def __init__(self, collection_name:str, persist_directory:str):
        super().__init__()
        self.vector_db = VectorDB(collection_name, persist_directory)

    def init_graph(self):
        retrieve = self.vector_db.get_db_searcher(k=10)

        memory = MemorySaver()
        return create_react_agent(
            model=self.llm,
            tools=[retrieve],
            checkpointer=memory,
            prompt=SystemMessage("You will be provided some research papers about a research topic. You will answer the question based on these papers if and only if needed (when the query is about the research topic).")
        )

    def chat_gradio(self, config:dict):
        graph = self.init_graph()

        def add_message(history:list[dict], message:dict):
            has_file = False
            list_files = []
            for filepath in message["files"]:
                has_file = True
                history.append({"role": "user", "content": {"path": filepath}})

                filename = filepath.split("/")[-1]
                gr.Info(f'Importing {filename} into database', duration=0)
                self.vector_db.add_doc(filepath)
                list_files.append(filename)

            # i want to explicitly demonstrate what I input to LLM to make it read the file
            # thus, i explicitly modify the user input
            # otherwise, these modification can be implicitly done in `get_reply` function
            if has_file:
                if message["text"] != '':
                    history.append({"role": "user", "content": f"{message['text']}. {list_files} are already in the vector database"})
                else:
                    history.append({"role": "user", "content": f"Summarize the content of these file {list_files}. They are already in the vector database"})
            else:
                history.append({"role": "user", "content": message['text']})

            # if has_file, we have to wait for it to be loaded in db
            return history, gr.MultimodalTextbox(value=None, interactive=has_file)

        def get_reply(history: list):
            # [print(h['content']) for h in history]
            # print('~'*80)

            # list_input = []
            # if type(history[-1]['content']) is tuple:
            #     list_input.append('Read these files. They are already in the vector database')
            # for item in reversed(history):
            #     if item['role'] != 'user':
            #         break
            #     else:
            #         content = item['content']
            #         if type(item['content']) is tuple:
            #             content = content[0].split('/')[-1]
            #         list_input.append(content)

            # print(list_input)
            # bot_message = graph.invoke(input={"messages": HumanMessage('. '.join(list_input))}, config=config)

            bot_message = graph.invoke(input={"messages": HumanMessage(history[-1]['content'])}, config=config)
            bot_message = bot_message['messages'][-1].content

            history.append({"role": "assistant", "content": ""})
            for character in bot_message:
                history[-1]["content"] += character
                time.sleep(0.01)
                yield history

        with gr.Blocks(theme='gstaff/xkcd', title='ChatBot', fill_height=True) as demo:
            gr.Markdown("<h1 style='text-align: center;'>ChatBot</h1>")

            chat_output = gr.Chatbot(elem_id="chatbot", bubble_full_width=False, type="messages", scale=1)
            chat_input = gr.MultimodalTextbox(interactive=True, file_count="multiple", placeholder="Enter message or upload PDF file", show_label=False, sources=["upload"], file_types=['.pdf'], scale=0)

            chat_msg = chat_input.submit(add_message, [chat_output, chat_input], [chat_output, chat_input])
            bot_msg = chat_msg.then(get_reply, chat_output, chat_output, api_name="bot_response")
            bot_msg.then(lambda: gr.MultimodalTextbox(interactive=True), None, [chat_input])

        demo.launch(server_name="0.0.0.0", server_port=7860)

if __name__=='__main__':
    load_dotenv()

    config = {"configurable": {"thread_id": "chatbot_2"}}

    chat_search = ChatRAG(
        collection_name='federated_learning',
        persist_directory='./data/db'
    )
    chat_search.chat_gradio(config)
