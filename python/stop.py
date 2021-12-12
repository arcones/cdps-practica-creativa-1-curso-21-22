# -*- coding: utf-8 -*-

import subprocess
import time


def stop(num_serv):
    print('\033[92m' + "Procediendo con la parada del escenario..." + '\033[0m')
    _stop_servers(num_serv)
    _stop_lb()
    _wait_till_servers_fully_stopped(num_serv)
    _wait_till_lb_fully_stopped()
    print('\033[92m' + "El escenario ha sido parado" + '\033[0m')


def _stop_servers(num_serv):
    print('\033[92m' + f"Iniciando la parada de los {num_serv} servidores en forma de máquinas virtuales..." + '\033[0m')
    i = 1
    while i <= num_serv:
        subprocess.call(["sudo", "virsh", "shutdown", f"s{i}"])
        i += 1


def _stop_lb():
    print('\033[92m' + f"Iniciando la parada del balanceador de carga en forma de máquina virtual..." + '\033[0m')
    subprocess.call(["sudo", "virsh", "shutdown", "lb"])


def _wait_till_servers_fully_stopped(num_serv):
    i = 1
    while i <= num_serv:
        command = ['sudo', 'virsh', 'domstate', f"s{i}"]
        while (subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0].decode('UTF-8').strip() != "shut off"):
            time.sleep(5)
        i += 1
    print('\033[92m' + "Los servidores se han detenido por completo" + '\033[0m')


def _wait_till_lb_fully_stopped():
    command = ['sudo', 'virsh', 'domstate', "lb"]
    while (subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0].decode('UTF-8').strip() != "shut off"):
        time.sleep(5)
    print('\033[92m' + "El balancedor de carga se ha detenido por completo" + '\033[0m')
