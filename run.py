import argparse
import subprocess
import sys
import os

# Warna untuk output
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def check_proxy(url, proxy, protocol):
    try:
        # Periksa jenis protokol
        if protocol == "http" or protocol == "https":
            command = f"socat - TCP:{url},proxy={proxy}"
        elif protocol == "socks4":
            command = f"socat - SOCKS4:{url},proxy={proxy}"
        elif protocol == "socks5":
            command = f"socat - SOCKS5:{url},proxy={proxy}"
        else:
            raise ValueError("Protokol tidak valid.")

        # Jalankan perintah socat dan periksa apakah proxy berhasil terhubung
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            print(f"{GREEN}[Aktif] Proxy {proxy} untuk {protocol} terhubung ke {url}{RESET}")
        else:
            print(f"{RED}[Tidak Aktif] Proxy {proxy} untuk {protocol} gagal terhubung ke {url}{RESET}")
    
    except Exception as e:
        print(f"{RED}[Error] {e}{RESET}")

def main():
    # Parsing argumen
    parser = argparse.ArgumentParser(description="Proxy Checker dengan socat")
    parser.add_argument('-u', '--url', required=True, help='URL atau alamat pool mining (misal: http://google.com)')
    parser.add_argument('-p', '--proxy_list', required=True, help='File yang berisi daftar proxy dan port')
    parser.add_argument('-x', '--protocol', choices=['http', 'https', 'socks4', 'socks5'], help='Jenis protokol (optional)')

    args = parser.parse_args()

    # Baca daftar proxy dari file
    try:
        with open(args.proxy_list, 'r') as f:
            proxies = f.readlines()
    except FileNotFoundError:
        print(f"{RED}[Error] File {args.proxy_list} tidak ditemukan!{RESET}")
        sys.exit(1)

    # Periksa proxy untuk setiap baris di file proxy
    for proxy in proxies:
        proxy = proxy.strip()  # Menghapus spasi atau baris kosong
        if not proxy:
            continue
        
        # Jika protokol tidak diberikan, periksa semua protokol
        if not args.protocol:
            for protocol in ['http', 'https', 'socks4', 'socks5']:
                check_proxy(args.url, proxy, protocol)
        else:
            check_proxy(args.url, proxy, args.protocol)

if __name__ == "__main__":
    main()
