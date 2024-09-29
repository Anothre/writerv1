from dotenv import load_dotenv
load_dotenv()

import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to get response from OpenAI
def get_openai_response(prompt):
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def read_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_notes(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Read the interview transcript
transcript = read_transcript('interview_transcript.txt')

# Generate notes from the transcript
notes_prompt = f"""
# CONTEXT #
You are a professional note keeper responsible for organizing and summarizing interview transcripts. Your team is helping a user write a real-life story, and your role is to create concise, well-structured notes based on interviews conducted by your team. These notes will be used by an editor to develop a detailed story outline.

#########

# OBJECTIVE #
Analyze the given interview transcript, focusing on extracting key information, necessary details, and main themes. Organize the notes in a clear, easy-to-read format, and ensure they are concise yet comprehensive. These notes will help the editor construct a coherent and structured story outline.

#########
#Transcript#
{transcript}


# STYLE #
The style should be factual, organized, and focused on clarity. Summarize the key points and themes without unnecessary elaboration. Ensure the notes are logically structured and categorized for quick reference.

#########

# TONE #
Maintain a professional and neutral tone throughout. Focus on providing clear, well-organized information without personal opinions or embellishment.

#########

# AUDIENCE #
The primary audience for your notes is an editor who will be drafting a story based on the users life experiences. Your notes should be easy for them to follow, offering clear insights into the interviews most important aspects.

#########

# RESPONSE FORMAT #
Provide structured notes in Chinese, summarizing key themes, necessary details, and main events discussed in the interview. Organize the notes in a clear, easy-to-read format that aligns with the flow of the conversation.

#############
"""

notes = get_openai_response(notes_prompt)

# Write the notes to a file
write_notes('interview_notes.txt', notes)

print("Notes have been generated and saved to 'interview_notes.txt'")