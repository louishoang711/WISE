#!/usr/bin/env python3
"""
Cảm biến WIDS - do Hưng (Sensor) chạy trên máy đã bật monitor mode.

Nhiệm vụ: nghe frame deauthentication / disassociation trên không khí và ghi log cho Wazuh.
Cảm biến cũng nghe beacon để biết tên Wi-Fi (SSID) của từng BSSID, nên mỗi dòng log có đủ:
  BSSID bị nhắm, tên Wi-Fi, MAC nguồn (src), MAC nhận (client), kênh, tín hiệu (dBm), reason code.

Gom theo cửa sổ thời gian (mặc định 1 giây): thay vì ghi 1 dòng cho mỗi gói (một đợt flood
10.000 gói sẽ làm Wazuh agent tràn bộ đệm và rớt log), cảm biến ghi 1 dòng / (BSSID, client, src)
mỗi cửa sổ, kèm count = số gói trong cửa sổ đó.

Dùng tshark (cài: sudo apt install tshark).

Cách chạy (thay wlan0mon bằng tên interface monitor của bạn, xem bằng `iw dev`):
    # Bắt mọi BSSID xung quanh:
    sudo python3 code/sensor/sensor-wids.py wlan0mon

    # Khuyên dùng khi chạy lab — chỉ lọc đúng BSSID của router nhóm để loại nhiễu hàng xóm:
    sudo python3 code/sensor/sensor-wids.py wlan0mon ac:15:a2:80:26:99

    # Đổi cửa sổ gom (giây), nhỏ hơn thì báo sớm hơn:
    sudo python3 code/sensor/sensor-wids.py wlan0mon ac:15:a2:80:26:99 --window 0.5

Trước đó phải bật monitor mode đúng kênh của AP:
    sudo airmon-ng check kill
    sudo airmon-ng start wlan0 7        # kênh của AP TL-WR940N, xác nhận bằng airodump-ng
"""

import argparse
import subprocess
import threading
import time

LOGFILE = "/var/log/wifi-wids.log"

# wlan.fc.type_subtype: 0x0c = deauthentication, 0x0a = disassociation, 0x08 = beacon
SUBTYPE_NAME = {0x0C: "deauth", 0x0A: "disassoc"}
BEACON = 0x08
DISPLAY_FILTER = (
    "wlan.fc.type_subtype==0x0c || wlan.fc.type_subtype==0x0a || wlan.fc.type_subtype==0x08"
)
FIELDS = [
    "wlan.fc.type_subtype",
    "wlan.sa",
    "wlan.da",
    "wlan.bssid",
    "wlan.ssid",
    "wlan_radio.channel",
    "wlan_radio.signal_dbm",
    "wlan.fixed.reason_code",
]


def first(value):
    """tshark có thể trả nhiều giá trị cách nhau bằng dấu phẩy; lấy giá trị đầu."""
    return value.split(",")[0].strip() if value else ""


def clean_ssid(ssid):
    return ssid.replace('"', "").replace("\n", " ").strip()


class Aggregator:
    """Gom gói theo (loại, bssid, src, client) rồi ghi 1 dòng log mỗi cửa sổ."""

    def __init__(self, logfile, window):
        self.window = window
        self.lock = threading.Lock()
        self.buckets = {}
        self.ssids = {}
        self.stop = threading.Event()
        self.f = open(logfile, "a")

    def set_ssid(self, bssid, ssid):
        if ssid:
            with self.lock:
                self.ssids[bssid] = clean_ssid(ssid)

    def add(self, kind, bssid, src, client, channel, signal, reason):
        key = (kind, bssid, src, client)
        with self.lock:
            b = self.buckets.setdefault(
                key, {"count": 0, "signal_sum": 0, "signal_n": 0, "channel": channel, "reason": reason}
            )
            b["count"] += 1
            if signal is not None:
                b["signal_sum"] += signal
                b["signal_n"] += 1
            if channel:
                b["channel"] = channel
            if reason:
                b["reason"] = reason

    def flush(self):
        with self.lock:
            buckets, self.buckets = self.buckets, {}
            ssids = dict(self.ssids)
        for (kind, bssid, src, client), b in buckets.items():
            signal = round(b["signal_sum"] / b["signal_n"]) if b["signal_n"] else 0
            ssid = ssids.get(bssid, "unknown")
            self.f.write(
                f'WIFI-WIDS type={kind} bssid={bssid} ssid="{ssid}" src={src} client={client} '
                f'channel={b["channel"] or 0} signal={signal} reason={b["reason"] or 0} '
                f'count={b["count"]}\n'
            )
        if buckets:
            self.f.flush()

    def run(self):
        while not self.stop.wait(self.window):
            self.flush()
        self.flush()


def to_int(value, default=None):
    try:
        return int(value, 0)
    except (TypeError, ValueError):
        return default


def main():
    ap = argparse.ArgumentParser(description="Cam bien WIDS: deauth/disassoc -> log cho Wazuh")
    ap.add_argument("iface", nargs="?", default="wlan0mon")
    ap.add_argument("bssid", nargs="?", default="", help="chi giu BSSID nay (khuyen dung)")
    ap.add_argument("--window", type=float, default=1.0, help="cua so gom goi, giay (mac dinh 1)")
    ap.add_argument("--log", default=LOGFILE, help=f"file log (mac dinh {LOGFILE})")
    args = ap.parse_args()

    target = args.bssid.strip().lower()

    cmd = ["tshark", "-i", args.iface, "-l", "-n", "-Y", DISPLAY_FILTER, "-T", "fields", "-E", "separator=/t"]
    for field in FIELDS:
        cmd += ["-e", field]

    print(f"[+] Cam bien WIDS dang nghe tren {args.iface}, ghi vao {args.log} (cua so gom {args.window}s)")
    if target:
        print(f"[+] Dang loc theo BSSID muc tieu: {target}")
    else:
        print("[!] Khong loc BSSID (ghi moi mang xung quanh). Truyen tham so thu 2 de loc BSSID.")
    print("[+] Nhan Ctrl+C de dung.")

    agg = Aggregator(args.log, args.window)
    flusher = threading.Thread(target=agg.run, daemon=True)
    flusher.start()

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)
    try:
        for line in proc.stdout:
            parts = line.rstrip("\n").split("\t")
            parts += [""] * (len(FIELDS) - len(parts))
            subtype = to_int(parts[0].strip())
            sa, da, bssid = (p.strip().lower() for p in parts[1:4])
            ssid = parts[4]
            channel = to_int(first(parts[5]), 0)
            signal = to_int(first(parts[6]))
            reason = to_int(first(parts[7]), 0)

            if not bssid:
                bssid = sa
            if target and target not in (bssid, sa, da):
                continue

            if subtype == BEACON:
                agg.set_ssid(bssid, ssid)
                continue
            kind = SUBTYPE_NAME.get(subtype)
            if kind is None:
                continue
            agg.add(kind, bssid, sa or "unknown", da or "unknown", channel, signal, reason)
    except KeyboardInterrupt:
        print("\n[+] Da dung cam bien.")
    finally:
        proc.terminate()
        agg.stop.set()
        flusher.join()


if __name__ == "__main__":
    main()
