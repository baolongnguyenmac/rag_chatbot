from langchain.chat_models import init_chat_model

from langchain_core.messages import HumanMessage, SystemMessage, trim_messages
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.graph import START, END, StateGraph, MessagesState
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver

import time
import gradio as gr
from dotenv import load_dotenv


class ChatBot:
    def __init__(self):
        self.llm:BaseChatModel = init_chat_model("gemini-2.5-flash", model_provider="google_genai")
        # max input token of gemini-2.5-flash: 1,048,576 (https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash)
        self.trimmer = trim_messages(
            max_tokens=200_000,
            strategy="last",
            token_counter=self.llm,
            include_system=True,
            allow_partial=False,
            start_on="human",
        )

    def call_llm(self, state:MessagesState) -> dict[str, str]:
            """prompt to LLM using all history stuff stored in `state`

            Args:
                state (MessagesState): dictionary with only one key `messages`, store all conversation history

            Returns:
                dict[str, str]: reply from the LLM
            """
            sys_prompt = ChatPromptTemplate([
                SystemMessage(content="You talk like a scumbag but you always try your best to respond to any query from user"),
                MessagesPlaceholder(variable_name='messages')
            ])
            trimmed_msg = self.trimmer.invoke(state['messages'])
            prompt = sys_prompt.invoke(trimmed_msg)
            reply = self.llm.invoke(prompt)
            return {"messages": reply}

    def init_graph(self) -> CompiledStateGraph:
        workflow = StateGraph(MessagesState)

        # create graph
        workflow.add_edge(START, "call_llm")
        workflow.add_node("call_llm", self.call_llm)
        workflow.add_edge("call_llm", END)

        # add memory
        memory = MemorySaver()
        return workflow.compile(checkpointer=memory)

    def chat_console(self, config:dict):
        """ for debug purpose
        """

        graph:CompiledStateGraph = self.init_graph()

        while True:
            user_msg = input("[>]:\t")
            reply = graph.invoke(input={"messages": HumanMessage(user_msg)}, config=config)
            print(f"[AI]:\t{reply['messages'][-1].content}")

            if user_msg.lower() == '!quit':
                print('~~~~~~~~~~~~~')
                break

    def chat_gradio(self, config:dict):
        graph:CompiledStateGraph = self.init_graph()

        def add_message(user_message:str, history:list[dict]):
            history.append({"role": "user", "content": user_message})
            return "", history

        def get_reply(history:list[dict]):
            bot_message = graph.invoke(input={"messages": HumanMessage(history[-1]["content"])}, config=config)
            bot_message = bot_message['messages'][-1].content

            # streaming to chat
            history.append({"role": "assistant", "content": ""})
            for character in bot_message:
                history[-1]['content'] += character
                time.sleep(0.01)
                yield history

        with gr.Blocks(theme='gstaff/xkcd', title='ChatBot', fill_height=True) as demo:
            gr.Markdown("<h1 style='text-align: center;'>ChatBot</h1>")

            chat_output = gr.Chatbot(type="messages", label='Assistant', scale=1)
            chat_input = gr.Textbox(show_label=False, placeholder='Enter your query...', scale=0, interactive=True)

            bot_msg = chat_input.submit(fn=add_message, inputs=[chat_input, chat_output], outputs=[chat_input, chat_output], queue=False)
            bot_msg.then(fn=get_reply, inputs=chat_output, outputs=chat_output)

        demo.launch(server_name='0.0.0.0', server_port=7860)

def main():
    load_dotenv()

    config = {"configurable": {"thread_id": "chatbot_2"}}

    chatbot = ChatBot()
    chatbot.chat_gradio(config)


if __name__=='__main__':
    main()
