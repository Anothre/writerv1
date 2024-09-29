from dotenv import load_dotenv
load_dotenv()

import os
import anthropic

# Function to get response from Claude using the Messages API
def get_claude_response(prompt):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
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

# Read the interview notes
outline = read_file('outline.txt')
sections=read_file('sections.txt')
each_section = sections.split('\n\n')
# Generate outline from the notes
for i, paragraph in enumerate(each_section, 1):
    draft_prompt = f"""
    # CONTEXT #
    You are a professional biography writer, and your team is helping a user write their real-life story. You have received a structured story outline from your editor, and your role is to write the full story section by section in Chinese, based on the provided outline and section notes.

    #########

    # OUTLINE #
    {outline}
    
    #########
    #SECTION#
    {sections}
    # OBJECTIVE #
    Your goal is to write the story one section at a time in Chinese, you are now writing section {i} beginning each section with the first plot provided in the outline and ending with the last plot. You are not to deviate from the structure or interact; simply focus on drafting the story according to the outline and section notes.

    #########

    # STYLE #
    The style should be narrative, engaging, and reflective of real-life experiences. Write clearly and in a way that flows smoothly, ensuring the reader can follow the story naturally.

    #########

    # TONE #
    Maintain a respectful, empathetic tone throughout the story, staying true to the subjects experiences and emotions. Ensure that the tone is consistent with the life experiences described in the outline and section notes.

    #########

    # AUDIENCE #
    The audience for this story includes readers who are interested in personal narratives and biographies. The story should feel authentic and relatable, capturing the key themes and experiences outlined by your editor.

    #########

    # RESPONSE FORMAT #
    Write the section in Chinese, following the outline's structure. Begin with the first plot and end with the last plot, as directed. Donot start new line wtihin one section. No interaction is needed.
    """

    draft = get_claude_response(draft_prompt)
    if draft:
        write_file('draft.txt', draft)
    else:
        print(f"Failed to generate paragraph {i}. Skipping.")

print("Draft generation complete. Check 'draft.txt' for results.")