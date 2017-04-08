import os
import sys
import time
import requests

import subprocess

import pprint

from api import getAllInfo
from sar import parser


def get_data():
    p = subprocess.Popen('sar -f /var/log/sa/sar08'.split(' '), shell=True, stdout=subprocess.PIPE)
    outs, errs = p.communicate()
    
    
    sfile = ('%s/%s' % ('/var/log/sa', 'sar08'))
    insar = parser.Parser(sfile)
    #pprint.pprint(insar.get_sar_info())



    allinfo = getAllInfo()
    #pprint.pprint(allinfo['get_mem_info'])

    meta = allinfo['metadata']
    meta['num_cpu'] = allinfo['get_cpu_count']

    cpu = {}
    cpu['load_avg'] = allinfo['load_avg']

    mem = allinfo['get_mem_info']
    
    storage = allinfo['disk_usage']

    network = allinfo['get_net_io_counters']

    processes = allinfo['special_processes']

    data = {"id": meta['instance-id'], "meta": meta, "cpu": cpu, "mem": mem, "storage": storage, "network": network, "processes": processes}
    return data


while True:
    url = "https://stackcents.herokuapp.com/echo/"
    data = get_data()
    #pprint.pprint(data)
    r = requests.post(url, data=data)
    print(r.status_code)
    #print(r.json())
    time.sleep(10)
    
