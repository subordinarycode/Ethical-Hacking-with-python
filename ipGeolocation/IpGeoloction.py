#! /bin/env python3
import ipinfo
import sys
from colorama import Fore
from multiprocessing import Process
from random import choice
import time

# access token for ipinfo.io
access_token = '<access token>'

black = Fore.BLACK
green = Fore.GREEN
cyan = Fore.CYAN
purple = Fore.MAGENTA
blue = Fore.BLUE
white = Fore.RESET
red = Fore.RED
yellow = Fore.YELLOW
box = f"{red}[{yellow}+{red}]{white}"
error = f"{red}[ERROR]{white}"

def curser():  
    colors = [blue, white, red, yellow, black, green, cyan, purple]
    while True:
        try: 
            for i in "/|-\\":
                color = choice(colors)
                sys.stdout.write(f'\r{color}{i}{white}')
                sys.stdout.flush()
                time.sleep(0.1)
        except KeyboardInterrupt:
            break

try:
    ip_address = sys.argv[1]
except IndexError:
    ip_address = None

try:
    print(f"{box} Running IP Geoloction luckup")
    p1 = Process(target=curser)
    p1.start()

    # create a client object with the access token
    handler = ipinfo.getHandler(access_token)
    # get the ip info
    try:
        details = handler.getDetails(ip_address, None)
    except Exception as e:
        print(f"{error} {e}")
        p1.kill()
        exit()
        
    # print the ip info
    for key, value in details.all.items():
        print(f"{cyan}{key}{white}: {value}")

    p1.kill()
except KeyboardInterrupt:
    p1.kill()
    exit()
