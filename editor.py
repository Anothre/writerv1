from dotenv import load_dotenv
load_dotenv()

import os
import openai
import streamlit as st

# Check if the key exists in secrets
if "OPENAI_API_KEY" in st.secrets:
    st.write(
        "Has environment variables been set:",
        os.environ["OPENAI_API_KEY"] == st.secrets["OPENAI_API_KEY"]
    )
else:
    st.error("OPENAI_API_KEY is not set in secrets. Please add it to secrets.toml.")

def editor():
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

    def write_file(file_path, content):
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    # Streamlit UI
    st.title("编辑")

    # Read the initial content of the interview transcript
    initial_content = read_file('interview_transcript.txt')

    # Create a text area for editing the transcript
    edited_content = st.text_area("编辑采访笔记", value=initial_content, height=300)

    # Button to save changes
    if st.button("保存采访笔记"):
        write_file('interview_transcript.txt', edited_content)
        st.success("采访笔记保存成功!")

    # Button to generate outline
    if st.button("生成大纲"):
        with st.spinner("正在生成大纲..."):
            # Generate outline from the edited notes
            outline_prompt = f"""
            # CONTEXT #
            You are a professional editor responsible for organizing and summarizing interview notes to create a high-level story outline. Your team is helping a user write a real-life story. Your task is to analyze these notes and create a structured outline.

            #########

            #NOTES#
            {edited_content}

            #########

            # OBJECTIVE #
            The objective is to provide a high-level outline of the entire story based on the interview notes. This outline will guide the writer in drafting the story, ensuring clarity and flow.The outline should contain following parts
            [BACKGROUND]: The time and location of the story. If not mentioned in the notes, simply write not mentioned, do not make up the background.
            [CHARACTERS]: The description of each character showing up in the story.
            [OUTLINE]: The outline of the whole story which consists of various plots. 
            [BEATS]: The beats of the story line. Label the opening, development, climax and falldown. the beat label can be adjusted to fit the story if necessary.
            [INSTRUCTION]: Your instructions as a professional editor to passdown to writer to help writing the story.

            #########

            # STYLE #
            The style should be structured, concise, and easy to follow. Each section or paragraph summary should focus on key points, giving a clear idea of the story’s progression. The outline should offer enough detail to guide the writing without going into excessive depth.

            #########

            # TONE #
            Maintain a neutral tone. Focus on organizing the story logically and coherently, ensuring that it reads smoothly for the writer who will use the outline to develop the full narrative.

            #########

            # AUDIENCE #
            The audience is the writer responsible for drafting the story. The outline should be in Chinese and in clear, well-organized, and structured for quick reference, making it easy to transform the notes into a polished story.

            #########

            # RESPONSE FORMAT #
            [BACKGROUND]
            [/BACKGROUND]
            [CHARACTERS]
            [/CHARACTERS]
            [OUTLINE]
            [/OUTLINE]
            [BEATS]
            [/BEATS]
            [INSTRUCTIONS]
            [/INSTRUCTIONS]

            """

            outline = get_openai_response(outline_prompt)

            # Write the outline to a file
            write_file('outline.txt', outline)

            st.success("大纲已保存至 'outline.txt'")

            # Display the generated outline
            st.subheader("已生成的大纲")
            st.text_area("大纲", value=outline, height=400, disabled=True)

if __name__ == "__main__":
    editor()