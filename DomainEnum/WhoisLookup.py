#! /bin/env python3
import whois
from colorama import Fore
import time 
import multiprocessing
from random import choice
import os
from threading import Lock


blue = Fore.BLUE
white = Fore.RESET
red = Fore.RED
yellow = Fore.YELLOW
cyan = Fore.CYAN

printLock = Lock()

box = f"{red}[{yellow}+{red}]{white}"
error = f"{red}[ERROR]{white}"

 

def is_registered(domain_name):

    try:
        w = whois.whois(domain_name)
    except Exception as e:
        print(f"{error} {e}")
        return False
    else:
        return bool(w.domain_name)


def domain_infomation(domain_name, outFile=None):
    if is_registered(domain_name):
        whois_info = whois.whois(domain_name)
        print(blue + "="*30 + white + f" {domain_name} " + blue + "="*30)
        # print the registrar
        print(f"{box} {cyan}Registrar:{white}", whois_info.registrar)
        # print the WHOIS server
        print(f"{box} {cyan}WHOIS server:{white}", whois_info.whois_server)
        # dnssec
        print(f"{box} {cyan}Dns security: {white}{whois_info.dnssec}")
        # organization
        print(f"{box} {cyan}Organization: {white}{whois_info.org}")
        # emails
        print(f"{box} {cyan}Emails:{white}", whois_info.emails)
        
        # print updated date
        update_date =  str(whois_info.updated_date)
        with printLock:
            update_date = update_date.split("-")
            if len(update_date) >= 3:
                UpdateDate = f"{update_date[1]}-{update_date[2]}-{update_date[0]}"
            else:
                UpdateDate = ""

            
        print(f"{box} {cyan}Updated date: {white}{UpdateDate}")


        # get the creation time
        Creation_Date = str(whois_info.creation_date)
        with printLock:
            Creation_Date = Creation_Date.replace("[datetime.datetime(", "")
            Creation_Date = Creation_Date.split(",")
            if len(Creation_Date) >= 3:
                CreationDate = f"{Creation_Date[1].strip()}-{Creation_Date[2].strip()}-{Creation_Date[0].strip()}"
            else:
                CreationDate = ""
            
        print(f"{box} {cyan}Creation date: {white}{CreationDate}")


        # get expiration date
        Experation_Date = str(whois_info.expiration_date)
        with printLock:
            Experation_Date = Experation_Date.replace("[datetime.datetime(", "")
            Experation_Date = Experation_Date.replace("[datetime.datetime(", "")
            Experation_Date = Experation_Date.replace(")]", "")
            Experation_Date = Experation_Date.split(",")
            if len(Experation_Date) >= 3:
                ExperationDate = f"{Experation_Date[1].strip()}-{Experation_Date[2].strip()}-{Experation_Date[0].strip()}"
            else:
                ExperationDate = ""
            print(f"{box} {cyan}Expiration date: {white}{ExperationDate}")


        # country 
        print(f"{box} {cyan}Country: {white}{whois_info.country}")
        # state
        print(f"{box} {cyan}State: {white}{whois_info.state}")
        # address 
        print(f"{box} {cyan}Address:{white}", whois_info.address)
        # postal code
        print(f"{box} {cyan}Postal code: {white}{whois_info.registrant_postal_code}")
        
 
        if outFile != None:
            if  os.path.exists(outFile): 
                with printLock:
                    with open(outFile, "a") as f:
                        f.write(blue + "="*30 + white + f" {domain_name} " + blue + "="*30 + "\n")
                        f.write(f"{box} {cyan}Registrar:{white}{whois_info.registrar}\n")
                        f.write(f"{box} {cyan}WHOIS server:{white}{whois_info.whois_server}\n")
                        f.write(f"{box} {cyan}Dns security: {white}{whois_info.dnssec}\n")
                        f.write(f"{box} {cyan}Organization: {white}{whois_info.org}\n")
                        f.write(f"{box} {cyan}Emails:{white}{whois_info.emails}\n") 
                        f.write(f"{box} {cyan}Updated date:{white} {UpdateDate}\n")
                        f.write(f"{box} {cyan}Creation date: {white}{CreationDate}\n")
                        f.write(f"{box} {cyan}Expiration date: {white}{ExperationDate}\n")
                        f.write(f"{box} {cyan}Country: {white}{whois_info.country}\n")
                        f.write(f"{box} {cyan}State: {white}{whois_info.state}\n")
                        f.write(f"{box} {cyan}Address:{white} {whois_info.address}\n")
                        f.write(f"{box} {cyan}Postal code: {white}{whois_info.registrant_postal_code}\n")
            else:
                with printLock:
                    with open(outFIle, "w") as f:
                        f.write(blue + "="*30 + white + f" {domain_name} " + blue + "="*30 + "\n")
                        f.write(f"{box} {cyan}Registrar:{white}{whois_info.registrar}\n")
                        f.write(f"{box} {cyan}WHOIS server:{white}{whois_info.whois_server}\n")
                        f.write(f"{box} {cyan}Dns security: {white}{whois_info.dnssec}\n")
                        f.write(f"{box} {cyan}Organization: {white}{whois_info.org}\n")
                        f.write(f"{box} {cyan}Emails:{white}{whois_info.emails}\n") 
                        f.write(f"{box} {cyan}Updated date:{white} {UpdateDate}\n")
                        f.write(f"{box} {cyan}Creation date: {white}{CreationDate}\n")
                        f.write(f"{box} {cyan}Expiration date: {white}{ExperationDate}\n")
                        f.write(f"{box} {cyan}Country: {white}{whois_info.country}\n")
                        f.write(f"{box} {cyan}State: {white}{whois_info.state}\n")
                        f.write(f"{box} {cyan}Address:{white} {whois_info.address}\n")
                        f.write(f"{box} {cyan}Postal code: {white}{whois_info.registrant_postal_code}\n")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Proforms a whois lookup on a domain")
    parser.add_argument("domain", help="The domain name")
    parser.add_argument("-o", "--output", help="The output file path")
    
    
    args = parser.parse_args()
    
    domain_infomation(domain=args.domain, outFIle=args.output)

