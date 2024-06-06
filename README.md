# MTL Blog Chatbot Project

## Overview
The MTL Blog Chatbot project is an innovative solution designed to interactively provide users with information and updates from the MTL Blog website. Leveraging the power of the LlamaCpp Large Language Model (LLM), this chatbot offers responses across various categories such as news, eat/drink, things-to-do, and more. The project encapsulates the entire pipeline from data collection and vectorization to conversational interface implementation.

## Key Features
- **Data Collection and Vectorization:** Utilizes a custom script to scrape content from the MTL Blog website, process the textual data, and store it in a vectorized format for efficient retrieval.
- **Vector Database:** Employs the Chroma database system to manage the vectorized content, enabling quick and relevant responses based on user queries.
- **Conversational Interface:** A user-friendly chat interface built with Tkinter allows for real-time interaction with the chatbot.
- **Large Language Model Integration:** Incorporates the LlamaCpp LLM for generating responses, ensuring they are contextually relevant and informative.

## Technical Details

### Data Modeling and Vector Database
The project uses a sophisticated approach to data modeling, where content from the MTL Blog is first scraped and then vectorized using the LlamaCppEmbeddings system. This process transforms textual data into high-dimensional vectors that capture the semantic essence of the content. These vectors are stored in the Chroma vector database, which facilitates efficient retrieval of information based on similarity to the user's query.

### Web Scraping
Data collection is achieved through a dedicated web scraping script (`mtlblog_data_vectorizer.py`) that automatically fetches the latest articles from predefined categories on the MTL Blog website. This script ensures that the chatbot's database is continually updated with fresh content, maintaining the relevance and accuracy of its responses.

### Conversational Flow
The chatbot utilizes a conversational retrieval chain to manage the flow of dialogue. This involves interpreting the user's query, fetching the most relevant information from the vector database, and crafting a response that is both informative and contextually appropriate. The system is designed to handle a wide range of queries by dynamically selecting the most relevant category based on the user's input.

## Usage
To interact with the MTL Blog Chatbot, simply run the `mtlblog_chatbot.py` script. The graphical interface will prompt you to select a category or ask a question. The chatbot will then provide you with information drawn directly from the latest MTL Blog content, offering a seamless and engaging user experience.

## Conclusion
The MTL Blog Chatbot project represents a significant advancement in the use of AI and NLP technologies for information retrieval and user interaction. By combining state-of-the-art language models with efficient data modeling and vectorization techniques, this project offers a glimpse into the future of conversational interfaces.

## Authors
- Ethan Pirso