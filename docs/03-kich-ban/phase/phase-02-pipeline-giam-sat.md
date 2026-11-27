# Phase 02 — Pipeline giám sát Cảm biến → Wazuh (✅ Đã cài đặt xong)

> **Trạng thái:** **✅ Đã cài đặt xong Wazuh Agent cho Hưng (`002 hungs`), đã cấu hình `<localfile>`, và đã nạp `local_decoder.xml` + `local_rules.xml` trên Wazuh Manager của Khang.**  
> Khi chạy lại lab từ đầu, chỉ cần thực hiện **3 bước khởi động** dưới đây (khoảng 2 phút) là có thể bắt đầu ngay [Phase 03 (Tấn công)](phase-03-tan-cong.md).

---

## ⚡ Khởi động Pipeline trước khi chạy lại Lab (2 phút)

- [ ] **Bước 1 (Hưng — Làm sạch log cũ & Chạy cảm biến có lọc BSSID):**
      - Để dữ liệu của lần chạy lại từ đầu không bị lẫn với log thử nghiệm hôm trước, xóa hoặc làm rỗng file log cũ rồi chạy `sensor-wids.py` **kèm tham số BSSID của router nhóm** (`ac:15:a2:80:26:99` — code `sensor-wids.py` đã được cập nhật hỗ trợ lọc BSSID ở tham số thứ 2):
        ```bash
        sudo truncate -s 0 /var/log/wifi-wids.log
        sudo systemctl restart wazuh-agent
        sudo python3 code/sensor/sensor-wids.py wlo1mon ac:15:a2:80:26:99
        ```
      - Mở thêm 1 terminal phụ để quan sát dòng log sinh ra theo thời gian thực:
        ```bash
        sudo tail -F /var/log/wifi-wids.log
        ```
      → **Hưng báo OK** khi terminal hiện `[+] Dang loc theo BSSID muc tieu: ac:15:a2:80:26:99`.

- [ ] **Bước 2 (Khang — Kiểm tra Agent Active & Mở Dashboard):**
      -*(Nếu chưa xóa agent thừa `001 LeThaiHung` tạo nhầm lúc đầu thì chạy nhanh `sudo /var/ossec/bin/manage_agents` → `R` → `001`)*.
      - Mở Wazuh Dashboard trên trình duyệt, xác nhận Agent **`002 hungs` (`192.168.0.100`)** đang ở trạng thái **Active**.
      - Vào mục **Security Events**, đặt sẵn bộ lọc:
        `data.bssid: "ac:15:a2:80:26:99" AND rule.id: (100110 OR 100111)`  
      → **Khang báo OK** khi Dashboard đã sẵn sàng — cả nhóm chuyển ngay sang **[Phase 03 — Thực hiện tấn công](phase-03-tan-cong.md)**!

---

## Hồ sơ cấu hình Pipeline đã hoàn tất (Lưu đối chiếu báo cáo)

- [x] **Cấu hình Wazuh Agent trên máy Hưng (`/var/ossec/etc/ossec.conf`):**
      Đã thêm khối `<localfile>` đọc `/var/log/wifi-wids.log` (định dạng `syslog`) và enroll thành công thành Agent **`002 hungs`** (Ubuntu 24.04.5, Wazuh v4.9.2).
- [x] **Cấu hình Decoder & Rules trên máy Khang (`/var/ossec/etc/`):**
      Đã nạp [`code/wazuh/local_decoder.xml`](../../../code/wazuh/local_decoder.xml) và [`code/wazuh/local_rules.xml`](../../../code/wazuh/local_rules.xml), kiểm chứng qua `wazuh-logtest` và thực nghiệm nổ thành công:
      - `Rule 100100` (Level 3): Nhận diện sự kiện `wifi-wids`.
      - `Rule 100110` (Level 4): Phát hiện 1 gói Deauth đơn lẻ.
      - `Rule 100111` (Level 12): Phát hiện **Tấn công Deauth Flood** (cảm biến gom gói theo cửa sổ 1 giây; rule nổ khi `count >= 5` trong một dòng log).
- [x] **Cập nhật [`code/sensor/sensor-wids.py`](../../../code/sensor/sensor-wids.py):**
      Đã bổ sung bộ lọc `TARGET_BSSID` (tham số dòng lệnh thứ 2) và tự động chuẩn hóa MAC về chữ thường để loại bỏ hoàn toàn nhiễu Deauth từ các mạng Wi-Fi hàng xóm ngay tại nguồn.
