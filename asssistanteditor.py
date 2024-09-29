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
def get_openai_response(messages):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    return response.choices[0].message.content

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def assistanteditor():
    st.title("助理编辑")

    # Read the current outline
    outline = read_file('outline.txt')

    # Create a text area for editing the outline
    edited_outline = st.text_area("编辑大纲", value=outline, height=300)

    # Save button for the outline
    if st.button("保存大纲"):
        write_file('outline.txt', edited_outline)
        st.success("大纲保存成功!")

    # Button to generate sections
    if st.button("生成情景笔记"):
        with st.spinner("正在生成情景笔记..."):
            notes = read_file('interview_transcript.txt')
            assistant_editor_prompt = f"""
            You are an assistant editor responsible for splitting the plots of the story based on the story outline. You've received a high-level outline from the editor and the notes from interview with the user, and your task is to create detailed notes of each plots of the story.
            Your output should be in Chinese.

            #########

            # OUTLINE #
            {edited_outline}

            #########
            # NOTES #
            {notes}

            #########

            # OBJECTIVE #
            The objective is to provide detailed plot descriptions based on the outline while controlling the story's beat. Each plot should include:
            1. [THEME]:The main idea or topic
            2. [KEY_POINTS]:Key points to be covered
            3. [DEVELOPMENT]:Any relevant character development or plot progression
            4. [TONE]:Suggested tone or mood for the plot
            5. [FIRST_PLOT]: The first scene of the plot
            6. [LAST_PLOT]: The last scene of the plot
            7. [WORD_LIMIT]: The word limit of the plot based on the importance to the development to the story.
                [less than 50 words]
                [50-100 words]
                [100-200 words]
                [200-400 words]
                [more than 500 words]

            # ... rest of the prompt ...

            ##########
            # OUTPUT #
            Split each plot with "\n\n", Do not make any split within each plot.
            """

            messages = [
                {"role": "system", "content": "You are an assistant editor helping to expand a story outline into plot section descriptions in CHinese. Write down all the sections. Do not say 'And so on with the other sections of the story...'. Be strict on the [IMPORTANCE] evaluation to avoid redundant description on minor plots. Split each plot with '\n\n', do not make any split within each section."},
                {"role": "user", "content": assistant_editor_prompt}
            ]

            detailed_sections = get_openai_response(messages)

            # Write the detailed sections to a file
            write_file('sections.txt', detailed_sections)

        st.success("情景笔记已保存至 'sections.txt'")

    # Display the generated sections
    if os.path.exists('sections.txt'):
        st.subheader("已生成的情景笔记")
        sections = read_file('sections.txt')
        st.text_area("情景笔记", value=sections, height=300, disabled=True)

if __name__ == "__main__":
    assistanteditor()