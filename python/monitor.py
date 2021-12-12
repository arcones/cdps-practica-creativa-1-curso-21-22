# -*- coding: utf-8 -*-

import subprocess
from util import read_num_serv, get_scenario_machines_list

def monitor(CONFIG_FILE, domain):
    print("\033[92m" + "Arrancando la monitorización del escenario en un nuevo terminal..." + "\033[0m")
    if not domain:
        process = subprocess.Popen(["gnome-terminal", "-e", "watch sudo virsh list"], stdout=subprocess.DEVNULL)
    else: 
        machines = get_scenario_machines_list(read_num_serv(CONFIG_FILE))
        if domain not in machines:
            print("\033[91m" + f"El dominio indicado no existe, por favor ejecute el comando con uno de {machines}" + "\033[0m")
            raise ValeError()
        process = subprocess.Popen(["gnome-terminal", "-e", f"watch sudo virsh dominfo {domain}"], stdout=subprocess.DEVNULL) 
    print("\033[92m" + "La monitorización del escenario ha sido arrancado" + "\033[0m")
