# Phase 00 — Hạ tầng & Thiết bị (✅ Đã hoàn tất cài đặt)

> **Trạng thái:** **✅ Hạ tầng đã cài đặt và kiểm chứng xong.**  
> Khi chạy lại lab từ đầu, nhóm **không cần cài đặt lại** — chỉ cần thực hiện mục **"⚡ Bật nhanh trước buổi chạy (3 phút)"** ngay bên dưới rồi sang Phase 02 / Phase 03.

---

## ⚡ Bật nhanh trước buổi chạy Lab (3 phút)

- [ ] **1. Khang (Router & Mạng LAN):**
      - Cắm điện Router **TL-WR940N** (`BSSID: AC:15:A2:80:26:99`). Cắm 2 dây mạng từ cổng LAN router vào máy Hưng (`192.168.0.100`) và máy Khang (`192.168.0.102`, profile `WISE-Lab-LAN`).
      - Vào `http://192.168.0.1`: đặt SSID `Lab-Cafe-Wifi` (hoặc `WISE-Cafe-Staff`), cố định **Channel 7** (hoặc 6), mật khẩu WPA2-PSK **yếu** cho lượt đầu (`12345678` hoặc `CafeDemo2026`).
      - Kết nối thiết bị **Client nạn nhân** (điện thoại/iPhone; nếu chạy cả màn Camera thì bật app `SimpleIPCamera` quay tờ giấy `DEMO-01`) vào Wi-Fi trên.  
      → **Khang báo OK** kèm: `SSID`, `Channel`, `BSSID` (`AC:15:A2:80:26:99`).

- [ ] **2. Huy (Máy Attacker — `hungs`):**
      - Bật Monitor Mode đúng kênh AP:
        ```bash
        sudo airmon-ng check kill
        sudo airmon-ng start wlp1s0 7
        ```
      → **Huy báo OK** khi interface monitor đã lên đúng kênh.

- [ ] **3. Hưng (Máy Sensor — `Katana`):**
      - Bật Monitor Mode đúng kênh AP (vẫn giữ kết nối dây LAN với router):
        ```bash
        sudo airmon-ng check kill
        sudo airmon-ng start wlo1 7
        ```
      → **Hưng báo OK** để chuyển sang bật script ở [Phase 02](phase-02-pipeline-giam-sat.md).

---

## Hồ sơ hạ tầng đã hoàn tất trước đó (Lưu đối chiếu báo cáo)

- [x] **Phân bổ phần cứng 3 máy:**
      - Máy **`hungs` (`wlp1s0`)** → `Injection is working!` (100%) → **A — Attacker (Huy)**.
      - Máy **`Katana` (`wlo1`)** → Monitor mode thụ động + cáp LAN → **B — Sensor (Hưng)**.
      - Máy **Khang (`enxec1ac3125c1b`)** → Wazuh Manager + Indexer + Dashboard `4.9.2` → **C — Blue Team (Khang)**.
- [x] **Đấu nối LAN không cần Switch rời:** Tận dụng trực tiếp 4 cổng LAN tích hợp trên router TL-WR940N (`192.168.0.1/24`).
- [x] **Cài đặt công cụ:** Đã cài đầy đủ `AirHunt`, `aircrack-ng`, `reaver`, `nmap` trên máy Attacker; `tshark`, `python3`, `wazuh-agent` trên máy Sensor; và `Wazuh 4.9.2` trên máy Blue Team.
