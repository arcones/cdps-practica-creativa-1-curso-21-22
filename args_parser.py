# -*- coding: utf-8 -*-

HELP_ORDER = """
La orden a ejecutar.
"prepare": Para crear los ficheros .qcow2 de diferencias y los de especificación en XML de cada MV, así como los bridges virtuales que sopo
rtan las LAN del escenario.
"launch": Para arrancar las máquinas virtuales y mostrar su consola.
"stop": Para parar las máquinas virtuales (sin liberarlas).
"release": Para liberar el escenario, borrando todos los ficheros creados.
"cleanup": Para borrar ficheros de configuración de ejecuciones anteriores 
"""

HELP_NUM_SERV = "Con la orden prepare, el número de servidores web a arrancar (de 1 a 5), si este parámetro no se pasa, será 3. El número de servidores se guardará para las siguientes órdenes"

# Punto de entrada
def parse(parser):
    parser.add_argument('orden', help=HELP_ORDER, nargs='?', choices=('prepare', 'launch', 'stop', 'release', 'cleanup', 'download'))
    parser.add_argument("-n", "--num_serv", help=HELP_NUM_SERV, default=3, required=False, type=int)
    return parser.parse_args()

