import os
import psutil
from boto.utils import get_instance_metadata

metadata = get_instance_metadata()

proc = {"mongod", "a.out", "python"}

def getMetaData():
    return metadata

def getInfoAboutNamedProcesses():
    processes = {}
    for p in psutil.process_iter():
        if p.name() in proc:
            processes[p.name()] = p.as_dict()
    return processes

def getDiskUsage():
    total, used, free, percent = psutil.disk_usage('/')
    return {"total": total, "free": free, "used": used, "percent": percent}


def getLoadAvg():
    (min1,min5,min10) = os.getloadavg()
    return {"1_min": min1, "5_min": min5, "10_min": min10}


def getCpuCount():
    return {"num_cpu": os.cpu_count()}


def getAllInfo():
    return {
        "load_avg": getLoadAvg(),
        "get_cpu_count": getCpuCount(),
        "disk_usage": getDiskUsage(),
        "special_processes": getInfoAboutNamedProcesses(),
        "metadata": getMetaData()
    }