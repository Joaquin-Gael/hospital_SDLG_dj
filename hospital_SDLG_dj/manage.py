import os
import sys
from threading import Thread
import subprocess
import socket
import psutil
from concurrent.futures import ThreadPoolExecutor

def is_port_in_use(port):
    """Comprueba si un puerto está en uso."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        in_use = s.connect_ex(('127.0.0.1', port)) == 0
        if in_use:
            print(f"El puerto {port} ya está en uso.")
        return in_use

def kill_process_using_port(port):
    """Detiene el proceso que utiliza el puerto especificado."""
    for conn in psutil.net_connections():
        try:
            if conn.laddr.port == port and conn.pid != 0:  # Añadir condición para evitar PID 0
                process = psutil.Process(conn.pid)
                process.terminate()
                process.wait()  # Esperar a que el proceso termine
                print(f"Proceso con PID {conn.pid} detenido en el puerto {port}.")
        except psutil.NoSuchProcess:
            # El proceso ya no existe, continuar con el siguiente
            pass
        except psutil.AccessDenied:
            # No se tienen permisos para terminar el proceso, continuar con el siguiente
            print(f"No se tienen permisos para detener el proceso con PID {conn.pid}.")

def run_streamlit_server(port):
    streamlit_command = f"streamlit run chatbot/streamlit_app/chatbot_logic.py --server.port {port}"
    subprocess.run(streamlit_command, shell=True)

def check_and_kill_ports(ports):
    """Verifica y mata los procesos en los puertos especificados."""
    
    # Crea un ThreadPoolExecutor para gestionar múltiples subprocesos.
    with ThreadPoolExecutor() as executor:
        
        # Crea una lista de futuros (future objects), cada uno representando
        # la ejecución asíncrona de la función `kill_process_if_in_use` para
        # cada puerto en la lista `ports`.
        futures = [executor.submit(kill_process_if_in_use, port) for port in ports]
        
        # Itera sobre la lista de futuros para esperar a que todas las tareas
        # asíncronas terminen. La llamada a `future.result()` bloquea hasta que
        # la tarea correspondiente haya terminado.
        for future in futures:
            future.result()  # Espera a que todas las tareas terminen

def kill_process_if_in_use(port):
    """Mata el proceso si el puerto está en uso."""
    if is_port_in_use(port):
        kill_process_using_port(port)

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

    # Verificar y matar procesos en puertos del 8502 al 8510 y el puerto 8501
    ports_to_check = list(range(8501, 8511))
    check_and_kill_ports(ports_to_check)

    # Arranca el servidor de Streamlit en el puerto 8501
    #streamlit_thread = Thread(target=run_streamlit_server, args=(8501,))
    #streamlit_thread.daemon = True
    #streamlit_thread.start()

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
