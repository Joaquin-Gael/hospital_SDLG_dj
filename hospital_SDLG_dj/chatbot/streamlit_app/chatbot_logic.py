import streamlit as st
import dotenv
import os
from langchain_openai import ChatOpenAI
from pathlib import Path

dotenv.load_dotenv(dotenv_path=str(Path(__file__).parent.parent.parent.as_posix() + '/.env'))

chatbot = ChatOpenAI(model='gpt-3.5',temperature=0.3,api_key=os.environ.get('API_KEY',default='secret key'))

st.title('chatbot Hospital SDLG')

messages = [('system','Eres un chatbot IA de un hospital no podes responder nunca ninguna pregunta que no sea referente a un tema medico')]

if 'message' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input('Ingrese su pregunta...'):
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role':'user','content':prompt})
    messages.append(['human',prompt])
    response = chatbot.invoke([msg[1] for msg in messages]).content
    with st.chat_message('assistant'):
        st.markdown(response)
    st.session_state.messages.append({'role':'assistant','content':response})