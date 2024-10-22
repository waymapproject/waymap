# Copyright (c) 2024 waymap developers
# See the file 'LICENSE' for copying permission.
# jm.py profile critical

from colorama import Fore, Style, init
from sqlinjection.CVE_2018_6396 import scan_cve_2018_6396
from sqlinjection.CVE_2012_17254 import scan_cve_2018_17254
from auth.CVE_2017_18345 import scan_cve_2017_18345
from sqlinjection.CVE_2017_8917 import scan_cve_2017_8917
init(autoreset=True)

def handle_cve_2018_6396(target):

    print(f"{Fore.CYAN}[+] Starting scan for {Fore.YELLOW}CVE-2018_6396 {Fore.CYAN}on {Fore.GREEN}{target}{Style.RESET_ALL}...")

    scan_cve_2018_6396(target)

    print(f"{Fore.CYAN}[-] Completed scan for {Fore.YELLOW}CVE-2018_6396 {Fore.CYAN}on {Fore.GREEN}{target}{Style.RESET_ALL}.")

def handle_cve_2018_17254(target):

    print(f"{Fore.CYAN}[+] Starting scan for {Fore.YELLOW}CVE-2018_17254 {Fore.CYAN}on {Fore.GREEN}{target}{Style.RESET_ALL}...")

    scan_cve_2018_17254(target)

    print(f"{Fore.CYAN}[-] Completed scan for {Fore.YELLOW}CVE-2018_17254 {Fore.CYAN}on {Fore.GREEN}{target}{Style.RESET_ALL}.")

def handle_cve_2017_18345(target):

    print(f"{Fore.CYAN}[+] Starting scan for {Fore.YELLOW}CVE-2017_18345 {Fore.CYAN}on {Fore.GREEN}{target}{Style.RESET_ALL}...")

    scan_cve_2017_18345(target)

    print(f"{Fore.CYAN}[-] Completed scan for {Fore.YELLOW}CVE-2017_18345 {Fore.CYAN}on {Fore.GREEN}{target}{Style.RESET_ALL}.")

def handle_cve_2017_8917(target):

    print(f"{Fore.CYAN}[+] Starting scan for {Fore.YELLOW}CVE-2017_8917 {Fore.CYAN}on {Fore.GREEN}{target}{Style.RESET_ALL}...")

    scan_cve_2017_8917(target)

    print(f"{Fore.CYAN}[-] Completed scan for {Fore.YELLOW}CVE-2017_8917 {Fore.CYAN}on {Fore.GREEN}{target}{Style.RESET_ALL}.")
