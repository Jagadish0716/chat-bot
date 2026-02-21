import streamlit as st
import os
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# ---------------------------
# Logging Configuration
# ---------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------
# Streamlit Page Config
# ---------------------------
st.set_page_config(page_title="Jagadish ChatBot", layout="centered")
st.title("🧠 Jagadish ChatBot (Powered by Gemini)")

# ---------------------------
# Read API Key from Environment
# ---------------------------
# Change from OPENAI_API_KEY to GOOGLE_API_KEY
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY not found. Please update your Jenkins credentials.")
    st.stop()

# ---------------------------
# Sidebar Settings
# ---------------------------
st.sidebar.title("⚙️ Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 2048, 500)
model_name = st.sidebar.selectbox(
    "Select Model",
    ["gemini-1.5-flash", "gemini-1.5-pro"]
)

# ---------------------------
# Prompt Template
# ---------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful and professional AI assistant named Jagadish ChatBot."),
    ("human", "{question}")
])

# ---------------------------
# Session State for History
# ---------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------
# Generate Response Function
# ---------------------------
def generate_response(question: str) -> str:
    try:
        # Initializing Gemini Chat Model
        chat_model = ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=api_key,
            temperature=temperature,
            max_output_tokens=max_tokens
        )

        parser = StrOutputParser()
        chain = prompt | chat_model | parser
        response = chain.invoke({"question": question})

        return response

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return f"Error: {str(e)}"

# ---------------------------
# User Input Section
# ---------------------------
user_input = st.chat_input("Ask your question...")

if user_input:
    st.session_state.chat_history.append(("User", user_input))
    answer = generate_response(user_input)
    st.session_state.chat_history.append(("Bot", answer))

# ---------------------------
# Display Chat History
# ---------------------------
for role, text in st.session_state.chat_history:
    with st.chat_message(role.lower()):
        st.write(text)