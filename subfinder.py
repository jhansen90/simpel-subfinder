#!/usr/bin/env python3
import requests
import argparse
import sys
import os
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style, init

init(autoreset=True)
requests.packages.urllib3.disable_warnings()

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 13; Termux) SubFinder/2.0"
}

def banner():
    print(f"""{Fore.RED}
███████╗███████╗ ██████╗  ██████╗██╗███████╗████████╗██╗   ██╗
██╔════╝██╔════╝██╔═══██╗██╔════╝██║██╔════╝╚══██╔══╝╚██╗ ██╔╝
█████╗  ███████╗██║   ██║██║     ██║█████╗     ██║    ╚████╔╝ 
██╔══╝  ╚════██║██║   ██║██║     ██║██╔══╝     ██║     ╚██╔╝  
██║     ███████║╚██████╔╝╚██████╗██║███████╗   ██║      ██║   
╚═╝     ╚══════╝ ╚═════╝  ╚═════╝╚═╝╚══════╝   ╚═╝      ╚═╝   
{Fore.CYAN}
        Simple Subdomain Finder, FarizalXploit
       Instagram: @farizal_dzaky_anazili
              [ fsociety ]
    {Style.RESET_ALL}""")

def clean_domain(domain):
    domain = domain.lower().strip()
    if domain.startswith("http"):
        domain = domain.split("//")[-1].split("/")[0]
    return domain

def get_from_alienvault(domain):
    print(f"{Fore.BLUE}[*] Mengambil dari AlienVault OTX ...{Style.RESET_ALL}")
    subs = set()
    try:
        url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            data = r.json()
            for item in data.get("passive_dns", []):
                hostname = item.get("hostname", "").lower()
                if hostname.endswith(domain):
                    subs.add(hostname)
            print(f"{Fore.GREEN}[+] AlienVault: {len(subs)} ditemukan{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.YELLOW}[!] AlienVault gagal: {e}{Style.RESET_ALL}")
    return subs

def get_from_hackertarget(domain):
    print(f"{Fore.BLUE}[*] Mengambil dari HackerTarget ...{Style.RESET_ALL}")
    subs = set()
    try:
        url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200 and "error" not in r.text.lower():
            for line in r.text.splitlines():
                if "," in line:
                    sub = line.split(",")[0].strip().lower()
                    if sub.endswith(domain):
                        subs.add(sub)
            print(f"{Fore.GREEN}[+] HackerTarget: {len(subs)} ditemukan{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[!] HackerTarget limit / error{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.YELLOW}[!] HackerTarget gagal: {e}{Style.RESET_ALL}")
    return subs

def get_from_crtsh(domain):
    print(f"{Fore.BLUE}[*] Mengambil dari crt.sh (cadangan) ...{Style.RESET_ALL}")
    subs = set()
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        r = requests.get(url, headers=headers, timeout=25)
        if r.status_code == 200:
            data = r.json()
            for entry in data:
                name = entry.get("name_value", "")
                for sub in name.split("\n"):
                    sub = sub.strip().lower()
                    if sub.endswith(domain) and "*" not in sub:
                        subs.add(sub)
            print(f"{Fore.GREEN}[+] crt.sh: {len(subs)} ditemukan{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.YELLOW}[!] crt.sh gagal (timeout/normal): {e}{Style.RESET_ALL}")
    return subs

def get_from_urlscan(domain):
    print(f"{Fore.BLUE}[*] Mengambil dari urlscan.io ...{Style.RESET_ALL}")
    subs = set()
    try:
        url = f"https://urlscan.io/api/v1/search/?q=domain:{domain}&size=100"
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            for result in data.get("results", []):
                page = result.get("page", {})
                host = page.get("domain", "").lower()
                if host.endswith(domain):
                    subs.add(host)
            print(f"{Fore.GREEN}[+] urlscan.io: {len(subs)} ditemukan{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.YELLOW}[!] urlscan gagal: {e}{Style.RESET_ALL}")
    return subs

def get_from_rapiddns(domain):
    print(f"{Fore.BLUE}[*] Mengambil dari RapidDNS ...{Style.RESET_ALL}")
    subs = set()
    try:
        url = f"https://rapiddns.io/subdomain/{domain}?full=1"
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            found = re.findall(rf"[\w\.-]+\.{re.escape(domain)}", r.text, re.I)
            for sub in found:
                subs.add(sub.lower())
            print(f"{Fore.GREEN}[+] RapidDNS: {len(subs)} ditemukan{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.YELLOW}[!] RapidDNS gagal: {e}{Style.RESET_ALL}")
    return subs

def save_results(subdomains, output_file):
    sorted_subs = sorted(subdomains)
    with open(output_file, "w", encoding="utf-8") as f:
        for sub in sorted_subs:
            f.write(f"https://{sub}\n")
    print(f"\n{Fore.GREEN}[✓] Hasil disimpan ke → {output_file}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[✓] Total subdomain unik: {len(sorted_subs)}{Style.RESET_ALL}")

def main():
    banner()

    parser = argparse.ArgumentParser(description="Subdomain Finder v2")
    parser.add_argument("domain", help="Domain target (contoh: example.com)")
    parser.add_argument("-o", "--output", default="subdomains.txt", help="File output")
    args = parser.parse_args()

    domain = clean_domain(args.domain)
    print(f"{Fore.CYAN}[*] Target Domain : {domain}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}[*] Output File   : {args.output}{Style.RESET_ALL}\n")

    all_subs = set()

    sources = [
        get_from_alienvault,
        get_from_hackertarget,
        get_from_urlscan,
        get_from_rapiddns,
        get_from_crtsh,
    ]

    for func in sources:
        try:
            result = func(domain)
            all_subs.update(result)
        except Exception as e:
            print(f"{Fore.RED}[!] Error di salah satu sumber: {e}{Style.RESET_ALL}")

    if not all_subs:
        print(f"\n{Fore.RED}[!] Tidak ada subdomain yang ditemukan dari semua sumber.{Style.RESET_ALL}")
        return

    save_results(all_subs, args.output)

    print(f"\n{Fore.YELLOW}--- Preview ---{Style.RESET_ALL}")
    for sub in sorted(all_subs)[:15]:
        print(f"  {sub}")
    if len(all_subs) > 15:
        print(f"  ... dan {len(all_subs)-15} lainnya")

if __name__ == "__main__":
    main()