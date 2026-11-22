# Nhật ký phiên làm việc — 14-16/11/2026 (Khang) & Cập nhật 22/11/2026

> Ghi lại quá trình dựng hạ tầng + pipeline giám sát (Phase 00 + Phase 02), các lỗi gặp phải,
> cách sửa, kết quả test end-to-end đầu tiên và tiến độ chuẩn hóa tài liệu. Dùng để đối chiếu khi viết báo cáo và bàn giao thông tin giữa Huy / Hưng / Khang.

---

## 1. Hạ tầng (Phase 00)

### 1.1 Router TL-WR940N v6
- Cấu hình lúc test 16/11: SSID mặc định ban đầu là `TP-Link_269A` (cần đổi thành `Lab-Cafe-Wifi` hoặc `WISE-Cafe-Staff` khi quay demo chính thức). BSSID thực: **`AC:15:A2:80:26:99`**.
- Kênh thực tế: **kênh 7** (ổn định suốt quá trình test). Đã xác minh kênh KHÔNG bị "Auto" trôi lung tung như nghi ngờ ban đầu — chỉ là header của `airodump-ng` khi quét (hopping scan) hiển thị kênh đang nhảy tới ở header, khác với cột `CH` của từng BSSID (là kênh thật, cố định).
- 4 cổng LAN trên router là đủ, **không cần switch rời** — cắm thẳng 2 dây LAN (Hưng `192.168.0.100` + Khang `192.168.0.102`) vào 2 cổng LAN của router.

### 1.2 Máy Khang — Mạng LAN
- Máy không có cổng Ethernet vật lý sẵn → dùng adapter USB-to-Ethernet (`enxec1ac3125c1b`).
- Sự cố đã xử lý: NetworkManager tự áp 1 profile tĩnh cũ tên `M02-Lab` (IP `10.20.0.10/24`) → đã xóa `M02-Lab`, tạo profile mới `WISE-Lab-LAN` (DHCP tự động) → nhận đúng IP `192.168.0.102/24` từ router, ping router (`192.168.0.1`) thành công 0% mất gói.
- Wi-Fi (`wlp1s0`) và dây LAN chạy song song bình thường, không xung đột.

### 1.3 Wazuh (Khang)
- Wazuh 4.9.2 (Manager + Indexer + Dashboard) đã cài sẵn trên máy Khang, chạy ổn định.
- Đã copy `local_decoder.xml` + `local_rules.xml` vào `/var/ossec/etc/...`, test bằng `wazuh-logtest` thành công: Rule `100110` (level 4, 1 gói) → Rule `100111` (level 12, đủ 5 gói/10s) nổ đúng như thiết kế.

---

## 2. AirHunt & Kịch bản — Xác minh công cụ và chuẩn hóa mạch Demo

