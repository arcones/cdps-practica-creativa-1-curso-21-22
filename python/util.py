# -*- coding: utf-8 -*-

import json

def get_scenario_machines_list(num_serv):
    servers_and_lb = unfurl(num_serv)
    servers_and_lb.append("lb")
    return servers_and_lb


def unfurl(num_serv):
    servers = []
    i = 1
    while i <= num_serv:
        servers.append(f"s{i}")
        i += 1
    return servers

def read_num_serv(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as config_file_contents:
        num_serv = json.load(config_file_contents)['num_serv']
    return num_serv
