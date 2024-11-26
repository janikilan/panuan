import subprocess
import sys
import time
import threading
from colorama import Fore, init

init(autoreset=True)  # Initialize colorama for colored output


def check_proxy(url, proxy, protocol):
    """
    Mengecek proxy dengan socat.

    Args:
        url: URL untuk diakses.
        proxy: Proxy dalam format "host:port".
        protocol: Protocol proxy (http, https, socks4, socks5).

    Returns:
        True jika proxy aktif, False jika tidak.
    """

    command = [
        "socat",
        f"TCP4:{proxy}",
        f"SYSTEM:'curl -s -k -m 5 -x {protocol}://{proxy} {url}'",
        "-v",
    ]
    try:
        subprocess.run(command, capture_output=True, check=True, timeout=5)
        return True
    except subprocess.CalledProcessError:
        return False
    except subprocess.TimeoutExpired:
        return False


def check_proxy_list(url, proxy_list, protocol):
    """
    Mengecek proxy dalam list.

    Args:
        url: URL untuk diakses.
        proxy_list: Path ke file list proxy.
        protocol: Protocol proxy (http, https, socks4, socks5).
    """
    with open(proxy_list, "r") as file:
        for line in file:
            proxy = line.strip()
            start_time = time.time()
            if check_proxy(url, proxy, protocol):
                elapsed_time = time.time() - start_time
                print(
                    f"{Fore.GREEN}Proxy {proxy} [{protocol}] {url} aktif (waktu: {elapsed_time:.2f} detik)"
                )
            else:
                print(f"{Fore.RED}Proxy {proxy} [{protocol}] {url} tidak aktif")


def main():
    """
    Fungsi utama untuk menjalankan script.
    """
    url = None
    proxy_list = None
    protocol = ["http", "https", "socks4", "socks5"]  # Default all protocols

    for i, arg in enumerate(sys.argv):
        if arg == "-u":
            url = sys.argv[i + 1]
        elif arg == "-p":
            proxy_list = sys.argv[i + 1]
        elif arg == "-x":
            protocol = [sys.argv[i + 1]]

    if url and proxy_list:
        for p in protocol:
            check_proxy_list(url, proxy_list, p)
    else:
        print(
            f"{Fore.RED}Error: Parameter -u (URL) dan -p (proxy_list) harus diberikan."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
