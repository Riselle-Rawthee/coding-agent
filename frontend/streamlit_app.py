import streamlit as st
import requests
import pandas as pd

import sys
sys.path.append("C:/AI Agents/coding-agent")  # Add the project root to sys.path
from backend.app.core.config import settings

st.title("C++ AI Assistant")
st.write("Generate C++ code using AI models")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input for session ID
session_id = st.text_input("Enter Session ID", value="user123")

# Input for model selection
model = st.selectbox("Select Model", ["llama3", "mistral", "fine-tuned-cpp"])

# Input for code prompt
prompt = st.text_area("Enter your code prompt")

if st.button("Get models"):
    try:
        response = requests.get("http://127.0.0.1:8000//api/models")
        if response.status_code == 200:
            df_data = []
            i=0
            st.write(response.json()["models"]["models"])
            
        else:
            st.error("Failed to fetch the models or no models have been downloaded")
    except Exception as e:
        st.error(f"Error: {e}")



if st.button("Generate Code"):
    try:
        # Send request to the backend
        response = requests.post(
            f"http://127.0.0.1:8000//api/generate",
            json={"model": model, "prompt": prompt, "session_id": session_id})
        
        if response.status_code == 200:
            # Add user and assistant messages to chat history
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.session_state.chat_history.append({"role": "assistant", "content": response.json()["response"]})

            # Display chat history
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
        else:
            st.error("Failed to generate code")
    except Exception as e:
        st.error(f"Error: {e}")