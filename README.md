# Automatización de escenario virtual de balanceo de carga

Este script provee de ciertas opciones que permitiran al usuario crear el escenario siguiente:

![escenario con n servidores, un balanceador de carga y un cliente](img/Escenario.png)

Así como controlar su ejecución, monitorizarlo o destruirlo.

## Ayuda con el script
Simplemente ejecutelo de la siguiente manera `./auto-p2.py --help` para encontrar indicaciones acerca de su uso.

# Requisitos

Primeramente habrá que descargar los ficheros base sobre los que se crean la máquinas virtuales que componen el escenario.
Se ha preparado una orden adicional en el script para realizar esta tarea `./auto-p2.py download´


añadir permisos de ejecucción al script
pip3 install -r requirements.txt
./download-requirements.sh


acerca de la nueva orden cleanup
