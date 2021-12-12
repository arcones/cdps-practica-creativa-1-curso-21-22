# -*- coding: utf-8 -*-

HELP_ORDER = """
La orden a ejecutar.
"download": Para bajarse los ficheros base .qcow2 y .xml.
"prepare": Para crear los ficheros .qcow2 de diferencias y los de especificación en XML de cada MV, así como los bridges virtuales que soportan las LAN del escenario.
"launch": Para arrancar las máquinas virtuales y mostrar su consola.
"monitor": Sin argumento domain, arranca la monitorización de todas las máquinas. Con el argumento domain, arranca la monitorización de una máquina.
"stop": Para parar las máquinas virtuales (sin liberarlas).
"release": Para liberar el escenario, destruyendo las máquinas y borrando todos los ficheros creados.
"""

HELP_NUM_SERV = "Con la orden prepare, el número de servidores web a arrancar (de 1 a 5), si este parámetro no se pasa, será 3. El número de servidores se guardará para las siguientes órdenes"

HELP_DOMAIN = "Con la orden monitor, el nombre del servidor a monitorizar. Si este argumento no se proporciona, se arranca la montorización de todo el escenario"


def parse(parser):
    parser.add_argument('orden', help=HELP_ORDER, nargs='?', choices=('download', 'prepare', 'launch', 'monitor', 'stop', 'release'))
    parser.add_argument("-n", "--num_serv", help=HELP_NUM_SERV, default=3, required=False, type=int)
    parser.add_argument("-d", "--domain", help=HELP_DOMAIN, required=False, type=str)
    return parser.parse_args()
