# -*- coding: utf-8 -*-

import subprocess
import os
import time

# Importo el resto de ficheros del programa
from logs import init_logs, log_error, log_warn, log_info

# Configuración de los logs
init_logs()

# Punto de entrada
def launch(num_serv):
    log_info("Procediendo con el arranque del escenario...")
    _launch_vm_manager()
    _launch_vms(num_serv)
    _launch_lb()
    _open_vms_console(num_serv)
    _open_lb_console()
    log_info("Esperando a que las máquinas virtuales acaben de arrancar...") # TODO después de esto da unos warnings de virsh
    time.sleep(60)
    log_info("El escenario ha sido arrancado")

## TODO por aqui da un warning del virt-viewer

def _launch_vm_manager():
    log_info("Arrancando el gestor de máquinas virtuales...")
    #os.environ["HOME"] = "/mnt/tmp" check what we do with this
    subprocess.call(["sudo", "virt-manager"], stderr=subprocess.DEVNULL)
    log_info("Arrancado el gestor de máquinas virtuales")

def _launch_vms(num_serv):
    log_info(f"Arrancando los {num_serv} servidores en forma de máquinas virtuales...")
    i = 1
    while i <= num_serv:
        subprocess.call(["sudo", "virsh", "define", f"s{i}.xml"], stderr=subprocess.DEVNULL)
        subprocess.call(["sudo", "virsh", "start", f"s{i}"], stderr=subprocess.DEVNULL)
        i += 1
    log_info(f"Arrancados los {num_serv} servidores en forma de máquinas virtuales")

def _launch_lb():
    log_info("Arrancando el balanceador de carga en forma de máquina virtual...")
    subprocess.call(["sudo", "virsh", "define", "lb.xml"], stderr=subprocess.DEVNULL)
    subprocess.call(["sudo", "virsh", "start", f"lb"], stderr=subprocess.DEVNULL)
    log_info("Arrancado el balanceador de carga en forma de máquina virtual")

def _open_vms_console(num_serv):
    log_info(f"Abriendo las {num_serv} consolas de los servidores...")
    i = 1
    while i <= num_serv:
        subprocess.Popen(["virt-viewer", f"s{i}"])
        i += 1
    log_info(f"Abiertas las {num_serv} consolas de los servidores")
    
def _open_lb_console():
    log_info("Abriendo la consola del balanceador de carga...")
    subprocess.Popen(["virt-viewer", "lb"])
    log_info(f"Abiertas la consola del balanceador de carga")
