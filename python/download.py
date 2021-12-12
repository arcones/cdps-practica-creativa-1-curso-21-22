# -*- coding: utf-8 -*-

import subprocess

REPO_URL = "https://idefix.dit.upm.es/download/cdps/pc1"



def download():
    print('\033[92m' + "Procediendo con la descarga de los ficheros..." + '\033[0m')
    _download_xml()
    _download_qcow()
    print('\033[92m' + "Los ficheros han sido descargados exitosamente" + '\033[0m')


def _download_xml():
    print('\033[92m' + "Descargando fichero plantilla xml..." + '\033[0m')
    subprocess.call(["wget", "-nc", f"{REPO_URL}/plantilla-vm-pc1.xml", "--no-check-certificate"])
    print('\033[92m' + "Descargado fichero plantilla xml" + '\033[0m')


def _download_qcow():
    print('\033[92m' + "Descargando fichero base qcow..." + '\033[0m')
    subprocess.call(["wget", "-nc", f"{REPO_URL}/cdps-vm-base-pc1.qcow2", "--no-check-certificate"])
    print('\033[92m' + "Descargado fichero base qcow" + '\033[0m')
