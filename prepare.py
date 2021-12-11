# -*- coding: utf-8 -*-

import subprocess
import os
import json

# Importo el resto de ficheros del programa
from release import release
from configure import configure
from logs import init_logs, log_error, log_warn, log_info

# Configuración de los logs
init_logs()

# Punto de entrada
def prepare(CONFIG_FILE, num_serv):
    log_warn("Liberando el escenario de ejecuciones anteriores...")
    release(CONFIG_FILE, num_serv)

    log_info("El escenario ha sido liberado, procediendo con la preparación...")
    _check_requirements_are_downloaded()
    _save_config_file(CONFIG_FILE, num_serv)
    _create_mv_qcows(num_serv)
    _create_lb_qcow()
    _create_mv_xml(num_serv) # TODO Create also the client C1
    _create_lb_xml()
    _create_bridges() #TODO this can be moved to configure py

    configure(num_serv)
    log_info("El escenario ha sido preparado")


def _check_requirements_are_downloaded():
    log_info("Comprobando que los ficheros necesarios para preparar el escenario están presentes...")
    if not os.path.isfile('./cdps-vm-base-pc1.qcow2') or not os.path.isfile('./plantilla-vm-pc1.xml'):
        log_error("Los ficheros necesarios para preparar el escenario no están presentes, ejecute la orden download para obtenerlos")
        raise ValueError()
    log_info("Los ficheros necesarios están presentes")


def _clean_up_from_previous_runs():
    log_info("Borrando ficheros de configuración de ejecuciones anteriores...")
    i = 1
    while i <= 5:
        with open(os.devnull, 'w') as devnull:
            subprocess.call(["rm", f"s{i}.qcow2"], stdout=devnull)
            subprocess.call(["rm", f"s{i}.xml"], stdout=devnull)
        i += 1
    log_info("Borrandos los ficheros de configuración de ejecuciones anteriores")

def _save_config_file(CONFIG_FILE, num_serv):
    log_info(f"Corriendo la orden prepare con num_serv={num_serv}")
    auto_p2_json = open(CONFIG_FILE, "w")
    num_serv_as_json = json.dumps({"num_serv": num_serv}, indent=4)
    auto_p2_json.write(num_serv_as_json)
    auto_p2_json.close()
    log_info("El fichero json de configuración ha sido almacenado")


def _create_mv_qcows(num_serv):
    log_info("Creando los ficheros qcow2 requeridos para los servidores...")
    i = 1
    while i <= num_serv:
        log_info(f"Creando el fichero qcow2 de la máquina {i}...")
        subprocess.call(["qemu-img", "create", "-f", "qcow2",
                        "-b", "cdps-vm-base-pc1.qcow2", f"s{i}.qcow2"], stdout=subprocess.DEVNULL)
        log_info(f"Creado el fichero qcow2 de la máquina {i}")
        i += 1

    log_info("Los ficheros qcow2 requeridos para los servidores han sido creados")


def _create_mv_xml(num_serv):
    log_info("Creando los ficheros xml de configuración requeridos para los servidores...")
    i = 1
    while i <= num_serv:
        log_info(f"Creando el fichero xml de configuración de la máquina {i}...")
        subprocess.call(["cp", "plantilla-vm-pc1.xml", f"s{i}.xml"])

        with open(f"s{i}.xml", "r") as xml:
            xml_content = xml.read()

        xml_content = xml_content.replace('<name>XXX</name>', f'<name>s{i}</name>')
        xml_content = xml_content.replace('/mnt/tmp/XXX/XXX.qcow2',f'{os.getcwd()}/s{i}.qcow2')
        xml_content = xml_content.replace("bridge='XXX'", f"bridge='LAN2'")
        
        with open(f"s{i}.xml", 'w') as xml:
            xml.write(xml_content)

        log_info(f"Creado el fichero xml de configuración de la máquina {i}")
        i += 1

    log_info("Los ficheros xml de configuración requeridos para los servidores han sido creados")

def _create_lb_qcow():
    log_info("Creando el fichero qcow2 requerido para el balanceador de carga...")
    subprocess.call(["qemu-img", "create", "-f", "qcow2", "-b", "cdps-vm-base-pc1.qcow2", f"lb.qcow2"], stdout=subprocess.DEVNULL)
    log_info("El fichero qcow2 requerido para el balanceador de carga ha sido creado")

def _create_lb_xml():
    log_info("Creando el fichero de configuración del balanceador de carga...")
    subprocess.call(["cp", "plantilla-vm-pc1.xml", f"lb.xml"])

    with open(f"lb.xml", "r") as xml:
        xml_content = xml.read()

    xml_content = xml_content.replace('<name>XXX</name>', f'<name>lb</name>')
    xml_content = xml_content.replace('/mnt/tmp/XXX/XXX.qcow2',f'{os.getcwd()}/lb.qcow2')

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


    log_info("El fichero xml de configuración requerido para el balanceador de carga ha sido creado")

def _create_bridges():
    log_info(f"Creando los bridges correspondientes a las dos redes virtuales...")
    subprocess.call(["sudo", "brctl", "addbr", "LAN1"])
    subprocess.call(["sudo", "brctl", "addbr", "LAN2"])
    subprocess.call(["sudo", "ifconfig", "LAN1", "up"])
    subprocess.call(["sudo", "ifconfig", "LAN2", "up"])
    log_info(f"Creados los bridges correspondientes a las dos redes virtuales")
