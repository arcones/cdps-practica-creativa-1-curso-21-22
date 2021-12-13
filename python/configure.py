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
    _update_lb_network_interface()
    _update_host_configuration()
    _update_indexes(num_serv)
    _update_lb_haproxy(num_serv)

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


def _update_lb_network_interface():
    subprocess.call(["mkdir", "-p", TMP_DIR])
    with open(f"{TMP_DIR}/interfaces", 'w') as interfaces:
        interfaces.write("auto eth0\n")
        interfaces.write("iface eth0 inet static\n")
        interfaces.write("\taddress 10.10.1.1\n")
        interfaces.write("\tnetmask 255.255.255.0\n\n")
        interfaces.write("auto eth1\n")
        interfaces.write("iface eth1 inet static\n")
        interfaces.write("\taddress 10.10.2.1\n")
        interfaces.write("\tnetmask 255.255.255.0\n")
    subprocess.call(["sudo", "virt-copy-in", "-a", f"lb.qcow2", f"{TMP_DIR}/interfaces", "/etc/network/"])

    with open(f"{TMP_DIR}/sysctl.conf", 'w') as sysctl:
        sysctl.write("net.ipv4.ip_forward=1\n")
    subprocess.call(["sudo", "virt-copy-in", "-a", f"lb.qcow2", f"{TMP_DIR}/sysctl.conf", "/etc"])

    subprocess.call(["rm", "-rf", TMP_DIR])


def _update_lb_haproxy(num_serv):
    subprocess.call(["mkdir", "-p", TMP_DIR])
    with open(f"{TMP_DIR}/haproxy.cfg", 'a') as haproxy:
        haproxy.write("global\n")
        haproxy.write("log /dev/log	local0\n")
        haproxy.write("log /dev/log	local1 notice\n")
        haproxy.write("chroot /var/lib/haproxy\n")
        haproxy.write("stats socket /run/haproxy/admin.sock mode 660 level admin expose-fd listeners\n")
        haproxy.write("stats timeout 30s\n")
        haproxy.write("user haproxy\n")
        haproxy.write("group haproxy\n")
        haproxy.write("daemon\n")
        haproxy.write("ca-base /etc/ssl/certs\n")
        haproxy.write("crt-base /etc/ssl/private\n")
        haproxy.write(
            "ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384\n")
        haproxy.write(
            "ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256\n")
        haproxy.write("ssl-default-bind-options ssl-min-ver TLSv1.2 no-tls-tickets\n")
        haproxy.write("defaults\n")
        haproxy.write("log	global\n")
        haproxy.write("mode	http\n")
        haproxy.write("option	httplog\n")
        haproxy.write("option	dontlognull\n")
        haproxy.write("timeout connect 5000\n")
        haproxy.write("timeout client  50000\n")
        haproxy.write("timeout server  50000\n")
        haproxy.write("errorfile 400 /etc/haproxy/errors/400.http\n")
        haproxy.write("errorfile 403 /etc/haproxy/errors/403.http\n")
        haproxy.write("errorfile 408 /etc/haproxy/errors/408.http\n")
        haproxy.write("errorfile 500 /etc/haproxy/errors/500.http\n")
        haproxy.write("errorfile 502 /etc/haproxy/errors/502.http\n")
        haproxy.write("errorfile 503 /etc/haproxy/errors/503.http\n")
        haproxy.write("errorfile 504 /etc/haproxy/errors/504.http\n")
        haproxy.write("frontend lb\n")
        haproxy.write("\tbind *:80\n")
        haproxy.write("\tmode http\n")
        haproxy.write("\tdefault_backend webservers\n")
        haproxy.write("backend webservers\n")
        haproxy.write("\tmode http\n")
        haproxy.write("\tbalance roundrobin\n")
        i = 1
        while i <= num_serv:
            haproxy.write(f"\tserver s{i} 10.10.2.1{i}:80 check\n")
            i += 1

    subprocess.call(["sudo", "virt-copy-in", "-a", f"lb.qcow2", f"{TMP_DIR}/haproxy.cfg", "/etc/haproxy/"])

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
