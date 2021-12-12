# -*- coding: utf-8 -*-

import os


def validate(argv, args, CONFIG_FILE):
    if (_args_count_wrong(argv) 
        or _order_not_present(args) 
        or _wrong_order_with_domain(args)
        or _wrong_num_servs(args)
        or _missing_required_config_file(args, CONFIG_FILE)):
        print('\033[91m' + "Los parámetros introducidos al script son incorrectos, ejecutelo con --help para encontrar más información" + '\033[0m')
        raise ValueError()


def args_warnings(argv, args):
    if args.orden == 'prepare' and len(argv) == 2:
        print('\033[93m'+ "Se usarán 3 servidores como valor predeterminado por la ausencia de este parámetro" + '\033[0m')


def _args_count_wrong(argv):
    if len(argv) < 2:
        print('\033[91m' + "Este script necesita algunos argumentos para ejecutarse. Si necesita ayuda, ejecute el programa con --help" + '\033[0m')
        return True


def _order_not_present(args):
    if not args.orden:
        print('\033[91m' + "Se debe especificar la orden a realizar. Vuelva a ejecutar el script con una de las órdenes proporcionadas" + '\033[0m')
        return True

def _wrong_order_with_domain(args):
    if args.orden != 'monitor' and args.domain:
        print('\033[91m' + "El domain sólo se debe especificar con la orden monitor" + '\033[0m')
        return True

def _wrong_num_servs(args):
    if args.orden == 'prepare' and (args.num_serv < 1 or args.num_serv > 5):
        print('\033[91m' + "El número de servidores para la orden prepare ha de estar entre 1 y 5. Vuelva a ejecutar el script con un número de servidores correcto" + '\033[0m')
        return True


def _missing_required_config_file(args, CONFIG_FILE):
    if (args.orden == 'launch' or args.orden == 'stop' or args.orden == 'release') and (not os.path.exists(CONFIG_FILE)):
        print('\033[91m' + "Las órdenes launch, stop y release necesitan el fichero de configuración generado con la orden prepare. Ejecute primeramente el script con la orden prepare para generarlo" + '\033[0m')
        return True
