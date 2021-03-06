from pathlib import Path
import streamlit as st

def read_markdown_file(markdown_file):
    return Path(markdown_file).read_text()


def app():
    intro_markdown = read_markdown_file("home.md")
    st.markdown(intro_markdown, unsafe_allow_html=True)



