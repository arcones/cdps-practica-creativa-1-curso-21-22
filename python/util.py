# -*- coding: utf-8 -*-

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
