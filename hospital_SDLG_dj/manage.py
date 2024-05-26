#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from threading import Thread
import subprocess
import socket

def is_port_in_use(port):
    """Comprueba si un puerto está en uso."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def run_streamlit_server():
    streamlit_command = "streamlit run chatbot/streamlit_app/chatbot_logic.py"
    subprocess.run(streamlit_command, shell=True)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_SDLG_dj.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Verifica si el servidor de Streamlit ya está en ejecución
    if not is_port_in_use(8501):  # Cambia el número de puerto según sea necesario
        # Arranca el servidor de Streamlit en un hilo aparte
        streamlit_thread = Thread(target=run_streamlit_server)
        streamlit_thread.daemon = True
        streamlit_thread.start()

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
