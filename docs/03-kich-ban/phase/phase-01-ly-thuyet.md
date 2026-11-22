# Phase 01 — Lý thuyết nền & Tài liệu (Mỗi người tự viết, song song)

> **Phụ thuộc:** Không — có thể làm bất cứ lúc nào, không cần đợi thiết bị.  
> **Mục tiêu:** Hoàn thành các mục lý thuyết của báo cáo (Chương 1–2).  
> **Tham chiếu:** [`docs/03-kich-ban/kich-ban-demo.md`](../kich-ban-demo.md) (Mục 7).

Phase này **không có thứ tự bắt buộc giữa 3 người** (ai viết phần của mình độc lập), nhưng vẫn giữ nếp "báo OK" để Khang biết khi nào tổng hợp được vào báo cáo.

## Checklist (Mỗi người báo OK khi xong phần của mình)

- [ ] **Huy viết:**
      - Frame quản lý 802.11, cơ chế Deauthentication, 4-Way Handshake (Earle Ch5, Ch13) và nguyên lý quét dịch vụ LAN sau xâm nhập Wi-Fi (`nmap`).
      - Đánh giá công cụ **AirHunt** (chuẩn đầu ra **G4.2**, Earle Ch16): kiến trúc, chức năng, so sánh với `aircrack-ng` / `wifite2` / `airgeddon`.
      - **Lưu ý đưa vào bài đánh giá:** AirHunt **không hỗ trợ PMKID** (chỉ liệt kê `hcxtools` ở References, không có trong Features — xem [`nhat-ky-phien-16-11-2026.md`](../../04-ket-qua/nhat-ky-phien-16-11-2026.md) mục 2) và cũng không có tính năng quét IP/camera trong LAN (phải kết hợp `nmap`). Đồng thời ghi rõ lỗi code thật đã phát hiện: hàm `start_monitor_mode()` thiếu bước `airmon-ng check kill` trước khi bật monitor, khiến monitor mode không ổn định — đây là bằng chứng thực nghiệm cụ thể cho phần đánh giá công cụ.  
      → **Báo OK** khi bản viết xong, có trích dẫn nguồn đúng chuẩn.

- [ ] **Hưng viết:**
      - Monitor Mode vs Managed Mode.
      - Khái niệm WIDS (Wireless Intrusion Detection System) và ranh giới giữa giám sát vô tuyến tầng 2 (L2) với giám sát mạng nội bộ tầng 3–7 (L3–L7).
      - Giới thiệu `tshark` / `Kismet` (công cụ đang dùng làm cảm biến ở Phase 02).  
      → **Báo OK** khi bản viết xong, có trích dẫn nguồn đúng chuẩn.

- [ ] **Khang viết:**
      - WEP/WPA/WPA2/WPA3, 802.1X, chính sách an ninh WLAN (Earle Ch12, Ch14; Osterhage mục 3.7).
      - Kiến trúc phòng thủ đa lớp: 802.11w (PMF), phân đoạn mạng khách (Guest Network Isolation / VLAN), bảo mật dịch vụ IoT/Camera nội bộ (chuẩn đầu ra **G4.1**, Earle Ch15).  
      → **Báo OK** khi bản viết xong, có trích dẫn nguồn đúng chuẩn.

## Verify

Mỗi mục có trích dẫn nguồn đúng chuẩn (Earle, Osterhage, tài liệu Wazuh/Aircrack-ng/Nmap — xem danh mục tham khảo ở [`docs/03-kich-ban/kich-ban-demo.md`](../kich-ban-demo.md) mục 7).

## Ship

Gom cả 3 phần vào Chương 1–2 của báo cáo cuối ([`docs/05-bao-cao/`](../../05-bao-cao/)).
