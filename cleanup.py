import subprocess
# Importo el resto de ficheros del programa
from logs import init_logs, log_error, log_warn, log_info

# Configuración de los logs
init_logs()

# Punto de entrada
def cleanup(CONFIG_FILE):
    _cleanup_qcows()
    _cleanup_xmls()
    _cleanup_config(CONFIG_FILE)
    _cleanup_bridges()

def _cleanup_qcows():
    log_info("Borrando ficheros qcows de ejecuciones anteriores (si existiesen)...")
    i = 1
    while i <= 5:
        subprocess.call(["rm", f"s{i}.qcow2"], stderr=subprocess.DEVNULL)
        i += 1
    subprocess.call(["rm", f"lb.qcow2"], stderr=subprocess.DEVNULL)
    log_info("Borrados los ficheros qcows de ejecuciones anteriores")

def _cleanup_xmls():
    log_info("Borrando ficheros xmls de ejecuciones anteriores (si existiesen)...")
    i = 1
    while i <= 5:
        subprocess.call(["rm", f"s{i}.xml"], stderr=subprocess.DEVNULL)
        i += 1
    subprocess.call(["rm", f"lb.xml"], stderr=subprocess.DEVNULL)
    log_info("Borrados los ficheros xmls de ejecuciones anteriores")

def _cleanup_config(CONFIG_FILE):
    log_info("Borrando fichero json de configuración de ejecuciones anteriores (si existiese)...")
    subprocess.call(["rm", CONFIG_FILE], stderr=subprocess.DEVNULL)
    log_info("Borrado fichero json de configuración de ejecuciones anteriores")

def _cleanup_bridges():
    log_info("Borrando bridges de ejecuciones anteriores (si existiese)...")
    subprocess.call(["sudo", "ip", "link", "set", "LAN1", "down"], stdout=subprocess.DEVNULL)
    subprocess.call(["sudo", "brctl", "delbr", "LAN1"], stdout=subprocess.DEVNULL)
    subprocess.call(["sudo", "ip", "link", "set", "LAN2", "down"], stdout=subprocess.DEVNULL)
    subprocess.call(["sudo", "brctl", "delbr", "LAN2"], stdout=subprocess.DEVNULL)
    log_info("Borrados bridges de ejecuciones anteriores")
