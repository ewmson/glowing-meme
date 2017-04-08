import time
import requests
from api import getAllInfo

while True:
    # TODO: call Eric's stuff and send to John's stuff
    url = "https://stackcents.herokuapp.com/echo/"
    data = getAllInfo()
    #data = {"hello":"world"}
    #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=data)
    #print(r.status_code)
    #print(r.json())
    time.sleep(10)
