import sys
import time

while True:
    if len(sys.argv) != 2:
        print "usage: fillmem <number-of-megabytes>"
        sys.exit()
    
    count = int(sys.argv[1])
    
    megabyte = (0,) * (1024 * 1024 / 8)
    
    data = megabyte * count
    
    time.sleep(15)
    
