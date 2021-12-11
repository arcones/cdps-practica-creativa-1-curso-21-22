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
    log_info("Configurando las máquinas virtuales...")

    servers_and_lb = get_scenario_machines_list(num_serv)

    _update_hostname(servers_and_lb)
    _update_hosts(servers_and_lb)
    _update_server_network_interfaces(num_serv)
    _update_lb_network_interface()

    log_info("El escenario ha sido configurado")
    

def _update_hostname(domain_list):
    subprocess.call(["mkdir", "-p", TMP_DIR])
    for domain in domain_list:
        with open(f"{TMP_DIR}/hostname", 'w') as hostname:
            hostname.write(f"{domain}\n")
        subprocess.call(["sudo", "virt-copy-in", "-a", f"{domain}.qcow2", f"{TMP_DIR}/hostname", "/etc"])
        subprocess.call(["sudo", "virt-cat", "-a", f"{domain}.qcow2", "/etc/hostname"]) # TODO remove
    subprocess.call(["rm", "-rf", TMP_DIR])

def _update_hosts(domain_list):
    subprocess.call(["mkdir", "-p", TMP_DIR])
    for domain in domain_list:
        with open(f"{TMP_DIR}/hosts", 'w') as hosts:
            hosts.write(f"127.0.1.1  {domain}\n")
        subprocess.call(["sudo", "virt-copy-in", "-a", f"{domain}.qcow2", f"{TMP_DIR}/hosts", "/etc"])
        subprocess.call(["sudo", "virt-cat", "-a", f"{domain}.qcow2", "/etc/hosts"]) # TODO remove
    subprocess.call(["rm", "-rf", TMP_DIR])

def _update_server_network_interfaces(num_serv):
    subprocess.call(["mkdir", "-p", TMP_DIR])
    i = 1
    while i <= num_serv:
        with open(f"{TMP_DIR}/interfaces", 'w') as interfaces:
            interfaces.write(f"""
            auto eth1
            iface eth1 inet static
                address 10.10.2.1{i}
                netmask 255.255.255.0
                up route add default via 10.10.2.1 dev eth1
            """)
        subprocess.call(["sudo", "virt-copy-in", "-a", f"s{i}.qcow2", f"{TMP_DIR}/interfaces", "/etc/network/"])
        subprocess.call(["sudo", "virt-cat", "-a", f"s{i}.qcow2", "/etc/network/interfaces"]) # TODO remove
        i += 1
    subprocess.call(["rm", "-rf", TMP_DIR])

def _update_lb_network_interface():
    subprocess.call(["mkdir", "-p", TMP_DIR])
    with open(f"{TMP_DIR}/interfaces", 'w') as interfaces:
        interfaces.write(f"""
        auto eth0
        iface eth0 inet static
            address 10.10.1.1
            netmask 255.255.255.0
            
        auto eth1
        iface eth0 inet static
            address 10.10.2.1
            netmask 255.255.255.0
        """)
    subprocess.call(["sudo", "virt-copy-in", "-a", f"lb.qcow2", f"{TMP_DIR}/interfaces", "/etc/network/"])
    subprocess.call(["sudo", "virt-cat", "-a", f"lb.qcow2", "/etc/network/interfaces"]) # TODO remove

    with open(f"{TMP_DIR}/sysctl.conf", 'w') as sysctl:
        sysctl.write("net.ipv4.ip_forward=1\n")
    subprocess.call(["sudo", "virt-copy-in", "-a", f"lb.qcow2", f"{TMP_DIR}/sysctl.conf", "/etc"])
    subprocess.call(["sudo", "virt-cat", "-a", f"lb.qcow2", "/etc/sysctl.conf"]) # TODO remove

    subprocess.call(["rm", "-rf", TMP_DIR])
