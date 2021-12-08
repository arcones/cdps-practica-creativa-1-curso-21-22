# -*- coding: utf-8 -*-

import subprocess

# Importo el resto de ficheros del programa
from logs import init_logs, log_error, log_warn, log_info

# Configuración de los logs
init_logs()

REPO_URL = "https://idefix.dit.upm.es/download/cdps/pc1"

# Punto de entrada
def download():
    _download_xml()
    _download_qcow()

def _download_xml():
    log_info("Descargando fichero plantilla xml...")
    subprocess.call(["wget", "-nc", f"{REPO_URL}/plantilla-vm-pc1.xml", "--no-check-certificate"])
    log_info("Descargado fichero plantilla xml")

def _download_qcow():
    log_info("Descargando fichero base qcow...")
    subprocess.call(["wget", "-nc", f"{REPO_URL}/cdps-vm-base-pc1.qcow2", "--no-check-certificate"])
    log_info("Descargado fichero base qcow")
