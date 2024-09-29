import streamlit as st
from dotenv import load_dotenv
load_dotenv()

import os
import anthropic
if "CLAUDE_API_KEY" in st.secrets:
    st.write(
        "Has environment variables been set:",
        os.environ["CLAUDE_API_KEY"] == st.secrets["CLAUDE_API_KEY"]
    )
else:
    st.error("CLAUDE_API_KEY is not set in secrets. Please add it to secrets.toml.")
# Function to get response from Claude using the Messages API
def get_claude_response(prompt):
    client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        messages=[{"role": "user", "content": prompt}]
    )
    # Extract the text content from the response
    text_content = ''.join(block.text for block in response.content)
    return text_content

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(content + '\n\n')  # Add two newlines for separation

def amplifier():
    st.title("修辞大师")

    # Read the files
    outline = read_file('outline.txt')
    draft = read_file('draft.txt')
    section_notes = read_file('sections.txt')

    # Display and allow editing of the draft
    edited_draft = st.text_area("编辑初稿:", value=draft, height=300)

    # Save draft changes
    if st.button("Save Draft"):
        write_file('draft.txt', edited_draft)
        st.success("初稿已保存!")

    # Generate story button
    if st.button("润色初稿"):
        with st.spinner("正在润色中..."):
            # Split the draft into paragraphs
            draft_sections = edited_draft.split('\n\n')
            generated_story = ""

            for i, section in enumerate(draft_sections, 1):
                amplify_prompt = f"""
                # CONTEXT #
                You are a skilled Chinese story amplifier. Your task is to enhance a draft section by adding rhetorical devices and engaging dialogues, making it more captivating for readers. 
                #####################
                # OUTLINE #
                {outline}
                #####################
                #DRAFT SECTION TO AMPLIFY#
                {section}
                ######################
                #SECTION_NOTES#
                {section_notes}
                ######################
                # OBJECTIVE #
                Amplify the given section by:
                1. Adding vivid descriptions and sensory details properly following the section notes
                2. Incorporating various rhetorical devices, Do not use single devices too much
                3. Expanding existing dialogues and adding new ones to make the story more engaging properly following the section notes
                4. Ensuring the amplified section follows the structure and beats of the outline section notes

                # STYLE #
                Maintain the original tone and style while enhancing the storytelling. The amplified version should be more immersive and emotionally resonant.

                # RESPONSE FORMAT #
                Provide the amplified section as a continuous text in Chinese, ready for readers. Do not include any explanations or comments.
                """

                amplified_section = get_claude_response(amplify_prompt)
                generated_story += f"Section {i}:\n{amplified_section}\n\n"

        # Display the generated story and allow editing
        st.subheader("已润色的故事")
        edited_story = st.text_area("编辑您的故事:", value=generated_story, height=500)

        # Save and export story button
        if st.button("保存并导出故事"):
            write_file('story.txt', edited_story)
            st.success("故事已成功导出!")
            st.download_button(
                label="下载故事",
                data=edited_story,
                file_name="generated_story.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    amplifier()