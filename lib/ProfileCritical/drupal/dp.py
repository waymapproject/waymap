# Copyright (c) 2024 waymap developers
# See the file 'LICENSE' for copying permission.
# dp.py profile critical

from colorama import Fore, Style, init
from others.CVE_2019_6339 import scan_cve_2019_6339
from rce.CVE_2018_7602 import scan_cve_2018_7602
from others.CVE_2018_7600 import scan_cve_2018_7600
init(autoreset=True)

def handle_cve_2019_6339(target):

    print(f"{Fore.CYAN}[+] Starting scan for {Fore.YELLOW}CVE-2019_6339 {Fore.CYAN}on {Fore.GREEN}{target}{Style.RESET_ALL}...")

    scan_cve_2019_6339(target)

    print(f"{Fore.CYAN}[-] Completed scan for {Fore.YELLOW}CVE-2019_6339 {Fore.CYAN}on {Fore.GREEN}{target}{Style.RESET_ALL}.")

def handle_cve_2018_7602(target):

    print(f"{Fore.CYAN}[+] Starting scan for {Fore.YELLOW}CVE-2018_7602 {Fore.CYAN}on {Fore.GREEN}{target}{Style.RESET_ALL}...")

    scan_cve_2018_7602(target)

    print(f"{Fore.CYAN}[-] Completed scan for {Fore.YELLOW}CVE-2018_7602 {Fore.CYAN}on {Fore.GREEN}{target}{Style.RESET_ALL}.")

def handle_cve_2018_7600(target):

    print(f"{Fore.CYAN}[+] Starting scan for {Fore.YELLOW}CVE-2018_7600 {Fore.CYAN}on {Fore.GREEN}{target}{Style.RESET_ALL}...")

    scan_cve_2018_7600(target)

    print(f"{Fore.CYAN}[-] Completed scan for {Fore.YELLOW}CVE-2018_7600 {Fore.CYAN}on {Fore.GREEN}{target}{Style.RESET_ALL}.")
