import subprocess
import argparse
import sys
import concurrent.futures
from colorama import init, Fore, Style

# Inisialisasi colorama untuk warna
init(autoreset=True)

def check_proxy(url, proxy, protocol):
    try:
        # Menggunakan socat untuk melakukan pengecekan proxy
        cmd = [
            'timeout', '10', 'socat', 
            f'{protocol.upper()}-CONNECT:{url}', 
            f'{protocol.lower()}://[{proxy}]'
        ]
        
        result = subprocess.run(cmd, 
                                stdout=subprocess.PIPE, 
                                stderr=subprocess.PIPE, 
                                text=True, 
                                timeout=10)
        
        if result.returncode == 0:
            print(f"{Fore.GREEN}[ACTIVE] {proxy} - {protocol.upper()}")
            return proxy, protocol
        else:
            print(f"{Fore.RED}[INACTIVE] {proxy} - {protocol.upper()}")
            return None
    except Exception as e:
        print(f"{Fore.RED}[ERROR] {proxy} - {protocol.upper()}: {str(e)}")
        return None

def check_proxies(url, proxy_list, protocols=None):
    if not protocols:
        protocols = ['http', 'https', 'socks4', 'socks5']
    
    active_proxies = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        
        with open(proxy_list, 'r') as f:
            for line in f:
                proxy = line.strip()
                if not proxy:
                    continue
                
                for protocol in protocols:
                    futures.append(
                        executor.submit(check_proxy, url, proxy, protocol)
                    )
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                active_proxies.append(result)
    
    return active_proxies

def main():
    parser = argparse.ArgumentParser(description='Proxy Checker')
    parser.add_argument('-u', '--url', required=True, help='Target URL or connection string')
    parser.add_argument('-p', '--proxy_list', required=True, help='Path to proxy list file')
    parser.add_argument('-x', '--protocol', nargs='+', help='Specific protocols to check')
    
    args = parser.parse_args()
    
    active_proxies = check_proxies(args.url, args.proxy_list, args.protocol)
    
    print("\n--- Active Proxies Summary ---")
    for proxy, protocol in active_proxies:
        print(f"{Fore.GREEN}{proxy} - {protocol.upper()}")

if __name__ == '__main__':
    main()
