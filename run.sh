#!/bin/bash

# Fungsi untuk menampilkan teks berwarna
function green() {
  printf "\e[32m$1\e[0m\n"
}

function red() {
  printf "\e[31m$1\e[0m\n"
}

# Parsing argumen
while getopts "u:p:x:" opt; do
  case $opt in
    u) url=$OPTARG ;;
    p) proxy_list=$OPTARG ;;
    x) protocol=$OPTARG ;;
    *) exit 1 ;;
  esac
done

# Periksa apakah parameter yang diperlukan tersedia
if [[ -z $url || -z $proxy_list ]]; then
  echo "Usage: $0 -u <url> -p <proxy_list.txt> [-x <protocol>]"
  exit 1
fi

# Validasi protokol jika disediakan
if [[ -n $protocol && ! $protocol =~ ^(http|https|socks4|socks5)$ ]]; then
  echo "Invalid protocol. Supported protocols are: http, https, socks4, socks5"
  exit 1
fi

# Membaca file proxy_list
if [[ ! -f $proxy_list ]]; then
  echo "Proxy list file not found: $proxy_list"
  exit 1
fi

# Fungsi untuk memeriksa proxy
function check_proxy() {
  local proxy=$1
  local proto=$2
  local host=$(echo $proxy | cut -d: -f1)
  local port=$(echo $proxy | cut -d: -f2)

  # Menggunakan socat untuk memeriksa koneksi
  if echo -e "GET / HTTP/1.1\r\nHost: $url\r\n\r\n" | socat - PROXY:$host:$port,$proto,proxyport=$port >/dev/null 2>&1; then
    green "ACTIVE: $proto://$proxy"
  else
    red "FAILED: $proto://$proxy"
  fi
}

# Loop melalui proxy_list
while IFS= read -r proxy; do
  if [[ -z $protocol ]]; then
    # Periksa semua protokol jika tidak ada protokol tertentu
    for proto in http https socks4 socks5; do
      check_proxy $proxy $proto
    done
  else
    # Periksa hanya protokol tertentu
    check_proxy $proxy $protocol
  fi
done < "$proxy_list"
