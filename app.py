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
st.title("🧠 Jagadish ChatBot (Gemini Edition)")

# ---------------------------
# Read API Key from Environment
# ---------------------------
# Note: Gemini uses GOOGLE_API_KEY by default
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("GOOGLE_API_KEY not found. Please check your Jenkins environment variables.")
    st.stop()

# ---------------------------
# Sidebar Settings
# ---------------------------
st.sidebar.title("⚙️ Model Settings")
st.sidebar.info("Adjust the AI's behavior here.")

model_name = st.sidebar.selectbox(
    "Select Gemini Model",
    ["gemini-1.5-flash", "gemini-1.5-pro"]
)

temperature = st.sidebar.slider("Creativity (Temperature)", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Response Length", 50, 2048, 500)

st.sidebar.divider()
st.sidebar.write("🚀 **Status:** Online")

# ---------------------------
# Prompt Template
# ---------------------------
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant named Jagadish ChatBot."),
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
        # Initialize Gemini model
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
        logger.error(f"Error: {e}")
        return f"Error: {str(e)}"

# ---------------------------
# UI Layout
# ---------------------------
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Generate bot response
    answer = generate_response(user_input)
    # Store and display history
    st.session_state.chat_history.append(("User", user_input))
    st.session_state.chat_history.append(("Bot", answer))

# Display Chat History
for role, text in st.session_state.chat_history:
    with st.chat_message(role.lower()):
        st.write(text)