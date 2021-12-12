# -*- coding: utf-8 -*-

import subprocess
from util import read_num_serv

def release(CONFIG_FILE):
    num_serv = read_num_serv(CONFIG_FILE)
    _destroy_vms(num_serv)
    _destroy_lb()
    _cleanup_qcows()
    _cleanup_xmls()
    _cleanup_config(CONFIG_FILE)
    _cleanup_bridges()


def _destroy_vms(num_serv):
    print("\033[92m" + f"Destruyendo los {num_serv} servidores en forma de máquinas virtuales..." + "\033[0m")
    i = 1
    while i <= num_serv:
        subprocess.call(["sudo", "virsh", "destroy", f"s{i}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.call(["sudo", "virsh", "undefine", f"s{i}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        i += 1
    print("\033[92m" + f"Destruidos los {num_serv} servidores en forma de máquinas virtuales" + "\033[0m")


def _destroy_lb():
    print("\033[92m" + "Destruyendo el balanceador de carga en forma de máquina virtual..." + "\033[0m")
    subprocess.call(["sudo", "virsh", "destroy", "lb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.call(["sudo", "virsh", "undefine", "lb"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("\033[92m" + "Destruido el balanceador de carga en forma de máquina virtual" + "\033[0m")


def _cleanup_qcows():
    print("\033[92m" + "Borrando ficheros qcows de ejecuciones anteriores (si existiesen)..." + "\033[0m")
    i = 1
    while i <= 5:
        subprocess.call(["rm", "-rf", f"s{i}.qcow2"])
        i += 1
    subprocess.call(["rm", "-rf", f"lb.qcow2"])
    print("\033[92m" + "Borrados los ficheros qcows de ejecuciones anteriores" + "\033[0m")


def _cleanup_xmls():
    print("\033[92m" + "Borrando ficheros xmls de ejecuciones anteriores (si existiesen)..." + "\033[0m")
    i = 1
    while i <= 5:
        subprocess.call(["rm", "-rf", f"s{i}.xml"])
        i += 1
    subprocess.call(["rm", "-rf", f"lb.xml"])
    print("\033[92m" + "Borrados los ficheros xmls de ejecuciones anteriores" + "\033[0m")


def _cleanup_config(CONFIG_FILE):
    print("\033[92m" + "Borrando fichero json de configuración de ejecuciones anteriores (si existiese)..." + "\033[0m")
    subprocess.call(["rm", CONFIG_FILE])
    print("\033[92m" + "Borrado fichero json de configuración de ejecuciones anteriores" + "\033[0m")


def _cleanup_bridges():
    print("\033[92m" + "Borrando bridges de ejecuciones anteriores (si existiese)..." + "\033[0m")
    subprocess.call(["sudo", "ip", "link", "set", "LAN1", "down"])
    subprocess.call(["sudo", "brctl", "delbr", "LAN1"])
    subprocess.call(["sudo", "ip", "link", "set", "LAN2", "down"])
    subprocess.call(["sudo", "brctl", "delbr", "LAN2"])
    print("\033[92m" + "Borrados bridges de ejecuciones anteriores" + "\033[0m")
