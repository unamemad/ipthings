import socket
import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing

def domain_to_ip(domain):
    try:
        with closing(socket.create_connection((domain, 80), timeout=20)) as conn:
            ip_address = conn.getpeername()[0]
        return (domain, ip_address)
    except socket.gaierror:
        print(f"[-]  {domain}")
        return (domain, None)
    except socket.timeout:
        print(f"[-]  {domain}")
        return (domain, None)
    except OSError as e:
        print(f"[-]  {domain}")
        return (domain, None)

def read_domains_from_file(filename):
    with open(filename, 'r') as file:
        domains = [line.strip() for line in file.readlines()]
    return domains

def resolve_domains_in_parallel(domains, max_workers):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(domain_to_ip, domains)
    return dict(results)

def save_ips_to_file(filename, ip_addresses):
    with open(filename, 'a') as file:
        for domain, ip in ip_addresses.items():
            if ip is not None:
                print (f"{domain}: {ip}\n")
                file.write(f"{domain}: {ip}\n")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Resolve domain names to IP addresses.")
    parser.add_argument("-l", "--input", dest="input_file", required=True,
                        help="Path to the input file containing domain names, one per line.")
    parser.add_argument("-o", "--output", dest="output_file", required=True,
                        help="Path to the output file where IP addresses will be saved.")
    parser.add_argument("-t", "--threads", dest="num_threads", type=int, default=200,
                        help="Number of threads to use (default: 200)")
    return parser.parse_args()

def print_banner():
    banner = r"""
 ____    ____       _       ______     _________  _____   ______  ________  _______      
|_   \  /   _|     / \     |_   _ `.  |  _   _  ||_   _|.' ___  ||_   __  ||_   __ \     
  |   \/   |      / _ \      | | `. \ |_/ | | \_|  | | / .'   \_|  | |_ \_|  | |__) |    
  | |\  /| |     / ___ \     | |  | |     | |      | | | |   ____  |  _| _   |  __ /     
 _| |_\/_| |_  _/ /   \ \_  _| |_.' /    _| |_    _| |_\ `.___]  |_| |__/ | _| |  \ \_   
|_____||_____||____| |____||______.'    |_____|  |_____|`._____.'|________||____| |___|  
Domain To IP Grabber | Its Gonna help you in BB/BH | Fast , secure , free | mad tiger 
                              hunterkhayrol@yahoo.com
                                                                                         
"""
    print(banner)

if __name__ == "__main__":
    print_banner()
    args = parse_arguments()
    domains = read_domains_from_file(args.input_file)
    ip_addresses = resolve_domains_in_parallel(domains, max_workers=args.num_threads)
    save_ips_to_file(args.output_file, ip_addresses)
    print(f"IP addresses have been saved to {args.output_file}.")

