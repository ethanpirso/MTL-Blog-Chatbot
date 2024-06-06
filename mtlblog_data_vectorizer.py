"""
MTLBlog Data Collector and Vectorizer

This script is designed to scrape data from various categories of the MTLBlog website,
process the textual content, and store it as vectors in a Chroma database for later retrieval.

Modules:
---------
- WebBaseLoader: Module for loading content from a given URL.
- RecursiveCharacterTextSplitter: Enables splitting text into manageable chunks.
- LlamaCppEmbeddings: Embedding system for vector representations.
- Chroma: Database system for vectorized content storage.

Key Functions:
--------------
- load_and_vectorize_data(url: str) -> str:
    Fetches and returns data as text from the specified URL.

- split_and_store_data(data: str, category: str) -> None:
    Processes and stores vectorized text in a category-specific Chroma database.

- load_all_data() -> None:
    Processes and stores data for each predefined MTLBlog category.

Execution:
----------
Upon running, the script processes data from all predefined categories and
stores it in separate Chroma databases under the `mtlBlogData` directory.

Note:
-----
Ensure:
1. The model path is correctly set.
2. All essential libraries are available.
3. You have appropriate permissions for data access and storage in the designated directories.

Usage:
------
Execute the script to initiate the data collection and storage procedure.
"""

from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import LlamaCppEmbeddings
from langchain.vectorstores import Chroma

# Llama LLM model path
model_path = "C:/Users/ethan/iCloudDrive/llama-2-7b-chat.ggmlv3.q8_0.bin"


# Load mtlBlog data
def load_and_vectorize_data(url):
    # Load data from the web
    loader = WebBaseLoader(url)
    data = loader.load()
    return data


# Vectorize and store data in Chrome DB
def split_and_store_data(data, category):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    vectorstore = Chroma.from_documents(documents=all_splits, embedding=LlamaCppEmbeddings(model_path=model_path),
                                        persist_directory=f"./mtlBlogData/{category}")
    vectorstore.persist()


# Load mtlBlog data for all categories
def load_all_data():
    categories = ['news', 'eat-drink', 'things-to-do', 'travel', 'sports', 'lifestyle',
                  'money', 'deals', 'real-estate', 'conversations']
    for category in categories:
        url = f'https://www.mtlblog.com/{category}'
        data = load_and_vectorize_data(url)
        split_and_store_data(data, category)


load_all_data()
