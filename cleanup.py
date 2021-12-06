import logging
import subprocess
# Importo el resto de ficheros del programa
from init_logs import init_logs

# Configuración de los logs
init_logs()

# Punto de entrada
def cleanup(CONFIG_FILE):
    _cleanup_qcows()
    _cleanup_xmls()
    _cleanup_config(CONFIG_FILE)

def _cleanup_qcows():
    logging.info(
        f"Borrando ficheros qcows de ejecuciones anteriores (si existiesen)...")
    i = 1
    while i <= 5:
        subprocess.call(["rm", f"s{i}.qcow2"], stderr=subprocess.DEVNULL)
        i += 1
    logging.info(
        f"Borrados los ficheros qcows de ejecuciones anteriores")

def _cleanup_xmls():
    logging.info(
        f"Borrando ficheros xmls de ejecuciones anteriores (si existiesen)...")
    i = 1
    while i <= 5:
        subprocess.call(["rm", f"s{i}.xml"], stderr=subprocess.DEVNULL)
        i += 1
    logging.info(
        f"Borrados los ficheros xmls de ejecuciones anteriores")

def _cleanup_config(CONFIG_FILE):
    logging.info(
        f"Borrando fichero json de configuración de ejecuciones anteriores (si existiese)...")
    subprocess.call(["rm", CONFIG_FILE], stderr=subprocess.DEVNULL)
    logging.info(
        f"Borrado fichero json de configuración de ejecuciones anteriores")
