import streamlit as st
import openai
import os
from pathlib import Path

# Configurar la clave de la API de OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY', 'tu_clave_de_api')

# Agregar un estilo CSS para ocultar el botón de "Deploy" y el pie de página
hide_elements_style = """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
"""

st.markdown(hide_elements_style, unsafe_allow_html=True)

st.title('chatbot Hospital SDLG')

messages = [('system', 'Eres un chatbot IA de un hospital no puedes responder nunca ninguna pregunta que no sea referente a un tema medico')]

if 'message' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input('Ingrese su pregunta...'):
    st.chat_message('user').markdown(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    messages.append(('human', prompt))
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-0613",
        prompt=''.join([f'{role}: {content}\n' for role, content in messages]),
        max_tokens=150
    ).choices[0].text.strip()
    with st.chat_message('assistant'):
        st.markdown(response)
    st.session_state.messages.append({'role': 'assistant', 'content': response})
