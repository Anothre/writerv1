import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import os
import openai
if "OPENAI_API_KEY" in st.secrets:
    st.write(
        "Has environment variables been set:",
        os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"]
    )
else:
    st.error("OPENAI_API_KEY is not set in secrets. Please add it to secrets.toml.")
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to get response from OpenAI
def get_openai_response(prompt):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content, mode='w'):
    with open(file_path, mode, encoding='utf-8') as file:
        file.write(content)

def generate_draft(outline, sections):
    # Clear the existing draft file
    write_file('draft.txt', '')
    
    each_section = sections.split('\n\n')
    for i, paragraph in enumerate(each_section, 1):
        draft_prompt = f"""
        # CONTEXT #
        You are a professional biography writer, and your team is helping a user write their real-life story. You have received a structured story outline from your editor, and your role is to write the full story section by section in Chinese, based on the provided outline and plot notes.

        #########

        # OUTLINE #
        {outline}
        
        #########
        #PLOT NOTES#
        {sections}
        # OBJECTIVE #
        Your goal is to write the story one plot at a time in Chinese, you are now writing plot {i} beginning each plot with the first scene and ending with the last scene provided in the PLOT NOTES. You are not to deviate from the structure or interact; simply focus on drafting the story according to the OUTLINE and PLOT NOTES.

        #########

        # STYLE #
        The style should be narrative, engaging, and reflective of real-life experiences. Write clearly and in a way that flows smoothly, ensuring the reader can follow the story naturally.

        #########

        # TONE #
        Maintain a respectful, empathetic tone throughout the story, staying true to the subjects experiences and emotions. Ensure that the tone is consistent with the life experiences described in the OUTLINE and PLOT NOTES.

        #########

        # AUDIENCE #
        The audience for this story includes readers who are interested in personal narratives and biographies. The story should feel authentic and relatable, capturing the key themes and experiences outlined by your editor.

        #########

        # RESPONSE FORMAT #
        Write the section in Chinese, following the structure of PLOT NOTES. Begin with the first scene and end with the last scene, as directed. Split plots with '\n\n'. Do not make any split within a plot. No interaction is needed.

        """

        draft = get_openai_response(draft_prompt)
        if draft:
            write_file('draft.txt', draft + '\n\n', mode='a')
        else:
            st.error(f"Failed to generate section {i}. Skipping.")

    st.success("初稿已保存至 'draft.txt'.")

def writer():
    st.title("撰稿人")

    # Read and display outline
    outline = read_file('outline.txt')
    st.subheader("大纲")
    outline_text = st.text_area("编辑大纲:", value=outline, height=300)

    # Read and display sections
    sections = read_file('sections.txt')
    st.subheader("段落节奏")
    sections_text = st.text_area("编辑段落节奏:", value=sections, height=300)

    # Save changes button
    if st.button("保存更改"):
        write_file('outline.txt', outline_text)
        write_file('sections.txt', sections_text)
        st.success("更改已保存!")

    # Generate draft button
    if st.button("生成初稿"):
        with st.spinner("正在生成初稿..."):
            generate_draft(outline_text, sections_text)

if __name__ == "__main__":
    writer()