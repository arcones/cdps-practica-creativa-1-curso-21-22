#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import json

# Importo el resto de ficheros del programa
from download import download
from prepare import prepare
from cleanup import cleanup
from launch import launch 
from stop import stop
from args_parser import parse
from args_validator import validate, args_warnings
from logs import init_logs, log_info, log_error, log_warn 

CONFIG_FILE = "auto-p2.json"

# Configuración de los logs
init_logs()

# Captura de argumentos de entrada al programa
args = parse(argparse.ArgumentParser())

# Validaciones de los argumentos de entrada al programa
validate(sys.argv, args, CONFIG_FILE)
# Mensajes informativos
args_warnings(sys.argv, args)

# Ejecucción del script con los argumentos proporcionados
if(args.orden == 'download'):
    download()
elif(args.orden == 'prepare'):
    prepare(CONFIG_FILE, args.num_serv)
elif(args.orden == 'cleanup'):
    cleanup(CONFIG_FILE)
elif(args.orden == 'launch' or args.orden == 'stop' or args.orden == 'release'):
    with open('auto-p2.json', 'r') as config_file_contents:
        num_serv = json.load(config_file_contents)['num_serv']
    log_info(f"Corriendo la orden {args.orden} con num_serv={args.num_serv}")
    if(args.orden == 'launch'):
        launch(num_serv)
    elif(args.orden == 'stop'):
        stop(num_serv)
else:
    log_error("Hay un problema con el código del programa. Contacte con el equipo de desarrollo")
