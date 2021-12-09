# -*- coding: utf-8 -*-

import subprocess
# Importo el resto de ficheros del programa
from logs import init_logs, log_error, log_warn, log_info

# Configuración de los logs
init_logs()

# Punto de entrada
def release(CONFIG_FILE, num_serv):
    _destroy_vms(num_serv)
    _destroy_lb()
    _cleanup_qcows()
    _cleanup_xmls()
    _cleanup_config(CONFIG_FILE)
    _cleanup_bridges()


def _destroy_vms(num_serv):
    log_info(f"Destruyendo los {num_serv} servidores en forma de máquinas virtuales...")
    i = 1
    while i <= num_serv:
        subprocess.call(["sudo", "virsh", "destroy", f"s{i}"])
        i += 1
    log_info(f"Destruidos los {num_serv} servidores en forma de máquinas virtuales")

def _destroy_lb():
    log_info("Destruyendo el balanceador de carga en forma de máquina virtual...")
    subprocess.call(["sudo", "virsh", "destroy", "lb"], stderr=subprocess.DEVNULL)
    log_info("Destruido el balanceador de carga en forma de máquina virtual")


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
    subprocess.call(["sudo", "ip", "link", "set", "LAN1", "down"], stderr=subprocess.DEVNULL)
    subprocess.call(["sudo", "brctl", "delbr", "LAN1"], stderr=subprocess.DEVNULL)
    subprocess.call(["sudo", "ip", "link", "set", "LAN2", "down"], stderr=subprocess.DEVNULL)
    subprocess.call(["sudo", "brctl", "delbr", "LAN2"], stderr=subprocess.DEVNULL)
    log_info("Borrados bridges de ejecuciones anteriores")
