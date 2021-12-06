import subprocess
import os
import json

# Importo el resto de ficheros del programa
from cleanup import cleanup
from logs import init_logs, log_error, log_warn, log_info

# Configuración de los logs
init_logs()

# Punto de entrada
def prepare(CONFIG_FILE, num_serv):
    cleanup(CONFIG_FILE)
    _save_config_file(CONFIG_FILE, num_serv)
    _create_mv_qcows(num_serv)
    _create_lb_qcow()
    _create_mv_xml(num_serv) # TODO Create also the client C1
    _create_lb_xml()


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
    log_info("Limpiando ficheros de configuración de posibles ejecuciones pasadas")
    if os.path.exists(f'./{CONFIG_FILE}'):
        os.remove(f'./{CONFIG_FILE}')

    log_info(f"Corriendo la orden prepare con num_serv={num_serv}")
    auto_p2_json = open(CONFIG_FILE, "w")
    num_serv_as_json = json.dumps({"num_serv": num_serv}, indent=4)
    auto_p2_json.write(num_serv_as_json)
    auto_p2_json.close()
    log_info("El fichero json ha sido almacenado")


def _create_mv_qcows(num_serv):
    log_info("Creando los ficheros qcow2 requeridos para los servidores...")
    i = 1
    while i <= num_serv:
        log_info(f"Creando el fichero qcow2 de la máquina {i}")
        subprocess.call(["qemu-img", "create", "-f", "qcow2",
                        "-b", "cdps-vm-base-pc1.qcow2", f"s{i}.qcow2"], stdout=subprocess.DEVNULL)
        i += 1

    log_info("Los ficheros qcow2 requeridos para los servidores han sido creados")


def _create_mv_xml(num_serv):
    log_info("Creando los ficheros xml de configuración requeridos para los servidores...")
    i = 1
    while i <= num_serv:
        log_info(f"Creando el fichero xml de configuración de la máquina {i}")
        subprocess.call(["cp", "plantilla-vm-pc1.xml", f"s{i}.xml"])

        with open(f"s{i}.xml", "r") as xml:
            xml_content = xml.read()

        xml_content = xml_content.replace('<name>XXX</name>', f'<name>s{i}</name>')
        xml_content = xml_content.replace('/mnt/tmp/XXX/XXX.qcow2',f'{os.getcwd()}/s{i}.qcow2')
        xml_content = xml_content.replace("bridge='XXX'", f"bridge='LAN2'")
        
        with open(f"s{i}.xml", 'w') as xml:
            xml.write(xml_content)

        i += 1

    log_info("Los ficheros xml de configuración requeridos para los servidores han sido creados")

def _create_lb_qcow():
    log_info("Creando el fichero qcow2 requerido para el balanceador de carga...")
    subprocess.call(["qemu-img", "create", "-f", "qcow2", "-b", "cdps-vm-base-pc1.qcow2", f"lb.qcow2"], stdout=subprocess.DEVNULL)
    log_info("El fichero qcow2 requerido para el balanceador de carga ha sido creado")

def _create_lb_xml():
    log_info(f"Creando el fichero de configuración del balanceador de carga...")
    subprocess.call(["cp", "plantilla-vm-pc1.xml", f"lb.xml"])

    with open(f"lb.xml", "r") as xml:
        xml_content = xml.read()

    xml_content = xml_content.replace('<name>XXX</name>', f'<name>lb</name>')
    xml_content = xml_content.replace('/mnt/tmp/XXX/XXX.qcow2',f'{os.getcwd()}/lb.qcow2')
    xml_content = xml_content.replace("bridge='XXX'", f"bridge='LAN2'")
    
    with open(f"lb.xml", 'w') as xml:
        xml.write(xml_content)


    log_info("El fichero xml de configuración requerido han sido creado")
