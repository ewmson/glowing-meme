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


process_history = {}


def get_data():
    allinfo = getAllInfo()
    now = datetime.datetime.now()
    start = "%02d:%02d:%02d"%(now.hour-1,now.minute,now.second)

    # meta
    meta = allinfo['metadata']
    meta['num_cpu'] = allinfo['get_cpu_count']
    meta['os'] = sys.platform

    # loadavg
    p = subprocess.Popen(["sar -q -s %s"%start], shell=True, stdout=subprocess.PIPE)
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
    p = subprocess.Popen(["sar -r -s %s"%start], shell=True, stdout=subprocess.PIPE)
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
    p = subprocess.Popen(["sar -S -s %s"%start], shell=True, stdout=subprocess.PIPE)
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

    # disk usage
    p = subprocess.Popen(["sar -d -s %s"%start], shell=True, stdout=subprocess.PIPE)
    outs, errs = p.communicate()

    storage = []
    index = 0
    ignore = 3
    for line in outs.split('\n'):
        if ignore > 0:
            ignore -= 1
        else:
            parse = line.split()
            if len(parse) == 11:
                storage.append({"index": index, "timestamp": "%s %s"%(parse[0],parse[1]), "tps": parse[3], "rd_sec/s": parse[4], "wr_sec/s": parse[5], "avgrq-sz": parse[6], "avgqu-sz": parse[7], "await": parse[8], "svctm": parse[9], "%util": parse[10]})
                index += 1

    # network
    p = subprocess.Popen(["sar -n DEV -s %s"%start], shell=True, stdout=subprocess.PIPE)
    outs, errs = p.communicate()

    network = []
    index = 0
    ignore = 3
    for line in outs.split('\n'):
        if ignore > 0:
            ignore -= 1
        else:
            parse = line.split()
            if len(parse) == 10 and parse[2] == "eth0":
                network.append({"index": index, "timestamp": "%s %s"%(parse[0],parse[1]), "interface": parse[2], "rxpck/s": parse[3], "txpck/s": parse[4], "rxkB/s": parse[5], "txkB/s": parse[6], "rxcmp/s": parse[7], "txcmp/s": parse[8], "rxmcst/s": parse[9]})
                index += 1

    # processes
    #for p in allinfo['special_processes']:
    processes = []




    data = {"id": meta['instance-id'], "timestamp": time.time(), "meta": meta, "cpu": cpu, "mem": mem, "swap": swap, "storage": storage, "network": network, "processes": processes}
    return data


while True:
    subprocess.Popen(["/usr/lib64/sa/sa1", "1", "1"], shell=True, stdout=subprocess.PIPE)
    url = "https://stackcents.herokuapp.com/save_data/"
    data = get_data()
    #pprint.pprint(data['meta'])
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    #print(r.status_code)
    #print(r.json())
    time.sleep(10)
    
