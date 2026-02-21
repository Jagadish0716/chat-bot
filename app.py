import streamlit as st
import os
import logging
from langchain_openai import ChatOpenAI
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
st.title("🧠 Jagadish ChatBot")

# ---------------------------
# Read API Key from Environment
# ---------------------------
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("OPENAI_API_KEY not found in environment variables.")
    st.stop()

# ---------------------------
# Sidebar Settings
# ---------------------------
st.sidebar.title("⚙️ Settings")
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 500, 200)
model_name = st.sidebar.selectbox(
    "Select Model",
    ["gpt-4o-mini", "gpt-4o"]
)

# ---------------------------
# Prompt Template
# ---------------------------
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a professional AI assistant. "
        "Provide accurate, concise, and structured responses. "
        "If you do not know something, clearly say so."
    ),
    ("user", "Question: {question}")
])

# ---------------------------
# Initialize Chat History
# ---------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------
# Generate Response Function
# ---------------------------
def generate_response(question: str) -> str:
    try:
        chat_model = ChatOpenAI(
            api_key=api_key,
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )

        parser = StrOutputParser()
        chain = prompt | chat_model | parser
        response = chain.invoke({"question": question})

        return response

    # except Exception as e:
    #     logger.error(f"Error generating response: {e}")
    #     return "An error occurred while generating response."
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
for role, message in st.session_state.chat_history:
    if role == "User":
        st.markdown(f"**🧑 You:** {message}")
    else:
        st.markdown(f"**🧠 Bot:** {message}")