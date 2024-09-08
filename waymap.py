from thirdparty.urlcrazy import run_urlcrazy
from thirdparty.scrapy_spider import run_scrapy
from thirdparty.spiderfoot import run_spiderfoot
from thirdparty.httrack import run_httrack
from thirdparty.wayback_machine import run_wayback_machine
from modules.url_filter.remove_duplicates import remove_duplicates
from thirdparty.waf_detection import run_waf_detection
import requests
import os

def test_connection(domain):
    """Test connection to the target domain."""
    try:
        response = requests.get(domain, timeout=10)
        if response.status_code == 200:
            print(f"[*] Successfully connected to {domain}")
            return True
        else:
            print(f"[!] Unexpected status code {response.status_code} when connecting to {domain}")
            return False
    except requests.ConnectionError as e:
        print(f"[!] Failed to connect to {domain}: {str(e)}")
        return False
    except requests.Timeout:
        print(f"[!] Connection to {domain} timed out.")
        return False
    
def retry_request(domain, max_retries=3):
    """Retry the connection up to max_retries times if the connection is lost."""
    retries = 0
    while retries < max_retries:
        if test_connection(domain):
            return True
        retries += 1
        print(f"[*] Retry {retries}/{max_retries}...")
    print("[!] Maximum retries reached. Aborting.")
    return False


def run_waf_check(domain):
    """Check for WAF and ask the user if they want to continue if WAF is detected."""
    print(f"[*] Checking for WAF protection on {domain}...")
    waf_detected = run_waf_detection(domain)

    if waf_detected:
        print("[CRITICAL] WAF detected! Proceeding might trigger security alerts.")
        user_input = input("[*] Do you want to continue? (y/N): ").strip().lower()
        if user_input != 'y':
            print("[*] Aborting operation due to WAF detection.")
            return False
    return True


def run_scraping(domain):
    # Create a session directory in the SQLMap style
    session_dir = f"sessions/{domain}"
    os.makedirs(session_dir, exist_ok=True)

    # Define the output file where all URLs will be appended
    all_urls_file = f"{session_dir}/all_urls.txt"
    unique_urls_file = f"{session_dir}/unique_urls.txt"
    
    # Clear the file at the start to ensure fresh collection of URLs
    open(all_urls_file, 'w').close()

    # Run third-party scraping tools and append output to all_urls.txt
    run_urlcrazy(domain, all_urls_file)
    run_scrapy(all_urls_file)
    run_spiderfoot(domain, all_urls_file)
    run_httrack(domain, all_urls_file)
    run_wayback_machine(domain, all_urls_file)

    # Remove duplicate URLs from the collected list
    remove_duplicates(all_urls_file, unique_urls_file)

    print(f"[*] Scraping completed. Unique URLs saved to {unique_urls_file}")

def run_waymap(domain):
    # Test the initial connection
    if not test_connection(domain):
        print("[*] Unable to connect to the target domain.")
        return

    # Run WAF detection and ask if user wants to continue if WAF is found
    if not run_waf_check(domain):
        return

    # Proceed to scraping with a retry mechanism in case of lost connection
    if not retry_request(domain):
        return
    
    print(f"[*] Starting scraping process on {domain}...")
    run_scraping(domain)

    print("[*] Scraping process completed.")
