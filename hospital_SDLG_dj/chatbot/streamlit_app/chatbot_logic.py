import streamlit as st
import dotenv
import os
from langchain_openai import ChatOpenAI
from pathlib import Path

dotenv.load_dotenv(dotenv_path=str(Path(__file__).parent.parent.parent.as_posix() + '/.env'))

chatbot = ChatOpenAI(model='gpt-4o',temperature=0.3,api_key=os.environ.get('API_KEY',default='secret key'))