import time
import os
import joblib
import streamlit as st
import google.generativeai as genai
import datetime
from dotenv import load_dotenv
from utils import menu_with_redirect

menu_with_redirect()

GOOGLE_API_KEY = st.secrets['GOOGLE_API_KEY']

genai.configure(api_key=GOOGLE_API_KEY)

new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '✨'

# Create a data/ folder if it doesn't already exist
try:
    os.mkdir('data/')
except:
    # data/ folder already exists
    pass

# Load past chats (if available)
try:
    past_chats: dict = joblib.load('data/past_chats_list')
except:
    past_chats = {}

# Sidebar allows a list of past chats
with st.sidebar:
    st.write('# Past Chats')
    if st.session_state.get('chat_id') is None:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x, 'New Chat'),
            placeholder='_',
        )
    else:
        # This will happen the first time AI response comes in
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
            placeholder='_',
        )
    # Save new chats after a message has been sent to AI
    # TODO: Give user a chance to name chat
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'

st.markdown(
    """
    <style>
    .gradient-container-chat {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        margin: 1rem 0;
        padding: 20px;
        border-radius: 10px;
        background: linear-gradient(45deg,#ff7e5f, #feb47b);
        color: white;
        text-align: center;
    }
    .gradient-text {
        font-size: 2.5em;
        font-weight: bold;
    }
    .gradient-subtext {
        font-size: 1.2em;
        margin-top: 10px;
    }
    </style>
    <div class="gradient-container-chat">
        <div class="gradient-text">Chat with Health Assistant</div>
        <div class="gradient-subtext">Get instant health insights and recommendations through AI-powered chat</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Chat history (allows to ask multiple questions)
try:
    st.session_state.messages = joblib.load(
        f'data/{st.session_state.chat_id}-st_messages'
    )
    st.session_state.gemini_history = joblib.load(
        f'data/{st.session_state.chat_id}-gemini_messages'
    )
    print('old cache')
except:
    st.session_state.messages = []
    st.session_state.gemini_history = []
    print('new_cache made')

st.session_state.model = genai.GenerativeModel('gemini-pro')
st.session_state.chat = st.session_state.model.start_chat(
    history=st.session_state.gemini_history,
)

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(
        name=message['role'],
        avatar=message.get('avatar'),
    ):
        st.markdown(message['content'])

# Get data from session state
data_df = st.session_state.get("data")

# Prepare data summary for context
data_summary = f"""
Heart Rate: {data_df['Heart Rate'].mean():.2f} bpm (average)
Temperature: {data_df['Temperature'].mean():.2f} °C (average)
ECG: {data_df['ECG'].mean():.2f} (average)
SpO2: {data_df['SpO2'].mean():.2f} % (average)
"""

# Prepare the prompt with the data table
data_table_prompt = f"""
Based on your health data:

| Metric      | Average Value |
|-------------|---------------|
| Heart Rate  | {data_df['Heart Rate'].mean():.2f} bpm  |
| Temperature | {data_df['Temperature'].mean():.2f} °C  |
| ECG         | {data_df['ECG'].mean():.2f}        |
| SpO2        | {data_df['SpO2'].mean():.2f} %    |

How can I assist you further?
"""

# React to user input
if prompt := st.chat_input('Your message here...'):
    # Save this as a chat for later
    if st.session_state.chat_id not in past_chats.keys():
        past_chats[st.session_state.chat_id] = st.session_state.chat_title
        joblib.dump(past_chats, 'data/past_chats_list')
    # Display user message in chat message container
    with st.chat_message('user'):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append(
        dict(
            role='user',
            content=prompt,
        )
    )
    ## Send message to AI
    full_prompt = f"{data_table_prompt}\n\nUser query: {prompt}"
    response = st.session_state.chat.send_message(
        full_prompt,
        stream=True,
    )
    # Display assistant response in chat message container
    with st.chat_message(
        name=MODEL_ROLE,
        avatar=AI_AVATAR_ICON,
    ):
        message_placeholder = st.empty()
        full_response = ''
        assistant_response = response
        # Streams in a chunk at a time
        for chunk in response:
            # Simulate stream of chunk
            # TODO: Chunk missing `text` if API stops mid-stream ("safety"?)
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.05)
                # Rewrites with a cursor at end
                message_placeholder.write(full_response + '▌')
        # Write full message with placeholder
        message_placeholder.write(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append(
        dict(
            role=MODEL_ROLE,
            content=st.session_state.chat.history[-1].parts[0].text,
            avatar=AI_AVATAR_ICON,
        )
    )
    st.session_state.gemini_history = st.session_state.chat.history
    # Save to file
    joblib.dump(
        st.session_state.messages,
        f'data/{st.session_state.chat_id}-st_messages',
    )
    joblib.dump(
        st.session_state.gemini_history,
        f'data/{st.session_state.chat_id}-gemini_messages',
    )
