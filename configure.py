# -*- coding: utf-8 -*-

import subprocess
from util import get_scenario_machines_list

# Importo el resto de ficheros del programa
from logs import init_logs, log_error, log_warn, log_info

# Configuración de los logs
init_logs()

TMP_DIR = "tmp_files"

# Punto de entrada
def configure(num_serv):
    log_info("Configurando las máquinas virtuales arrancadas...")
    servers_and_lb = get_scenario_machines_list(num_serv)

    _update_hostname(servers_and_lb)

    log_info("El escenario ha sido configurado")
    

def _update_hostname(domain_list):
    subprocess.call(["mkdir", "-p", TMP_DIR])
    for domain in domain_list:
        with open(f"{TMP_DIR}/hostname", 'w') as hostname:
            hostname.write(f"127.0.1.1   {domain}")
        subprocess.call(["sudo", "virt-copy-in", "-a", f"{domain}.qcow2", f"{TMP_DIR}/hostname", "/etc"])
        subprocess.call(["sudo", "virt-cat", "-a", f"{domain}.qcow2", "/etc/hostname"])
        subprocess.call(["echo", "\n\n"])
    subprocess.call(["rm", "-rf", TMP_DIR])
