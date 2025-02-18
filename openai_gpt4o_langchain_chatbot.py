import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app title
st.title("OpenAI GPT-4o Chatbot with LangChain")

llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model="gpt-4o",  # Use GPT-4 for even better factual accuracy
    temperature=0,  # Ensures the most correct answer
    streaming=True  
)

# Define prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
])

# Output parser to extract clean text
output_parser = StrOutputParser()

# Define the chat pipeline
chain = prompt | llm | output_parser

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt_input := st.chat_input("Ask ChatGPT anything"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt_input)

    # Invoke the LangChain pipeline for response
    with st.chat_message("assistant"):
        response = chain.invoke({"question": prompt_input})  # Call LangChain API
        st.markdown(response)  # Display response

    # Save assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
