#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import sys

from python.args_parser import parse
from python.args_validator import validate, args_warnings
# Importo el resto de ficheros del programa
from python.download import download
from python.launch import launch
from python.logs import init_logs
from python.prepare import prepare
from python.release import release
from python.stop import stop

CONFIG_FILE = "auto-p2.json"

LOGGER = init_logs()

# Captura de argumentos de entrada al programa
args = parse(argparse.ArgumentParser())

# Validaciones de los argumentos de entrada al programa
validate(sys.argv, args, CONFIG_FILE)
# Mensajes informativos
args_warnings(sys.argv, args)

# Ejecucción del script con los argumentos proporcionados
if (args.orden == 'download'):
    download()
elif (args.orden == 'prepare'):
    prepare(CONFIG_FILE, args.num_serv)
elif (args.orden == 'release'):
    release(CONFIG_FILE, args.num_serv)
elif (args.orden == 'launch' or args.orden == 'stop' or args.orden == 'release'):
    with open('auto-p2.json', 'r') as config_file_contents:
        num_serv = json.load(config_file_contents)['num_serv']
    LOGGER.info(f"Corriendo la orden {args.orden} con num_serv={args.num_serv}")
    if (args.orden == 'launch'):
        launch(num_serv)
    elif (args.orden == 'stop'):
        stop(num_serv)
else:
    LOGGER.error("Hay un problema con el código del programa. Contacte con el equipo de desarrollo")
