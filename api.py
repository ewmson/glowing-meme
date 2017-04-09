import os
import time
import psutil
from boto.utils import get_instance_metadata

metadata = get_instance_metadata()
metadata['uptime'] = time.time() - psutil.boot_time()

proc = {"mongod", "a.out", "python", "postmaster"}

def __get_meta_data():
    return metadata

def __get_info_about_named_processes():
    processes = {}
    for p in psutil.process_iter():
        if p.name() in proc:
            processes[str(p.pid)] = p.as_dict()
    return processes

def __get_disk_usage():
    total, used, free, percent = psutil.disk_usage('/')
    return {"total": total, "free": free, "used": used, "percent": percent}

def __get_mem_info():
    total, available, percent, used, free, active, inactive, buffers, cached, shared = psutil.virtual_memory()
    return {"total": total, "available": available, "percent": percent, "used": used, "free": free, "active": active, "inactive": inactive, "buffers": buffers, "cached": cached, "shared": shared}

def __getloadavg():
    (min1,min5,min10) = os.getloadavg()
    return {"1_min": min1, "5_min": min5, "10_min": min10}


def __get_cpu_count():
    return {"num_cpu": psutil.cpu_count()}

def __get_net_io_counters():
    bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout = psutil.net_io_counters()
    return {"bytes_sent": bytes_sent, "bytes_recv": bytes_recv, "packets_sent": packets_sent, "packets_recv": packets_recv, "errin": errin, "errout": errout, "dropin": dropin, "dropout": dropout}


def __get_intance_id():
    return metadata["instance-id"]

def getAllInfo():
    return {
        "load_avg": __getloadavg(),
        "get_cpu_count": __get_cpu_count(),
        "get_mem_info": __get_mem_info(),
        "disk_usage": __get_disk_usage(),
        "get_net_io_counters": __get_net_io_counters(),
        "special_processes": __get_info_about_named_processes(),
        "metadata": __get_meta_data(),
        "instance_id": __get_intance_id()
    }

    

if __name__ == "__main__":
    print(getAllInfo())
