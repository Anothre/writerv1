from dotenv import load_dotenv
load_dotenv()

import streamlit as st
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
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content

# System prompt for the interviewer
system_prompt = """
# CONTEXT #
You are an AI interviewer tasked with gathering in-depth information from users about their personal experiences. These conversations will be used to craft biographies or stories, and the information should be rich in detail to create an authentic and vivid narrative.

#########

# OBJECTIVE #
Your goal is to engage users in conversations that allow them to share their life journey, emotions, and reflections. You are to explore various aspects of their life, such as childhood, education, career, relationships, challenges, achievements, and aspirations. The purpose is to create a comprehensive and emotionally resonant story based on their experiences.

#########

# STYLE #
The style should be conversational, empathetic, and engaging. Ensure the tone remains supportive and patient throughout, encouraging open sharing. Active listening should be demonstrated to build trust and comfort in the conversation. 
Do not ask too many questions at one time.
#########

# TONE #
Maintain a warm, empathetic, and patient tone. Show appreciation for the user's time and openness. Let the conversation feel personal and thoughtful, making the user feel heard and understood.

#########

# AUDIENCE #
The audience consists of individuals willing to share their life experiences for the purpose of creating personal narratives or biographies. They may vary in background and life stage, so approach the conversation with flexibility and sensitivity to diverse experiences.

#########

# RESPONSE FORMAT #
Use open-ended questions to guide the conversation, encouraging detailed, reflective responses. Summarize key points at the end, and express appreciation for their time and insights.


"""

# Define the Streamlit page
def interviewer():

    st.title("AI 主持人 - 书写你的故事")
    st.markdown("欢迎来到我们的AI主持人系统。这里我们将帮助您讲述并记录您的生活故事。")

    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": "您好！我在这里帮助您撰写一个引人入胜的真实生活故事。您今天想写点什么?"}
        ]

    # Display chat history
    st.subheader("访谈过程")
    for message in st.session_state['chat_history'][1:]:  # Skip the system message
        if message['role'] == 'assistant':
            st.info(message['content'])
        else:
            st.write(message['content'])

    # User input
    user_input = st.text_area("您的回答:", key="input", height=150)
    col1, col2 = st.columns([1, 5])
    with col1:
        submit = st.button("发送", use_container_width=True)

    if submit and user_input:
        # Add user input to chat history
        st.session_state['chat_history'].append({"role": "user", "content": user_input})
        
        # Generate interviewer's response
        with st.spinner("AI正在思考..."):
            response = get_openai_response(st.session_state['chat_history'])

        # Add interviewer's response to chat history
        st.session_state['chat_history'].append({"role": "assistant", "content": response})
        st.info(f"主持人: {response}")
        st.experimental_rerun()

    # End conversation and export chat history
    if st.button("结束访谈", type="primary"):
        # Export chat history to a text file
        with open("interview_transcript.txt", "w", encoding="utf-8") as f:
            for message in st.session_state['chat_history'][1:]:  # Skip the system message
                f.write(f"{message['role'].capitalize()}: {message['content']}\n\n")
        
        st.success("访谈结束，感谢您的分享！您的故事已被保存。")
        # Clear chat history for a new session
        st.session_state['chat_history'] = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": "您好！我在这里帮助您撰写一个引人入胜的真实生活故事。您今天想写点什么?"}
        ]
        st.experimental_rerun()

if __name__ == "__main__":
    interviewer()