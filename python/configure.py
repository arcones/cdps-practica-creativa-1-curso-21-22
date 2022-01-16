# -*- coding: utf-8 -*-

import subprocess
from util import get_scenario_machines_list

TMP_DIR = "tmp_files"

def configure(num_serv):
    print('\033[92m' + "Configurando las máquinas virtuales..." + '\033[0m')

    servers_and_lb = get_scenario_machines_list(num_serv)

    _update_hostname(servers_and_lb)
    _update_hosts(servers_and_lb)
    _update_server_network_interfaces(num_serv)
    #_update_host_configuration()
    _update_indexes(num_serv)

    print('\033[92m' + "El escenario ha sido configurado" + '\033[0m')


def _update_hostname(domain_list):
    subprocess.call(["mkdir", "-p", TMP_DIR])
    for domain in domain_list:
        with open(f"{TMP_DIR}/hostname", 'w') as hostname:
            hostname.write(f"{domain}\n")
        subprocess.call(["sudo", "virt-copy-in", "-a", f"{domain}.qcow2", f"{TMP_DIR}/hostname", "/etc"])
    subprocess.call(["rm", "-rf", TMP_DIR])


def _update_hosts(domain_list):
    subprocess.call(["mkdir", "-p", TMP_DIR])
    for domain in domain_list:
        with open(f"{TMP_DIR}/hosts", 'w') as hosts:
            hosts.write(f"127.0.1.1  {domain}\n")
        subprocess.call(["sudo", "virt-copy-in", "-a", f"{domain}.qcow2", f"{TMP_DIR}/hosts", "/etc"])


def _update_server_network_interfaces(num_serv):
    subprocess.call(["mkdir", "-p", TMP_DIR])
    i = 1
    while i <= num_serv:
        with open(f"{TMP_DIR}/interfaces", 'w') as interfaces:
            interfaces.write("auto eth0\n")
            interfaces.write("iface eth0 inet static\n")
            interfaces.write(f"\taddress 10.10.2.1{i}\n")
            interfaces.write("\tnetmask 255.255.255.0\n")
            interfaces.write("\tgateway 10.10.2.1\n")
            interfaces.write("\tup route add default via 10.10.2.1 dev eth0\n")
        subprocess.call(["sudo", "virt-copy-in", "-a", f"s{i}.qcow2", f"{TMP_DIR}/interfaces", "/etc/network/"])
        i += 1
    subprocess.call(["rm", "-rf", TMP_DIR])


def _update_host_configuration():
    subprocess.call(["sudo", "ifconfig", "LAN1", "10.10.1.3/24"])
    subprocess.call(["sudo", "ip", "route", "add", "10.10.0.0/16", "via", "10.10.1.1"])

def _update_indexes(num_serv):
    subprocess.call(["mkdir", "-p", TMP_DIR])
    i = 1
    while i <= num_serv:
        with open(f"{TMP_DIR}/index.html", 'w') as interfaces:
            interfaces.write(f"S{i}\n")
        subprocess.call(["sudo", "virt-copy-in", "-a", f"s{i}.qcow2", f"{TMP_DIR}/index.html", "/var/www/html/"])
        i += 1
    subprocess.call(["rm", "-rf", TMP_DIR])
