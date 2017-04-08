import os
import psutil
from boto.utils import get_instance_metadata

metadata = get_instance_metadata()

proc = {"mongod", "a.out", "python"}

def __get_meta_data():
    return metadata

def __get_info_about_named_processes():
    processes = {}
    for p in psutil.process_iter():
        if p.name() in proc:
            processes[p.name()] = p.as_dict()
    return processes

def __get_disk_usage():
    total, used, free, percent = psutil.disk_usage('/')
    return {"total": total, "free": free, "used": used, "percent": percent}


def __getloadavg():
    (min1,min5,min10) = os.getloadavg()
    return {"1_min": min1, "5_min": min5, "10_min": min10}


def __get_cpu_count():
    return {"num_cpu": psutil.cpu_count()}


def getAllInfo():
    return {
        "load_avg": __getloadavg(),
        "get_cpu_count": __get_cpu_count(),
        "disk_usage": __get_disk_usage(),
        "special_processes": __get_info_about_named_processes(),
        "metadata": __get_meta_data()
    }
if __name__ == "__main__":
    print(getAllInfo())
