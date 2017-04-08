import os
import sys
import time
import json
import datetime
import requests
import subprocess

import pprint

from api import getAllInfo
from sar import parser


def get_data():
    # loadavg
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

    # mem usage
    p = subprocess.Popen(["sar -r"], shell=True, stdout=subprocess.PIPE)
    outs, errs = p.communicate()

    mem = []
    index = 0
    ignore = 3
    for line in outs.split('\n'):
        if ignore > 0:
            ignore -= 1
        else:
            parse = line.split()
            if len(parse) == 9:
                mem.append({"index": index, "timestamp": "%s %s"%(parse[0],parse[1]), "kbmemfree": parse[2], "kbmemused": parse[3], "%memused": parse[4], "kbbuffers": parse[5], "kbcached": parse[6], "kbcommit": parse[7], "%commit": parse[8]})
                index += 1

    # swap space
    p = subprocess.Popen(["sar -S"], shell=True, stdout=subprocess.PIPE)
    outs, errs = p.communicate()

    swap = []
    index = 0
    ignore = 3
    for line in outs.split('\n'):
        if ignore > 0:
            ignore -= 1
        else:
            parse = line.split()
            if len(parse) == 7:
                swap.append({"index": index, "timestamp": "%s %s"%(parse[0],parse[1]), "kbswpfree": parse[2], "kbswpused": parse[3], "%swpused": parse[4], "kbswpcad": parse[5], "%swpcad": parse[6]})
                index += 1




    allinfo = getAllInfo()
    #pprint.pprint(allinfo['get_mem_info'])

    meta = allinfo['metadata']
    meta['num_cpu'] = allinfo['get_cpu_count']

    #cpu = {}
    #cpu['load_avg'] = allinfo['load_avg']

    #mem = allinfo['get_mem_info']
    
    storage = allinfo['disk_usage']

    network = allinfo['get_net_io_counters']

    processes = allinfo['special_processes']

    data = {"id": meta['instance-id'], "timestamp": time.time(), "meta": meta, "cpu": cpu, "mem": mem, "swap": swap, "storage": storage, "network": network, "processes": processes}
    return data


while True:
    subprocess.Popen(["/usr/lib64/sa/sa1", "1", "1"], shell=True, stdout=subprocess.PIPE)
    url = "https://stackcents.herokuapp.com/save_data/"
    data = get_data()
    pprint.pprint(data['swap'])
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    #print(r.status_code)
    #print(r.json())
    time.sleep(10)
    
