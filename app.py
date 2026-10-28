import os
import streamlit as st
from groq import Groq
from agent import run_agent

st.set_page_config(page_title="AI Interview Prep Agent", page_icon="🎯")
st.title("🎯 AI Interview Preparation Agent")
st.write("Practise interviews with an LLM that can call interview-focused Python tools.")

with st.sidebar:
    model = st.text_input("Groq model", os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"))
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.rerun()

key = (st.secrets.get("GROQ_API_KEY", "") if hasattr(st, "secrets") else "") or os.getenv("GROQ_API_KEY", "")
if not key:
    st.warning("Add GROQ_API_KEY to .streamlit/secrets.toml or your environment variables.")
    st.code('GROQ_API_KEY = "your-real-key"', language="toml")
    st.stop()

client = Groq(api_key=key)
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("activity"):
            with st.expander("Tool activity"):
                for a in m["activity"]:
                    st.write(a)

prompt = st.chat_input("Try: Give me 3 beginner Python interview questions")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer, activity = run_agent(client, prompt, st.session_state.messages[:-1], model)
                st.markdown(answer)
                if activity:
                    with st.expander("Tool activity"):
                        for a in activity:
                            st.write(a)
                st.session_state.messages.append({"role": "assistant", "content": answer, "activity": activity})
            except Exception as e:
                st.error(f"Error: {e}")
                st.caption("Check your API key and whether your chosen Groq model supports tool calling.")
