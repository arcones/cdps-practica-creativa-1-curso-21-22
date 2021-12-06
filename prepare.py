import subprocess
import logging
import coloredlogs
import os
import json
from cleanup import cleanup

# Configuración de los logs
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG)
coloredlogs.DEFAULT_LEVEL_STYLES = {
    "warning": {"color": "orange", "bold": True},
    "success": {"color": "green", "bold": True},
    "error": {"color": "red", "bold": True},
}

coloredlogs.install()


def prepare(CONFIG_FILE, num_serv):
    cleanup(CONFIG_FILE)
    _save_config_file(CONFIG_FILE, num_serv)
    _create_qcows(num_serv)
    _create_templates(num_serv)


def _clean_up_from_previous_runs():
    logging.info(
        f"Borrando ficheros de configuración de ejecuciones anteriores...")
    i = 1
    while i <= 5:
        with open(os.devnull, 'w') as devnull:
            subprocess.call(["rm", f"s{i}.qcow2"], stdout=devnull)
            subprocess.call(["rm", f"s{i}.xml"], stdout=devnull)
        i += 1
    logging.info(
        f"Borrandos los ficheros de configuración de ejecuciones anteriores")


def _save_config_file(CONFIG_FILE, num_serv):
    logging.info(
        f"Limpiando ficheros de configuración de posibles ejecuciones pasadas")
    if os.path.exists(f'./{CONFIG_FILE}'):
        os.remove(f'./{CONFIG_FILE}')

    logging.info(f"Corriendo la orden prepare con num_serv={num_serv}")
    auto_p2_json = open(CONFIG_FILE, "w")
    num_serv_as_json = json.dumps({"num_serv": num_serv}, indent=4)
    auto_p2_json.write(num_serv_as_json)
    auto_p2_json.close()
    logging.info("El fichero json ha sido almacenado")


def _create_qcows(num_serv):
    i = 1
    while i < num_serv:
        logging.info(f"Creando el fichero qcow2 de la máquina {i}")
        subprocess.call(["qemu-img", "create", "-f", "qcow2",
                        "-b", "cdps-vm-base-pc1.qcow2", f"s{i}.qcow2"])
        i += 1

    logging.info("Los ficheros qcow2 requeridos han sido creados")


def _create_templates(num_serv):
    i = 1
    while i < num_serv:
        logging.info(
            f"Creando la plantilla de configuración de la máquina {i}")
        subprocess.call(["cp", "plantilla-vm-pc1.xml", f"s{i}.xml"])

        with open(f"s{i}.xml", "r") as xml:
            xml_content = xml.read()

        xml_content = xml_content.replace(
            '<name>XXX</name>', f'<name>s{i}</name>')
        xml_content = xml_content.replace('<source file="/mnt/tmp/XXX/XXX.qcow2"/>',
                                          f'<source file="/mnt/tmp/marta.rodrigueza/s{i}.qcow2"/>')  # TODO check which paths are
        xml_content = xml_content.replace(
            '<source bridge="XXX"/>', f'<source bridge="LAN2"/>')
        
        with open(f"s{i}.xml", 'w') as xml:
            xml.write(xml_content)

        i += 1

    logging.info("Las plantillas de configuración requeridas han sido creados")
