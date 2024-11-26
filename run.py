import argparse
import requests
from termcolor import colored

# Fungsi untuk mengecek proxy
def check_proxy(protocol, proxy, url):
    try:
        # Pastikan URL memiliki protokol yang sesuai
        if not url.startswith(("http://", "https://")):
            url = f"http://{url}"  # Tambahkan default protokol http

        proxies = {protocol: f"{protocol}://{proxy}"}
        
        # Menggunakan requests untuk mengakses URL dengan proxy
        response = requests.get(url, proxies=proxies, timeout=1)
        
        if response.status_code == 200:
            print(colored(f"Proxy aktif: {proxy}", "green"))
        else:
            print(colored(f"Proxy tidak aktif: {proxy}", "red"))

    except Exception:
        print(colored(f"Proxy tidak valid atau gagal: {proxy}", "red"))

# Fungsi utama
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Proxy Checker untuk Mining Pool")
    parser.add_argument("-u", required=True, help="URL Pool Mining")
    parser.add_argument("-x", required=True, help="Nama file list proxy (txt)")
    parser.add_argument("-p", required=True, help="Jenis protokol proxy (http, https, socks4, socks5)")

    args = parser.parse_args()
    url = args.u
    proxy_file = args.x
    protocol = args.p.lower()

    # Validasi protokol
    if protocol not in ["http", "https", "socks4", "socks5"]:
        print("Protokol tidak valid! Gunakan http, https, socks4, atau socks5.")
        exit(1)

    # Membaca file proxy
    try:
        with open(proxy_file, "r") as file:
            proxies = [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print("File list proxy tidak ditemukan!")
        exit(1)

    # Mengecek setiap proxy
    for proxy in proxies:
        check_proxy(protocol, proxy, url)
