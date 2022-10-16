#! /bin/env python3

import os
import sys
import time
import multiprocessing
import requests
import threading
from queue import Queue
from WhoisLookup import *
from colorama import Fore
import argparse
from random import choice 
from threading import Thread, Lock
from queue import Queue

q = Queue()
q2 = Queue()
printLock = Lock()

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

discovered_domains = []



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


def scanner(domain_name, Timeout=4): 
    global q
    while True:
        outFile = output
        if q.empty():
            break
        subdomain = q.get()
        url = f"http://{subdomain}.{domain_name}"
        try:
            requests.get(url, timeout=Timeout)
        except KeyboardInterrupt:
            p1.kill()
            print("\n")
            exit()
        except:
            pass
        else:
            print(f"{box} {cyan}Found subdomain: {white}{url}")
        
            with printLock:
                discovered_domains.append(url)
                if outFile != None:
                    if os.path.exists(outFile):
                        with open (outFile, "a") as f:
                            f.write(f"{box} {cyan}Found subdomain: {white}{url}\n")
                    else:
                        with open(outFile, "w") as f:
                            f.write(f"{box} {cyan}Found subdomain: {white}{url}\n")
            
            q.task_done()

def whoisINFO():    
    global q2
    while True:
        try:
            if q2.empty():
                break
            subdomain = q2.get()
            domain_infomation(subdomain, output)
            q2.task_done()
        except KeyboardInterrupt:
            break




def main(args):
    global p1, q, discovered_domains, output
    single_scan = True
    worker_threads = []
    if args.domains != None:
        if os.path.exists(args.domains) and os.path.isfile(args.domains):
            with open(args.domains) as f:
                d = f.read()
                domains = d.splitlines()
            single_scan = False

        else:
            print(f"{error} Could not find domain file")
            parser.print_help()
            exit()

    timeout = args.timeout
    output = args.output
    numOfThreads = args.threads
    try:
        p1 = multiprocessing.Process(target=curser)
        p1.start()

        if single_scan:
            print(f"{box} Scanning for subdomains")
            domain = args.domain

            with open(args.wordlist) as f:
                content = f.read()
                subdomains = content.splitlines()
            
            for i in subdomains:
                q.put(i)
            
            for _ in range(numOfThreads):
                t = threading.Thread(target=scanner, args=(domain, timeout))
                t.daemon = True
                t.start()
                worker_threads.append(t)
                
            for i in worker_threads:
                i.join()

            worker_threads = []
            print(f"{box} Starting whois on found domains")
            
            
            for i in discovered_domains:
                q2.put(i)

   
            for _ in range(numOfThreads):
                t = threading.Thread(target=whoisINFO)
                t.daemon = True
                t.start()
                worker_threads.append(t)
             
            

            for i in worker_threads:
                i.join()


        else:

            with open(args.wordlist) as f:
                content = f.read()
                subdomains = content.splitlines()
            

            for subdomain in subdomains:
                q.put(subdomain)
            
            for domain in domains:
                discovered_domains = []

                for _ in range(numOfThreads):
                    t = Thread(target=scanner, args=(domain, timeout, outfile))
                    t.daemon = True
                    t.start()
                    worker_threads.append(t)

                for i in worker_threads:
                    i.join()

                worker_threads = []
                for i in discovered_domains:
                    q2.put(i)
                
                for _ in range(numOfThreads):
                    for i in discovered_domains:
                        t = Thread(target=whoisINFO, args=(output))
                        t.daemon = True
                        t.start()
                        worker_threads.append(t)
                    

                for i in worker_threads:
                    i.join()

    
    except KeyboardInterrupt:
        p1.kill()
        print("\n")
        exit()
    else:
        p1.kill()
        exit()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Domain name information extractor, uses WHOIS db and scans for subdomains")
    parser.add_argument("-d", "--domain", help="The domain name")
    parser.add_argument("-D", "--domains", help="The file path that contains the list of domains to scan")
    parser.add_argument("-t", "--timeout", type=int, default=4, help="The timeout in seconds for prompting the connection, default is 4")
    parser.add_argument("-T", "--threads", type=int, default=200, help="Number of threads to use, default is 200")
    parser.add_argument("-w", "--wordlist", default="wordlist.txt", help="The file path to wordlist")
    parser.add_argument("-o", "--output", help="The output file path resulting the discovered subdomains")
    

    # parse the command-line arguments
    args = parser.parse_args()
    if args.domain == None and args.domains == None:
        parser.print_help()
        exit()

    main(args)
