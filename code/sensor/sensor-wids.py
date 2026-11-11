#!/usr/bin/env python3
"""
Cảm biến WIDS - do Hưng (Sensor) chạy trên máy đã bật monitor mode.

Nhiệm vụ: nghe các frame deauthentication / disassociation trên không khí, mỗi lần thấy thì
ghi một dòng log theo định dạng mà decoder của Khang (Wazuh) hiểu được.

Dùng tshark (cài: sudo apt install tshark). Đơn giản và ổn định cho đồ án; nếu muốn dùng
Kismet làm WIDS thay thế thì đọc alert qua REST API của Kismet rồi ghi cùng định dạng này.

Cách chạy (thay wlan0mon bằng tên interface monitor của bạn, xem bằng `iw dev`):
    sudo python3 sensor-wids.py wlan0mon

Trước đó phải bật monitor mode đúng kênh của AP:
    sudo airmon-ng check kill
    sudo airmon-ng start wlan0 6        # 6 = kênh của AP TL-WR940N
"""

import subprocess
import sys

IFACE = sys.argv[1] if len(sys.argv) > 1 else "wlan0mon"
LOGFILE = "/var/log/wifi-wids.log"

# wlan.fc.type_subtype: 0x0c = deauthentication, 0x0a = disassociation
DISPLAY_FILTER = "wlan.fc.type_subtype==0x0c || wlan.fc.type_subtype==0x0a"

cmd = [
    "tshark", "-i", IFACE, "-l", "-n",
    "-Y", DISPLAY_FILTER,
    "-T", "fields",
    "-e", "wlan.sa",      # source address (thường là AP bị giả mạo)
    "-e", "wlan.da",      # destination (client bị nhắm tới)
    "-e", "wlan.bssid",
    "-E", "separator=,",
]

print(f"[+] Cam bien WIDS dang nghe tren {IFACE}, ghi vao {LOGFILE}")
print("[+] Nhan Ctrl+C de dung.")

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
try:
    with open(LOGFILE, "a") as f:
        for line in proc.stdout:
            parts = line.strip().split(",")
            if len(parts) < 3:
                continue
            sa, da, bssid = parts[0], parts[1], parts[2]
            if not bssid:
                bssid = sa
            client = da if da else "unknown"
            f.write(f"WIFI-WIDS type=deauth bssid={bssid} client={client} channel=0 count=1\n")
            f.flush()
except KeyboardInterrupt:
    print("\n[+] Da dung cam bien.")
    proc.terminate()
