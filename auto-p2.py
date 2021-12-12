#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys

sys.path.insert(0, 'python')

from python.args_parser import parse
from python.args_validator import validate, args_warnings
from python.download import download
from python.monitor import monitor
from python.launch import launch
from python.prepare import prepare
from python.release import release
from python.stop import stop
from python.util import read_num_serv

CONFIG_FILE = "auto-p2.json"


# Captura de argumentos de entrada al programa
args = parse(argparse.ArgumentParser())

# Validaciones de los argumentos de entrada al programa
validate(sys.argv, args, CONFIG_FILE)

# Mensajes informativos
args_warnings(sys.argv, args)

print("\033[92m" + f"Corriendo la orden {args.orden}" + "\033[0m")

# Ejecucción del script con los argumentos proporcionados
if (args.orden == 'download'):
    download()
elif (args.orden == 'prepare'):
    prepare(CONFIG_FILE, args.num_serv)
elif (args.orden == 'release'):
    release(CONFIG_FILE)
elif (args.orden == 'launch' or args.orden == 'stop' or args.orden == 'monitor'):
    num_serv = read_num_serv(CONFIG_FILE)
    if (args.orden == 'launch'):
        launch(num_serv)
    elif (args.orden == 'stop'):
        stop(num_serv)
    elif (args.orden == 'monitor'):
        monitor(CONFIG_FILE, args.domain)
else:
    print("\033[91m Hay un problema con el código del programa. Contacte con el equipo de desarrollo" + "\033[0m")

