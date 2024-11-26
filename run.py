import socket
import argparse
import socks

def check_proxy(proxy_ip, proxy_port, pool_ip, pool_port, protocol):
    try:
        if protocol in ['http', 'https']:
            # HTTP/HTTPS proxy
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((proxy_ip, proxy_port))
            sock.sendall(f'CONNECT {pool_ip}:{pool_port} HTTP/1.1\r\nHost: {pool_ip}:{pool_port}\r\n\r\n'.encode('utf-8'))
            response = sock.recv(1024)
            if b"200 Connection established" in response:
                print(f"Proxy {proxy_ip}:{proxy_port} berhasil terhubung ke pool {pool_ip}:{pool_port}.")
            else:
                print(f"Proxy {proxy_ip}:{proxy_port} gagal terhubung: {response.decode('utf-8')}")
        elif protocol in ['socks4', 'socks5']:
            # SOCKS proxy
            socks.set_default_proxy(getattr(socks, protocol.upper()), proxy_ip, proxy_port)
            sock = socks.socksocket()
            sock.settimeout(5)
            sock.connect((pool_ip, pool_port))
            sock.sendall(f'{"{"} "method": "mining.authorize", "params": ["username", "password"], "id": 1 {"}"}\n'.encode('utf-8'))
            response = sock.recv(1024)
            print(f"Proxy {proxy_ip}:{proxy_port} berhasil terhubung ke pool {pool_ip}:{pool_port}. Respon: {response.decode('utf-8')}")
        else:
            print("Protokol tidak dikenali.")
    except (socket.timeout, socket.error) as e:
        print(f"Proxy {proxy_ip}:{proxy_port} tidak dapat terhubung: {e}")
    finally:
        sock.close()

def main():
    parser = argparse.ArgumentParser(description='Proxy Checker untuk Stratum+TCP.')
    parser.add_argument('-u', '--url', required=True, help='URL pool mining (misal: pool.example.com:3333)')
    parser.add_argument('-x', '--proxy_list', required=True, help='File yang berisi daftar proxy (satu per baris)')
    parser.add_argument('-p', '--protocol', choices=['http', 'https', 'socks4', 'socks5'], required=True, help='Jenis protokol proxy')
    
    args = parser.parse_args()
    
    # Mengambil informasi pool
    pool_info = args.url.split(':')
    pool_ip = pool_info[0]
    pool_port = int(pool_info[1])  # Mengambil port dari URL pool
    
    # Membaca daftar proxy dari file
    with open(args.proxy_list, 'r') as f:
        proxies = [line.strip().split(':') for line in f.readlines()]

    for proxy in proxies:
        if len(proxy) == 2:
            proxy_ip, proxy_port = proxy
            check_proxy(proxy_ip, int(proxy_port), pool_ip, pool_port, args.protocol)

if __name__ == '__main__':
    main()
