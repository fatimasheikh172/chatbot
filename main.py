import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, set_tracing_disabled

# Load environment variables
load_dotenv()
set_tracing_disabled(True)

# Constants
MODEL_NAME = "gemini-2.0-flash"
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("🔐 GEMINI_API_KEY environment variable is not set.")
    st.stop()

# Setup external OpenAI-compatible client
external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Setup model
model = OpenAIChatCompletionsModel(
    model=MODEL_NAME,
    openai_client=external_client,
)

# Create Agent
assistant = Agent(
    name="🌆Pakistan Assistant 🇵🇰",
    instructions="""🧠 You are a helpful assistant that only answers questions about Pakistan. 🇵🇰
If the user asks about anything not related to Pakistan, respond:
"I'm sorry😔, I can only help with topics related to Pakistan." """,
    model=model,
)

# Helper function (without history)
async def ask_pakistan_assistant_once(user_message):
    chat = [{"role": "user", "content": user_message}]
    result = await Runner.run(
        starting_agent=assistant,
        input=chat,
    )
    return result.final_output

# --- Streamlit App UI ---
st.set_page_config(page_title="🇵🇰 Pakistan Assistant", page_icon="🤖")
st.title("🤖 Pakistan Assistant 🇵🇰")
st.write("📍 *Ask me anything about Pakistan!* 🇵🇰🕌🗺️")

user_input = st.text_input("💬 Enter the question:", placeholder="✍️ Type something about Pakistan...")

if st.button("🔍 Search"):
    if user_input.strip():
        with st.spinner("🤔 Thinking..."):
            response = asyncio.run(ask_pakistan_assistant_once(user_input))
            st.markdown(f"🧑‍💬 **You:** {user_input}")
            st.markdown(f"🤖 **Assistant:** {response}")
