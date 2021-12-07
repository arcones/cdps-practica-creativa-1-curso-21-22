#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import json
import os

# Importo el resto de ficheros del programa
from prepare import prepare
from cleanup import cleanup
from launch import launch 
from logs import init_logs, log_info, log_error, log_warn 

CONFIG_FILE = "auto-p2.json"

# Configuración de los logs
init_logs()

# Captura de argumentos de entrada al programa
parser = argparse.ArgumentParser()


help_orden = """
La orden a ejecutar.
"prepare": Para crear los ficheros .qcow2 de diferencias y los de especificación en XML de cada MV, así como los bridges virtuales que soportan las LAN del escenario.
"launch": Para arrancar las máquinas virtuales y mostrar su consola.
"stop": Para parar las máquinas virtuales (sin liberarlas).
"release": Para liberar el escenario, borrando todos los ficheros creados.
"cleanup": Para borrar ficheros de configuración de ejecuciones anteriores 
"""

parser.add_argument('orden', help=help_orden, nargs='?',
                    choices=('prepare', 'launch', 'stop', 'release', 'cleanup'))

parser.add_argument("-n", "--num_serv", help="Con la orden prepare, el número de servidores web a arrancar (de 1 a 5), si este parámetro no se pasa, será 3. El número de servidores se guardará para las siguientes órdenes",
                    default=3, required=False, type=int)

args = parser.parse_args()

# Validaciones de los argumentos de entrada al programa
if len(sys.argv) < 2:
    log_error("Este script necesita algunos argumentos para ejecutarse. Si necesita ayuda, ejecute el programa con --help")
    raise ValueError()

if not args.orden:
    log_error("Se debe especificar la orden a realizar. Vuelva a ejecutar el script con la orden (prepare, launch, stop, release) correcta")
    raise ValueError()

if args.orden != 'prepare' and len(sys.argv) > 2:
    log_error("El número de servidores sólo se debe especificar con la orden prepare")
    raise ValueError()


if args.orden == 'prepare' and (args.num_serv < 1 or args.num_serv > 5):
    log_error("El número de servidores para la orden prepare ha de estar entre 1 y 5. Vuelva a ejecutar el script con un número de servidores correcto")
    raise ValueError()

# Mensajes informativos
if args.orden == 'prepare' and len(sys.argv) == 2:
    log_warn("Como no se ha especificado el número de servidores para la orden prepare, se usarán 3 servidores que es el valor predeterminado")

# Ejecucción del script con los argumentos proporcionados
if(args.orden == 'prepare'):
    prepare(CONFIG_FILE, args.num_serv)
elif(args.orden == 'cleanup'):
    cleanup(CONFIG_FILE)
elif(args.orden == 'launch' or args.orden == 'stop' or args.orden == 'release'):
    if not os.path.exists(f'./{CONFIG_FILE}'):
        log_error("Las órdenes launch, stop y release necesitan el fichero de configuración generado con la orden prepare. Ejecute primeramente el script con la orden prepare para generarlo")
        raise ValueError()
    else:
        with open('auto-p2.json', 'r') as config_file_contents:
            num_serv = json.load(config_file_contents)['num_serv']
        log_info(f"Corriendo la orden {args.orden} con num_serv={args.num_serv}")
        if(args.orden == 'launch'):
            launch(num_serv)
else:
    log_error("Hay un problema con el código del programa. Contacte con el equipo de desarrollo")
