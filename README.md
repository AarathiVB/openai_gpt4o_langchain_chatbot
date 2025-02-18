# **OpenAI GPT-4o Chatbot**

## **Project Overview**
This project is a **conversational AI chatbot** built using **OpenAI GPT-4o, LangChain, and Streamlit**. It provides a **real-time chatbot interface** where users can ask questions and receive intelligent responses. The chatbot leverages **LangChain's structured prompt handling, API calls to OpenAI, and session-based chat memory**.

---

## **Features**
- **Uses OpenAI GPT-4o** for intelligent and accurate responses.
- **LangChain-powered API integration** for structured query processing.
- **Streamlit UI for easy user interaction**.
- **Session-based chat memory** to maintain context.
- **Streaming responses for a real-time chat experience**.

---

## **Prerequisites**
Ensure you have the following installed:
- **Python 3.8+**
- **OpenAI API Key** (for accessing GPT-4o)
- **Streamlit**
- **LangChain & Dependencies**

---

## **Installation**
1. **Clone this repository**

2. **Create and activate a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Mac/Linux
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**  
   Create a `.env` file in the project root and add your **OpenAI API key** from https://platform.openai.com/api-keys:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

---

## **Code Explanation**
Below is a detailed explanation of the key sections of the code.

### **1. Import Required Libraries**
```python
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
```
- **Streamlit (`st`)**: Used to build the chatbot UI.
- **dotenv (`load_dotenv`)**: Loads environment variables for API key security.
- **LangChain (`ChatOpenAI`, `ChatPromptTemplate`, `StrOutputParser`)**: Handles OpenAI model calls, structured prompting, and output parsing.

---

### **2. Load API Key from Environment Variables**
```python
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
```
- Ensures **secure storage** of API keys instead of hardcoding them.
- Uses **dotenv** to fetch the API key from a `.env` file.

---

### **3. Initialize Streamlit App**
```python
st.title("OpenAI GPT-4o Chatbot with LangChain")
```
- **Displays the chatbot title** on the Streamlit UI.

---

### **4. Define the OpenAI LLM Model**
```python
llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model="gpt-4o",
    temperature=0,
    streaming=True  
)
```
- Uses **LangChain's `ChatOpenAI`** instead of direct OpenAI API calls.
- **`model="gpt-4o"`**: Specifies OpenAI’s GPT-4o model.
- **`temperature=0`**: Ensures deterministic, fact-based answers.
- **`streaming=True`**: Enables real-time response streaming.

---

### **5. Define the Prompt Template**
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{question}")
])
```
- **Ensures structured input** to OpenAI using LangChain.
- The **system message** sets the chatbot’s personality.
- The **human message** dynamically inserts the user's question.

---

### **6. Define the Output Parser**
```python
output_parser = StrOutputParser()
```
- Extracts **clean text** from OpenAI’s structured response.

---

### **7. Define the Chat Processing Pipeline**
```python
chain = prompt | llm | output_parser
```
- Uses LangChain’s **`|` operator** to create a modular workflow:
  1. **Formats the prompt**.
  2. **Sends it to GPT-4o**.
  3. **Extracts the response text**.

---

### **8. Initializing Chat History**
```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```
- `st.session_state` is a global state variable in Streamlit that persists across reruns.
- The `"messages"` key is initialized as an empty list if it does not already exist.
- This ensures that the conversation history is maintained throughout the session.

---

### **9. Displaying Chat History**
```python
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
```
- Iterates through all saved messages in `st.session_state.messages`.
- Uses `st.chat_message(message["role"])` to format and display the conversation in the chat UI.
- Displays the content using `st.markdown()`, preserving text formatting.

- Ensures that all previous messages are displayed each time the app refreshes.
- Maintains conversation context between user queries.

---

### **10. Accepting User Input**
```python
if prompt_input := st.chat_input("Ask ChatGPT anything"):
```
- Uses `st.chat_input()` to take user input.
- The `:=` (Walrus operator) ensures that the input is not empty before assigning it to `prompt_input`.

- Prevents processing of empty inputs.
- Waits for user input before invoking the AI.

---

### **11. Adding the User's Message to Chat History**
```python
st.session_state.messages.append({"role": "user", "content": prompt_input})
```

- Adds the user’s message to the session state as a dictionary:
  ```json
  {"role": "user", "content": "User's input here"}
  ```
- Stores the conversation history for future reference.

**Message Role in OpenAI API:**

OpenAI’s `ChatCompletion` API expects structured messages where `"role": "user"` represents human input.

**Example Format:**
```json
[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the capital of France?"}
]
```

---

### **12. Displaying User Message**
```python
with st.chat_message("user"):
    st.markdown(prompt_input)
```
- Uses `st.chat_message("user")` to display the user’s message in Streamlit.

- Ensures that the chat interface updates immediately with the user’s message.

---

### **13. Processing AI Response Using LangChain**
```python
with st.chat_message("assistant"):
    response = chain.invoke({"question": prompt_input})  
    st.markdown(response)  
```
- Calls `chain.invoke({"question": prompt_input})` to process the user input through the LangChain pipeline.
- The LangChain pipeline (`chain`) follows these steps:
  1. Formats the user input into a structured prompt.
  2. Sends it to OpenAI GPT-4o.
  3. Extracts the clean response using `StrOutputParser()`.
- Displays the AI’s response in the chat interface.

**OpenAI Message Structure:**

The structured message list passed to OpenAI via LangChain looks like:
```json
[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Translate 'hello' into French."},
    {"role": "assistant", "content": "Bonjour."}
]
```
**Breakdown of OpenAI Message Roles**
| Role       | Purpose                                      |
|------------|----------------------------------------------|
| **system** | Defines AI’s personality and behavior.       |
| **user**   | Represents human input (questions/commands). |
| **assistant** | AI-generated response.                      |

- OpenAI models require structured message history to provide context-aware responses.
---

### **14. Storing AI Response in Chat History**
```python
st.session_state.messages.append({"role": "assistant", "content": response})
```
- Saves the assistant’s response in session state as a dictionary:
  ```json
  {"role": "assistant", "content": "Bonjour."}
  ```
- Ensures AI responses are stored and displayed in future interactions.
---

#### **Summary of Message Roles**
| Step  | Message Role  | Example Message  | Purpose  |
|--------|--------------|------------------|----------|
| **System Message**  | `"system"`  | `"You are a helpful assistant."`  | Defines AI behavior.  |
| **User Message (First Query)**  | `"user"`  | `"What is the capital of France?"`  | User's question to AI.  |
| **AI Response (First Reply)**  | `"assistant"`  | `"The capital of France is Paris."`  | AI-generated answer.  |
| **User Message (Follow-up)**  | `"user"`  | `"What is its population?"`  | Continuing the chat.  |
| **AI Response (Follow-up)**  | `"assistant"`  | `"Paris has a population of about 2.1 million."`  | Context-aware response.  |
---

## **Running the Application**
To launch the Streamlit chatbot, run:
```bash
streamlit run app.py
```
This will open the **chat interface** in a web browser.

---

## **References**
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

## **License**
This project is licensed under the **MIT License**.
