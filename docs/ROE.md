# Rules of Engagement (ROE)

> Tài liệu chuẩn hóa phạm vi, quyền hạn và giới hạn của mọi hoạt động đánh giá trong dự án này —
> đúng khuôn mẫu một văn bản ROE trong pentest thật, thu nhỏ cho quy mô lab môn học.

## 1. Thông tin dự án

| Trường | Giá trị |
|---|---|
| Tên dự án | WISE — Wireless Attack & Detection Lab |
| Môn học | WISE432380 — An Toàn Mạng Không Dây và Di Động |
| Nhóm thực hiện | Huy (Red Team), Hưng (Wireless Sensor), Khang (Blue Team) |
| Người phê duyệt phạm vi | Giảng viên hướng dẫn |
| Thời gian hiệu lực | Trong suốt thời gian thực hiện đồ án (theo lịch học phần) |

## 2. Phạm vi được phép (In-Scope)

| Tài sản | Vai trò | Quyền sở hữu |
|---|---|---|
| Router TP-Link TL-WR940N v6 (`AC:15:A2:80:26:99`) | AP mục tiêu & cổng LAN nội bộ | Thuộc sở hữu nhóm |
| iPhone (chạy ứng dụng IP Camera nội bộ) | Client nạn nhân kiêm Camera mô phỏng (chỉ quay tờ giấy `DEMO-01`/`DEMO-02`) | Thuộc sở hữu nhóm |
| 3 Laptop thành viên + cáp mạng LAN | Máy Attacker (A), Sensor (B), Wazuh Manager (C) | Thuộc sở hữu nhóm |
| AP phụ WPA3/PMF (hotspot điện thoại / `hostapd`) | Demo kiểm chứng phòng thủ 802.11w | Thuộc sở hữu nhóm |

## 3. Ngoài phạm vi (Out-of-Scope) — Tuyệt đối không được đụng tới

- Bất kỳ SSID/BSSID nào **không thuộc sở hữu của nhóm**, kể cả khi nằm trong tầm sóng khi test (Wi-Fi hàng xóm, quán cà phê thật, ký túc xá, trường học...).
- Hạ tầng mạng thật của nhà trường, ISP, hoặc bên thứ ba.
- Dữ liệu cá nhân hoặc hình ảnh của người không tham gia dự án (camera trong lab **chỉ quay tờ giấy mã cảnh `DEMO-01` / `DEMO-02`**, tuyệt đối không quay khách hay người thật).

## 4. Kỹ thuật được phép thực hiện

| Kỹ thuật | Giới hạn |
|---|---|
| Trinh sát vô tuyến (`airodump-ng` / AirHunt) | Chỉ ghi nhận thông tin AP và Client trong phạm vi lab |
| Deauthentication Flood (`aireplay-ng` / AirHunt) | Chỉ nhắm vào BSSID lab (`AC:15:A2:80:26:99`) và `<CLIENT_MAC>` thuộc thiết bị của nhóm |
| Bắt 4-Way Handshake | Chỉ thu từ AP trong phạm vi lab |
| Crack mật khẩu ngoại tuyến (`aircrack-ng`) | Chỉ chạy trên file capture thu từ AP trong phạm vi lab |
| Quét mạng LAN (`nmap`) & Mở URL Camera | Chỉ quét trong dải LAN cách ly của router nhóm (`192.168.0.0/24`) và chỉ truy cập URL camera mô phỏng trên iPhone của nhóm |
| Tấn công WPS (`wash` / `reaver`) | Chỉ thực hiện khi WPS được bật có chủ đích trên AP lab |
| MAC Spoofing | Chỉ thực hiện trên card mạng của thành viên nhóm |

**Nghiêm cấm:** tấn công từ chối dịch vụ (DoS) kéo dài ra ngoài khung giờ thực nghiệm, quét `nmap` trên mạng công cộng/mạng trường, và bất kỳ hành vi nào vượt quá bảng trên.

## 5. Cửa sổ thời gian (Time Window)

- Chỉ thực hiện tấn công trong khung giờ đã thống nhất giữa 3 thành viên.
- Dừng ngay nếu phát hiện AP lạ bị ảnh hưởng ngoài ý muốn (nhiễu sóng chéo kênh).

## 6. Liên lạc khi có sự cố

Nếu phát sinh ảnh hưởng ngoài phạm vi → **dừng ngay lập tức**, thông báo giữa 3 thành viên, ghi nhận vào [`docs/04-ket-qua/`](04-ket-qua/) kèm thời điểm.

## 7. Phê duyệt

Văn bản này được xem là **đã phê duyệt nội bộ nhóm** khi cả Huy, Hưng, Khang đều xác nhận đã đọc trước khi bắt đầu [Phase 03 (Tấn công)](03-kich-ban/phase/phase-03-tan-cong.md).

Tham chiếu: [`docs/LEGAL_ETHICS.md`](LEGAL_ETHICS.md) (cơ sở pháp lý), [`docs/03-kich-ban/phase/README.md`](03-kich-ban/phase/README.md) (lịch trình thực thi).
