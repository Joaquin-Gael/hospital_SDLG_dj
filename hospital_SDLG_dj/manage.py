import os
import sys
from threading import Thread
import subprocess
import socket
import psutil

def is_port_in_use(port):
    """Comprueba si un puerto está en uso."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

def kill_process_using_port(port):
    """Detiene el proceso que utiliza el puerto especificado."""
    for conn in psutil.net_connections():
        try:
            if conn.laddr.port == port and conn.pid != 0:  # Añadir condición para evitar PID 0
                process = psutil.Process(conn.pid)
                process.terminate()
                print(f"Proceso con PID {conn.pid} detenido.")
        except psutil.NoSuchProcess:
            # El proceso ya no existe, continuar con el siguiente
            pass
        except psutil.AccessDenied:
            # No se tienen permisos para terminar el proceso, continuar con el siguiente
            print(f"No se tienen permisos para detener el proceso con PID {conn.pid}.")

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
    
    # Verifica si el servidor de Streamlit ya está en ejecución en el puerto 8501
    if is_port_in_use(8501):
        print("El puerto 8501 ya está en uso.")
        # Detiene cualquier proceso que esté utilizando el puerto 8501
        kill_process_using_port(8501)
    
    # Arranca el servidor de Streamlit en un hilo aparte
    streamlit_thread = Thread(target=run_streamlit_server)
    streamlit_thread.daemon = True
    streamlit_thread.start()

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
