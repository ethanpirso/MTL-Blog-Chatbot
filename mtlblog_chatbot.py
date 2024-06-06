"""
chatMTL - A Conversational Chatbot Interface

This script provides a chatbot interface powered by the LLM model (LlamaCpp)
to interactively retrieve information based on content from mtlBlog in various
categories including news, eat/drink, things-to-do, and more.

Modules:
---------
from langchain.llms: Module for working with the LlamaCpp LLM model.
from langchain.embeddings: Embedding functionality for LLM.
from langchain.vectorstores: Chroma database functionality for storing and retrieval.
from langchain.chains: Conversational chain for enabling back-and-forth chat.
from langchain.memory: Enables storing conversation summary.
tkinter: GUI toolkit for the chat interface.

Key Functions:
--------------
- chat_with_llm(category, question): Returns an assistant's response based on the
  given category and user's question.

- ChatbotInterface: A tkinter-based GUI class for the chat interface, enabling
  user interaction with the LLM model.

Execution:
----------
Upon execution, the script initializes the LLM model, loads vector data for
each mtlBlog category from Chroma DB, and launches the chatbot interface.

Usage:
------
To use, simply run the script. When prompted, choose a category or ask a question
related to a specific category. The chatbot will provide relevant responses based
on the mtlBlog content.
"""

from langchain.llms import LlamaCpp
from langchain.embeddings import LlamaCppEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter.font import Font
import threading


def chat_with_llm(category, question):
    # Ensure that the category data is loaded
    if category not in vector_stores:
        return "Category data not loaded. Please ensure the data is loaded properly."

    memory = ConversationSummaryMemory(llm=LLM, memory_key="chat_history", return_messages=True)
    retriever = vector_stores[category].as_retriever()
    qa_chain = ConversationalRetrievalChain.from_llm(LLM, retriever=retriever, memory=memory)

    prompt = (f"System: Based on the {category} content from Montreal Blog, "
              f"formulate a short response in 100 words or less which answers the User query: '{question}'. "
              f"Assistant: ")

    output = qa_chain(prompt)
    assistant_reply = output['answer']

    return assistant_reply


class ChatbotInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        self.configure(bg='black')  # Set the background color of the window
        self.title("chatMTL")

        # Define the fonts and colors for user and bot messages
        self.user_font = Font(family="Helvetica", size=14)
        self.bot_font = Font(family="Helvetica", size=14)
        self.user_color = 'red'
        self.bot_color = 'white'

        self.chat_area = scrolledtext.ScrolledText(self, bg='black', fg='white', wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10)

        self.message_field = ttk.Entry(self)
        self.message_field.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.X, expand=True)

        style = ttk.Style()
        style.configure("TButton", foreground="black", background="black")
        self.send_button = ttk.Button(self, text="Send", command=self.send_message, style="TButton")
        self.send_button.pack(padx=10, pady=10, side=tk.RIGHT)

        self.message_field.bind('<Return>', self.send_message)

        self.conversational_response = 0

    def send_message(self, event=None):
        message = self.message_field.get()
        if message:
            self.display_message("User", message, self.user_color, self.user_font)
            self.message_field.delete(0, 'end')

            # Start a new thread to fetch the bot's response
            threading.Thread(target=self.fetch_bot_response, args=(message,)).start()

    def fetch_bot_response(self, message):
        response = self.get_response(message)
        self.display_message("Bot", response, self.bot_color, self.bot_font)

    def display_message(self, sender, message, color, font):
        self.chat_area.configure(state='normal')
        tag_name = f"{sender.lower()}_tag"
        if not tag_name in self.chat_area.tag_names():
            # Create a new tag for this sender
            self.chat_area.tag_configure(tag_name, foreground=color)

        # Insert the message with the appropriate tag
        self.chat_area.insert(tk.END, f"{sender}: {message}\n", (tag_name, font))

        # Disable editing of the chat area
        self.chat_area.configure(state='disabled')

    def get_response(self, message):
        # Conversational responses with LLM
        if self.conversational_response == 1:
            category = self.category
            response = chat_with_llm(category, message)
            self.conversational_response = 0
            return response

        # Rule-based responses
        else:
            for category in vector_stores.keys():
                if category.replace("-", " ") in message.lower():
                    self.category = category
                    self.conversational_response = 1
                    return (f"Sure, I can provide information based on recent {category} content. "
                            f"What do you want to know?")
            return ("Please choose a category first: news, eat/drink, things to do, travel, sports, lifestyle, "
                    "money, deals, real-estate, or conversations.")


if __name__ == "__main__":
    # Load the LLM model using LlamaCpp
    model_path = "C:/Users/ethan/iCloudDrive/llama-2-7b-chat.ggmlv3.q8_0.bin"
    LLM = LlamaCpp(
        model_path=model_path,
        n_ctx=2000,
        temperature=0
    )
    # Load mtlBlog category data from Chrome DB
    vector_stores = {}
    categories = ['news', 'eat-drink', 'things-to-do', 'travel', 'sports', 'lifestyle',
                  'money', 'deals', 'real-estate', 'conversations']
    for category in categories:
        vector_stores[category] = Chroma(persist_directory=f"./mtlBlogData",
                                         embedding_function=LlamaCppEmbeddings(model_path=model_path))
    # Start the chatbot interface
    app = ChatbotInterface()
    app.fetch_bot_response('')
    app.mainloop()
