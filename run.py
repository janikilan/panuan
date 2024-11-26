import subprocess
import sys
import time
import threading

def check_proxy(proxy, protocol, url):
  """Memeriksa proxy dan mengembalikan True jika aktif, False jika tidak."""
  try:
    # Gunakan socat untuk menguji koneksi
    if protocol == "socks4":
      cmd = f"socat -4 -v PROXY:{proxy} - | python -c 'import requests; r = requests.get(\"{url}\"); print(r.status_code)'"
    elif protocol == "socks5":
      cmd = f"socat -5 -v PROXY:{proxy} - | python -c 'import requests; r = requests.get(\"{url}\"); print(r.status_code)'"
    elif protocol == "http":
      cmd = f"socat -v TCP4:{proxy} - | python -c 'import requests; r = requests.get(\"{url}\"); print(r.status_code)'"
    elif protocol == "https":
      cmd = f"socat -v TCP4:{proxy} - | python -c 'import requests; r = requests.get(\"{url}\"); print(r.status_code)'"
    else:
      return False
    
    # Jalankan perintah socat
    output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode("utf-8")
    
    # Periksa kode status
    if int(output.strip()) == 200:
      return True
    else:
      return False
  except Exception as e:
    return False

def check_proxies(proxy_list, url, protocols):
  """Memeriksa daftar proxy dan mencetak hasilnya."""
  for proxy in proxy_list:
    # Pisahkan proxy dan port
    proxy, port = proxy.strip().split(":")

    for protocol in protocols:
      start_time = time.time()
      is_active = check_proxy(f"{proxy}:{port}", protocol, url)
      duration = time.time() - start_time

      if is_active:
        print(f"\033[32mProxy {proxy}:{port} aktif ({protocol}) [{duration:.2f} detik]\033[0m")
      else:
        print(f"\033[31mProxy {proxy}:{port} tidak aktif ({protocol}) [{duration:.2f} detik]\033[0m")

def main():
  # Periksa argumen
  url = None
  proxy_list_file = None
  protocols = ["http", "https", "socks4", "socks5"]

  for i, arg in enumerate(sys.argv):
    if arg == "-u":
      url = sys.argv[i + 1]
    elif arg == "-p":
      proxy_list_file = sys.argv[i + 1]
    elif arg == "-x":
      protocols = [sys.argv[i + 1]]

  if not url or not proxy_list_file:
    print("Error: Parameter -u (URL) dan -p (proxy_list.txt) harus diberikan.")
    sys.exit(1)

  # Baca daftar proxy
  with open(proxy_list_file, "r") as f:
    proxy_list = f.readlines()

  # Jalankan pemeriksaan proxy secara bersamaan
  threads = []
  for protocol in protocols:
    thread = threading.Thread(target=check_proxies, args=(proxy_list, url, [protocol]))
    thread.start()
    threads.append(thread)

  # Tunggu semua thread selesai
  for thread in threads:
    thread.join()

if __name__ == "__main__":
  main()
