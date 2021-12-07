# -*- coding: utf-8 -*-

import subprocess

# Importo el resto de ficheros del programa
from logs import init_logs, log_error, log_warn, log_info

# Configuración de los logs
init_logs()

# Punto de entrada
def stop(num_serv):
    _stop_servers(num_serv)
    _stop_lb()


def _stop_servers(num_serv):
    log_info(f"Parando los {num_serv} servidores en forma de máquinas virtuales...")
    i = 1
    while i <= num_serv:
        subprocess.call(["sudo", "virsh", "shutdown", f"s{i}"])
        i += 1
    log_info(f"Parados los {num_serv} servidores en forma de máquinas virtuales")

def _stop_lb():
    log_info(f"Parando el balanceador de carga en forma de máquina virtual...")
    subprocess.call(["sudo", "virsh", "shutdown", "lb"])
    log_info(f"Parado el balanceador de carga en forma de máquina virtual")
