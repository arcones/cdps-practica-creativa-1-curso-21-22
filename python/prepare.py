# -*- coding: utf-8 -*-

import json
import os
import subprocess

from configure import configure
from release import release


def prepare(CONFIG_FILE, num_serv):
    _check_requirements_are_downloaded()
    _save_config_file(CONFIG_FILE, num_serv)
    _create_mv_qcows(num_serv)
    _create_lb_qcow()
    _create_mv_xml(num_serv)
    _create_lb_xml()
    _create_bridges()

    configure(num_serv)
    print('\033[92m' + "El escenario ha sido preparado" + '\033[0m')


def _check_requirements_are_downloaded():
    print('\033[92m' + "Comprobando que los ficheros necesarios para preparar el escenario están presentes..." + '\033[0m')
    if not os.path.isfile('./cdps-vm-base-pc1.qcow2') or not os.path.isfile('./plantilla-vm-pc1.xml'):
        print('\033[91m' + "Los ficheros necesarios para preparar el escenario no están presentes, ejecute la orden download para obtenerlos" + '\033[0m')
        raise ValueError()
    print('\033[92m' + "Los ficheros necesarios están presentes" + '\033[0m')


def _clean_up_from_previous_runs():
    print('\033[92m' + "Borrando ficheros de configuración de ejecuciones anteriores..." + '\033[0m')
    i = 1
    while i <= 5:
        with open(os.devnull, 'w') as devnull:
            subprocess.call(["rm", f"s{i}.qcow2"])
            subprocess.call(["rm", f"s{i}.xml"])
        i += 1
    print('\033[92m' + "Borrandos los ficheros de configuración de ejecuciones anteriores" + '\033[0m')


def _save_config_file(CONFIG_FILE, num_serv):
    print('\033[92m' + f"Corriendo la orden prepare con num_serv={num_serv}" + '\033[0m')
    auto_p2_json = open(CONFIG_FILE, "w")
    num_serv_as_json = json.dumps({"num_serv": num_serv}, indent=4)
    auto_p2_json.write(num_serv_as_json)
    auto_p2_json.close()
    print('\033[92m' + "El fichero json de configuración ha sido almacenado" + '\033[0m')


def _create_mv_qcows(num_serv):
    print('\033[92m' + "Creando los ficheros qcow2 requeridos para los servidores..." + '\033[0m')
    i = 1
    while i <= num_serv:
        print('\033[92m' + f"Creando el fichero qcow2 de la máquina {i}..." + '\033[0m')
        subprocess.call(["qemu-img", "create", "-f", "qcow2", "-b", "cdps-vm-base-pc1.qcow2", f"s{i}.qcow2"])
        print('\033[92m' + f"Creado el fichero qcow2 de la máquina {i}" + '\033[0m')
        i += 1

    print('\033[92m' + "Los ficheros qcow2 requeridos para los servidores han sido creados" + '\033[0m')


def _create_mv_xml(num_serv):
    print('\033[92m' + "Creando los ficheros xml de configuración requeridos para los servidores..." + '\033[0m')
    i = 1
    while i <= num_serv:
        print('\033[92m' + f"Creando el fichero xml de configuración de la máquina {i}..." + '\033[0m')
        subprocess.call(["cp", "plantilla-vm-pc1.xml", f"s{i}.xml"])

        with open(f"s{i}.xml", "r") as xml:
            xml_content = xml.read()

        xml_content = xml_content.replace('<name>XXX</name>', f'<name>s{i}</name>')
        xml_content = xml_content.replace('/mnt/tmp/XXX/XXX.qcow2', f'{os.getcwd()}/s{i}.qcow2')
        xml_content = xml_content.replace("bridge='XXX'", f"bridge='LAN2'")

        with open(f"s{i}.xml", 'w') as xml:
            xml.write(xml_content)

        print('\033[92m' + f"Creado el fichero xml de configuración de la máquina {i}" + '\033[0m')
        i += 1

    print('\033[92m' + "Los ficheros xml de configuración requeridos para los servidores han sido creados" + '\033[0m')


def _create_lb_qcow():
    print('\033[92m' + "Creando el fichero qcow2 requerido para el balanceador de carga..." + '\033[0m')
    subprocess.call(["qemu-img", "create", "-f", "qcow2", "-b", "cdps-vm-base-pc1.qcow2", "lb.qcow2"])
    print('\033[92m' + "El fichero qcow2 requerido para el balanceador de carga ha sido creado" + '\033[0m')


def _create_lb_xml():
    print('\033[92m' + "Creando el fichero de configuración del balanceador de carga..." + '\033[0m')
    subprocess.call(["cp", "plantilla-vm-pc1.xml", f"lb.xml"])

    with open(f"lb.xml", "r") as xml:
        xml_content = xml.read()

    xml_content = xml_content.replace('<name>XXX</name>', f'<name>lb</name>')
    xml_content = xml_content.replace('/mnt/tmp/XXX/XXX.qcow2', f'{os.getcwd()}/lb.qcow2')

    interface_template = """
    <interface type='bridge'>
      <source bridge='XXX'/>
      <model type='virtio'/>
    </interface>
    """

    interfaces_required = """
    <interface type='bridge'>
      <source bridge='LAN1'/>
      <model type='virtio'/>
    </interface>
    <interface type='bridge'>
      <source bridge='LAN2'/>
      <model type='virtio'/>
    </interface>
    """

    xml_content = xml_content.replace(interface_template, interfaces_required)

    with open(f"lb.xml", 'w') as xml:
        xml.write(xml_content)

    print('\033[92m' + "El fichero xml de configuración requerido para el balanceador de carga ha sido creado" + '\033[0m')


def _create_bridges():
    print('\033[92m' + f"Creando los bridges correspondientes a las dos redes virtuales..." + '\033[0m')
    subprocess.call(["sudo", "brctl", "addbr", "LAN1"])
    subprocess.call(["sudo", "brctl", "addbr", "LAN2"])
    subprocess.call(["sudo", "ifconfig", "LAN1", "up"])
    subprocess.call(["sudo", "ifconfig", "LAN2", "up"])
    print('\033[92m' + f"Creados los bridges correspondientes a las dos redes virtuales" + '\033[0m')
