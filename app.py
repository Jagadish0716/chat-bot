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
st.set_page_config(page_title="Jagadish ChatBot (Gemini)", layout="centered")
st.title("🧠 Jagadish ChatBot")

# ---------------------------
# Read API Key from Environment
# ---------------------------
# Gemini looks for GOOGLE_API_KEY by default
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY not found in environment variables.")
    st.stop()

# ---------------------------
# Sidebar Settings
# ---------------------------
st.sidebar.title("⚙️ Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
# Gemini usually allows up to 2048 or more, 500 is safe for testing
max_tokens = st.sidebar.slider("Max Tokens", 50, 2048, 500)
model_name = st.sidebar.selectbox(
    "Select Model",
    ["gemini-1.5-flash", "gemini-1.5-pro"]
)

# ---------------------------
# Prompt Template
# ---------------------------
# Note: Gemini works best with a Human message; 
# simple system-human pairings work well in LCEL
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
        return f"REAL ERROR: {str(e)}"

# ---------------------------
# User Input Section
# ---------------------------
user_input = st.text_input("Ask your question:")

if user_input:
    # Store user message
    st.session_state.chat_history.append(("User", user_input))

    # Generate bot response
    answer = generate_response(user_input)

    # Store bot message
    st.session_state.chat_history.append(("Bot", answer))

# ---------------------------
# Display Chat History
# ---------------------------
for role, text in st.session_state.chat_history:
    with st.chat_message(role.lower()):
        st.write(text)