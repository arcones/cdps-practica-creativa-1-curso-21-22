#! /bin/bash

echo "Descargando los ficheros necesarios..."

wget https://idefix.dit.upm.es/download/cdps/pc1/cdps-vm-base-pc1.qcow2 --no-check-certificate
wget https://idefix.dit.upm.es/download/cdps/pc1/plantilla-vm-pc1.xml --no-check-certificate

echo "Se han descargado los ficheros necesarios, ahora puede correr el script auto-p2"
