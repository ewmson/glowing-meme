import os
import sys
import time
import datetime
import requests
import subprocess

import pprint

from api import getAllInfo
from sar import parser


def get_data():
    p = subprocess.Popen(["sar -q"], shell=True, stdout=subprocess.PIPE)
    outs, errs = p.communicate()

    cpu = []
    index = 0
    ignore = 3
    for line in outs.split('\n'):
        if ignore > 0:
            ignore -= 1
        else:
            parse = line.split()
            if len(parse) == 7:
                cpu.append({"index": index, "timestamp": "%s %s"%(parse[0],parse[1]), "load_avg_1": parse[4], "load_avg_5": parse[5], "load_avg_15": parse[6]})
                index += 1


    allinfo = getAllInfo()
    #pprint.pprint(allinfo['get_mem_info'])

    meta = allinfo['metadata']
    meta['num_cpu'] = allinfo['get_cpu_count']

    #cpu = {}
    #cpu['load_avg'] = allinfo['load_avg']

    mem = allinfo['get_mem_info']
    
    storage = allinfo['disk_usage']

    network = allinfo['get_net_io_counters']

    processes = allinfo['special_processes']

    data = {"id": meta['instance-id'], "timestamp": time.time(), "meta": meta, "cpu": cpu, "mem": mem, "storage": storage, "network": network, "processes": processes}
    return data


while True:
    url = "https://stackcents.herokuapp.com/echo/"
    data = get_data()
    pprint.pprint(data)
    r = requests.post(url, data=data)
    print(r.status_code)
    #print(r.json())
    time.sleep(10)
    
