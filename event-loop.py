import time
import requests
from api import getAllInfo

while True:
    # TODO: call Eric's stuff and send to John's stuff
    url = "http://httpbin.org/post"
    data = getAllInfo()
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, json=data, headers=headers)
    # print r.status_code
    # print r.json()
    time.sleep(5)
