# -*- coding: utf-8 -*-

import os

# Importo el resto de ficheros del programa
from logs import init_logs

LOGGER = init_logs()


# Punto de entrada
def validate(argv, args, CONFIG_FILE):
    if _args_count_wrong(argv) or _order_not_present(args) or _wrong_order_with_num_servs(argv,
                                                                                          args) or _wrong_num_servs(
            args) or _missing_required_config_file(args, CONFIG_FILE):
        LOGGER.error(
            "Los parámetros introducidos al script son incorrectos, ejecutelo con --help para encontrar más información")
        raise ValueError()


def args_warnings(argv, args):
    if args.orden == 'prepare' and len(argv) == 2:
        LOGGER.warn("Se usarán 3 servidores como valor predeterminado por la ausencia de este parámetro")


def _args_count_wrong(argv):
    if len(argv) < 2:
        LOGGER.error(
            "Este script necesita algunos argumentos para ejecutarse. Si necesita ayuda, ejecute el programa con --help")
        return True


def _order_not_present(args):
    if not args.orden:
        LOGGER.error(
            "Se debe especificar la orden a realizar. Vuelva a ejecutar el script con una de las órdenes proporcionadas")
        return True


def _wrong_order_with_num_servs(argv, args):
    if args.orden != 'prepare' and len(argv) > 2:
        LOGGER.error("El número de servidores sólo se debe especificar con la orden prepare")
        return True


def _wrong_num_servs(args):
    if args.orden == 'prepare' and (args.num_serv < 1 or args.num_serv > 5):
        LOGGER.error(
            "El número de servidores para la orden prepare ha de estar entre 1 y 5. Vuelva a ejecutar el script con un número de servidores correcto")
        return True


def _missing_required_config_file(args, CONFIG_FILE):
    if (args.orden == 'launch' or args.orden == 'stop' or args.orden == 'release') and (
    not os.path.exists(f'./{CONFIG_FILE}')):
        LOGGER.error(
            "Las órdenes launch, stop y release necesitan el fichero de configuración generado con la orden prepare. Ejecute primeramente el script con la orden prepare para generarlo")
        return True
