# app.py
import streamlit as st
from main_2 import run_sql_agent

st.set_page_config(page_title="Chat2DB - T-Shirt Q&A", page_icon="👕")
st.title("👕 AtliQ T-Shirts: Database Q&A")

question = st.text_input("Ask your question about the T-shirt inventory:")

if question:
    with st.spinner("Thinking..."):
        response = run_sql_agent(question)
        st.success("Answer ready!")

        st.header("📢 Answer")
        st.write(response)
