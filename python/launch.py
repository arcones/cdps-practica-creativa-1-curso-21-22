# -*- coding: utf-8 -*-

import subprocess
import time


def launch(num_serv):
    print('\033[92m' + "Procediendo con el arranque del escenario..." + '\033[0m')
    _launch_vm_manager()
    _launch_vms(num_serv)
    _launch_lb()
    _open_vms_console(num_serv)
    _open_lb_console()
    print('\033[92m' + "Esperando a que las máquinas virtuales acaben de arrancar..." + '\033[0m')
    time.sleep(30)
    print('\033[92m' + "El escenario ha sido arrancado" + '\033[0m')

def _launch_vm_manager():
    print('\033[92m' + "Arrancando el gestor de máquinas virtuales..." + '\033[0m')
    subprocess.call(["sudo", "virt-manager"])
    print('\033[92m' + "Arrancado el gestor de máquinas virtuales" + '\033[0m')


def _launch_vms(num_serv):
    print('\033[92m' + f"Arrancando los {num_serv} servidores en forma de máquinas virtuales..." + '\033[0m')
    i = 1
    while i <= num_serv:
        subprocess.call(["sudo", "virsh", "define", f"s{i}.xml"], stderr=subprocess.DEVNULL)
        subprocess.call(["sudo", "virsh", "start", f"s{i}"])
        i += 1
    print('\033[92m' + f"Arrancados los {num_serv} servidores en forma de máquinas virtuales" + '\033[0m')


def _launch_lb():
    print('\033[92m' + "Arrancando el balanceador de carga en forma de máquina virtual..." + '\033[0m')
    subprocess.call(["sudo", "virsh", "define", "lb.xml"], stderr=subprocess.DEVNULL)
    subprocess.call(["sudo", "virsh", "start", f"lb"])
    print('\033[92m' + "Arrancado el balanceador de carga en forma de máquina virtual" + '\033[0m')


def _open_vms_console(num_serv):
    print('\033[92m' + f"Abriendo las {num_serv} consolas de los servidores..." + '\033[0m')
    i = 1
    while i <= num_serv:
        subprocess.Popen(["virt-viewer", f"s{i}"], stderr=subprocess.DEVNULL)
        i += 1
    print('\033[92m' + f"Abiertas las {num_serv} consolas de los servidores" + '\033[0m')


def _open_lb_console():
    print('\033[92m' + "Abriendo la consola del balanceador de carga..." + '\033[0m')
    subprocess.Popen(["virt-viewer", "lb"], stderr=subprocess.DEVNULL)
    print('\033[92m' + f"Abiertas la consola del balanceador de carga" + '\033[0m')
