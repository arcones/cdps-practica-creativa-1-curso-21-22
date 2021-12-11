# -*- coding: utf-8 -*-

import subprocess
import time

# Importo el resto de ficheros del programa
from logs import init_logs, log_error, log_warn, log_info

# Configuración de los logs
init_logs()

# Punto de entrada
def stop(num_serv):
    log_info("Procediendo con la parada del escenario...")
    _stop_servers(num_serv)
    _stop_lb()
    _wait_till_servers_fully_stopped(num_serv)
    _wait_till_lb_fully_stopped()
    log_info("El escenario ha sido parado")


def _stop_servers(num_serv):
    log_info(f"Iniciando la parada de los {num_serv} servidores en forma de máquinas virtuales...")
    i = 1
    while i <= num_serv:
        subprocess.call(["sudo", "virsh", "shutdown", f"s{i}"]) #TODO until machines are not servers_fully launched they will not stop!
        i += 1

def _stop_lb():
    log_info(f"Iniciando la parada del balanceador de carga en forma de máquina virtual...")
    subprocess.call(["sudo", "virsh", "shutdown", "lb"])

def _wait_till_servers_fully_stopped(num_serv):
    i = 1
    while i <= num_serv:
        command = ['sudo', 'virsh', 'domstate', f"s{i}"]
        while (subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0].decode('UTF-8').strip() != "shut off"):
            time.sleep(5)
        i += 1
    log_info("Los servidores se han detenido por completo")

def _wait_till_lb_fully_stopped():
    command = ['sudo', 'virsh', 'domstate', "lb"]
    while (subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0].decode('UTF-8').strip() != "shut off"):
        time.sleep(5)
    log_info("El balancedor de carga se ha detenido por completo")
