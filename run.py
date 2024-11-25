import argparse
import subprocess
from termcolor import colored

def check_proxy(url, proxy, protocol):
    # Membentuk perintah socat berdasarkan protokol
    if protocol == "http":
        socat_command = f"socat - TCP:{url},proxy={proxy}"
    elif protocol == "https":
        socat_command = f"socat - openssl:{url},proxy={proxy}"
    elif protocol == "socks4":
        socat_command = f"socat - SOCKS4:{url},proxy={proxy}"
    elif protocol == "socks5":
        socat_command = f"socat - SOCKS5:{url},proxy={proxy}"
    else:
        print(f"Unknown protocol: {protocol}")
        return False
    
    # Menjalankan perintah socat dan menangkap status
    try:
        result = subprocess.run(socat_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    parser = argparse.ArgumentParser(description="Proxy checker using socat")
    parser.add_argument("-u", "--url", required=True, help="URL to check the proxy against")
    parser.add_argument("-p", "--proxy_list", required=True, help="Path to the proxy list file")
    parser.add_argument("-x", "--protocol", choices=["http", "https", "socks4", "socks5"], help="Protocol type to check (optional)")

    args = parser.parse_args()
    
    # Membaca daftar proxy dari file
    with open(args.proxy_list, 'r') as file:
        proxies = file.readlines()

    # Menghapus karakter newline pada proxy
    proxies = [proxy.strip() for proxy in proxies]
    
    # Jika protokol tidak diberikan, memeriksa semua protokol
    protocols_to_check = [args.protocol] if args.protocol else ["http", "https", "socks4", "socks5"]
    
    # Memeriksa setiap proxy dengan setiap protokol
    for proxy in proxies:
        for protocol in protocols_to_check:
            if check_proxy(args.url, proxy, protocol):
                print(colored(f"Proxy {proxy} dengan protokol {protocol} berhasil terhubung ke {args.url}", 'green'))
            else:
                print(colored(f"Proxy {proxy} dengan protokol {protocol} gagal terhubung ke {args.url}", 'red'))

if __name__ == "__main__":
    main()
