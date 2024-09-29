import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

from interviewer import interviewer
from editor import editor
from asssistanteditor import assistanteditor
from writer import writer
from amplifier import amplifier


# Dictionary of pages
pages = {
    "主持人": interviewer,
    "编辑": editor,
    "助理编辑": assistanteditor,
    "撰稿人": writer,
    "修辞大师": amplifier
}

# Sidebar for page navigation
st.sidebar.title("请按顺序选择团队")

# Replace dropdown with radio buttons for navigation
selection = st.sidebar.radio("请按顺序选择团队", list(pages.keys()))

# Call the selected page function
page = pages[selection]
page()