- Xác nhận AirHunt là công cụ tại [github.com/Debajyoti0-0/AirHunt](https://github.com/Debajyoti0-0/AirHunt), đã tải sẵn tại `~/Desktop/AirHunt`. Toàn bộ dependency (`aircrack-ng`, `reaver`, `bully`, `wifite`, `ifconfig`, `iw`) đã có sẵn trên máy.
- Đối chiếu tính năng AirHunt: hỗ trợ Recon, Deauth, Handshake capture+crack, WPS — **không hỗ trợ PMKID** (chỉ liệt kê `hcxtools` ở mục References, không có trong Features).
- **Lỗi phát hiện trong code AirHunt:** hàm `start_monitor_mode()` chỉ chạy `airmon-ng start <iface>`, **thiếu bước `airmon-ng check kill`** trước đó → `NetworkManager`/`wpa_supplicant` giành lại card, khiến `aireplay-ng` bị kẹt ở `"Waiting for beacon frame"`. Cách khắc phục: chạy tay `sudo airmon-ng check kill` trước khi mở AirHunt → Đưa vào phần đánh giá công cụ (Chuẩn đầu ra **G4.2**).
- **Cập nhật kịch bản (22/11/2026):**
  - Đã **xóa hoàn toàn PMKID** khỏi toàn bộ tài liệu và sơ đồ SVG.
  - Đã **gộp kịch bản Camera iPhone (`SimpleIPCamera` quay mã cảnh `DEMO-01`/`DEMO-02`) + quét LAN bằng `nmap` + phòng thủ bằng tách mạng khách (`Guest Network Isolation`)** vào mạch chính tại [`docs/03-kich-ban/kich-ban-demo.md`](../03-kich-ban/kich-ban-demo.md) và [`docs/03-kich-ban/phase/`](../03-kich-ban/phase/README.md), đồng thời xóa file `.docx` rời và các file kế hoạch cũ bị trùng lặp.

---

## 3. Phase 02 — Đăng ký Wazuh Agent (Hưng)

- Lần 1 (thủ công): tạo agent `001 LeThaiHung` qua `manage_agents` → bị `"Never connected"` do Hưng enroll tự động qua biến `WAZUH_MANAGER` (cổng 1515).
- Đã đồng bộ version agent khớp bản `4.9.2` của Manager.
- Lưu ý vận hành Dashboard: nếu bấm refresh liên tục sẽ gặp `[API connection] No API available to connect` do API bị rate-limit (`429 Too Many Requests`) → khắc phục bằng `sudo systemctl restart wazuh-manager` + đợi vài giây.
- **Kết quả cuối:** Agent **`002 hungs`** (IP `192.168.0.100`, Ubuntu 24.04.5 LTS, v4.9.2) — **Active** thành công.

---

## 4. Test end-to-end đầu tiên (Deauth thật)

- Huy chạy Deauth qua AirHunt nhắm vào BSSID `ac:15:a2:80:26:99` (kênh 7).
- **Kết quả: THÀNH CÔNG** — Wazuh Dashboard ghi nhận **23,387+ sự kiện**, trong đó **5,000 cảnh báo mức 12** (Rule `100111` "Deauth flood") nổ liên tục trong khung giờ ~11:24–11:25 (16/11), đúng lúc Huy chạy lệnh.
- **3 phát hiện kỹ thuật quan trọng đã đưa vào kịch bản:**
  1. **Nhiễu từ mạng hàng xóm:** `sensor-wids.py` ban đầu chưa lọc theo BSSID nên bắt luôn deauth của các mạng xung quanh (`AMR_WIFI`, `UBND`, `Mandan`...). Khi lọc theo `data.bssid: "ac:15:a2:80:26:99"` (**chữ thường**) thì ra đúng dữ liệu của lab.
  2. **Chế độ Deauth:** Lần test đầu dùng `"Deauth ALL clients"` (broadcast). Khi đo số liệu chính thức ở Phase 03/05 nên chạy đúng chế độ `"Deauth 1 client"` (`-c <CLIENT_MAC>`).
  3. **Giới hạn định danh kẻ tấn công:** Frame Deauth không ký số và luôn giả mạo địa chỉ nguồn bằng BSSID của AP, nên WIDS phát hiện được hành vi tấn công nhưng không thể chỉ ra MAC thật của attacker → giải pháp gốc rễ là **802.11w (PMF)**.

---

## 5. Phương pháp phân tích log trên Wazuh (Dùng cho Phase 05)

1. Lọc đúng BSSID nhóm (chữ thường: `data.bssid: "ac:15:a2:80:26:99"`) + `rule.id: (100110 OR 100111)` trong Security Events.
2. Zoom vào đúng khung giờ tấn công trên histogram.
3. Sort `timestamp` tăng dần, tìm dòng `100111` đầu tiên → đối chiếu giờ Huy bấm lệnh → tính **thời gian phát hiện**.
4. Đếm tổng số `100110` / `100111` trong khung đã zoom.
5. Lọc ngoài khung giờ tấn công (cùng BSSID) → kiểm tra **False Positive** (kỳ vọng = `0`).
6. Lặp lại ~10 lần tấn công để lấy trung bình.

---

## 6. Checklist công việc của nhóm

- [x] Bỏ Màn 4 (PMKID) khỏi toàn bộ tài liệu + sơ đồ SVG, đồng thời gộp kịch bản Camera iPhone + Nmap + Guest Network Isolation vào [`docs/03-kich-ban/kich-ban-demo.md`](../03-kich-ban/kich-ban-demo.md) và [`docs/03-kich-ban/phase/`](../03-kich-ban/phase/README.md).
- [x] Thêm phần "Giới hạn định danh kẻ tấn công / 802.11 management frame không ký số" và "Ranh giới WIDS L2 vs Nmap/HTTP L3–L7" vào kịch bản demo.
- [x] Xóa các file thừa/trùng lặp (`Kich-ban-WiFi-camera-iPhone-ba-thanh-vien.docx`, `roadmap.md`, `huong-dan-nhom.md`) và cập nhật lại `README.md`.
- [ ] Đổi SSID router từ `TP-Link_269A` → `Lab-Cafe-Wifi` (hoặc `WISE-Cafe-Staff`) và cài `SimpleIPCamera` trên iPhone quay tờ giấy `DEMO-01`.
- [ ] Cập nhật `code/sensor/sensor-wids.py` (hoặc truyền tham số BSSID) để lọc theo đúng BSSID router nhóm (`ac:15:a2:80:26:99`) ngay tại nguồn.
- [ ] Xóa agent thừa `001 LeThaiHung` trên Wazuh Manager (`manage_agents` → `R` → `001`).
- [ ] Chạy full mạch Phase 03 (Deauth 1 client → Crack Handshake → Nmap tìm IP Camera → Xem mã cảnh `DEMO-02`) và Phase 04 (Mật khẩu mạnh + Tách mạng khách `WISE-Cafe-Guest` chặn xem camera + Tắt WPS + 802.11w PMF).
