import requests
import concurrent.futures
import socket
import socks

def check_proxy_requests(url, proxy, protocol):
    try:
        # Konfigurasi proxy berdasarkan protokol
        proxies = {
            'http': f'http://{proxy}',
            'https': f'https://{proxy}',
            'socks4': f'socks4://{proxy}',
            'socks5': f'socks5://{proxy}'
        }
        
        response = requests.get(
            url, 
            proxies={'http': proxies[protocol], 'https': proxies[protocol]},
            timeout=10
        )
        
        if response.status_code == 200:
            print(f"{Fore.GREEN}[ACTIVE] {proxy} - {protocol.upper()}")
            return proxy, protocol
    except Exception as e:
        print(f"{Fore.RED}[INACTIVE] {proxy} - {protocol.upper()}: {str(e)}")
    
    return None

def check_proxy_socket(url, proxy, protocol):
    try:
        # Parsing proxy
        host, port = proxy.split(':')
        port = int(port)
        
        # Konfigurasi socket proxy
        if protocol == 'socks4':
            socks.set_default_proxy(socks.SOCKS4, host, port)
        elif protocol == 'socks5':
            socks.set_default_proxy(socks.SOCKS5, host, port)
        
        # Buat socket
        socket.socket = socks.socksocket
        
        # Coba koneksi
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.close()
        
        print(f"{Fore.GREEN}[ACTIVE] {proxy} - {protocol.upper()}")
        return proxy, protocol
    except Exception as e:
        print(f"{Fore.RED}[INACTIVE] {proxy} - {protocol.upper()}: {str(e)}")
    
    return None

def check_proxies(url, proxy_list, protocols=None):
    if not protocols:
        protocols = ['http', 'https', 'socks4', 'socks5']
    
    active_proxies = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
        futures = []
        
        with open(proxy_list, 'r') as f:
            for line in f:
                proxy = line.strip()
                if not proxy:
                    continue
                
                for protocol in protocols:
                    # Gabungkan metode pengecekan
                    futures.append(
                        executor.submit(check_proxy_requests, url, proxy, protocol)
                    )
                    futures.append(
                        executor.submit(check_proxy_socket, url, proxy, protocol)
                    )
        
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result and result not in active_proxies:
                active_proxies.append(result)
    
    return active_proxies
