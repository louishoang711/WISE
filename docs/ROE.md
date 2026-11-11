# Rules of Engagement (ROE)

> Tài liệu chuẩn hóa phạm vi, quyền hạn và giới hạn của mọi hoạt động đánh giá trong dự án này —
> đúng khuôn mẫu một văn bản ROE trong pentest thật, thu nhỏ cho quy mô lab môn học.

## 1. Thông tin dự án

| Trường | Giá trị |
|---|---|
| Tên dự án | WISE — Wireless Attack & Detection Lab |
| Môn học | WISE432380 — An Toàn Mạng Không Dây và Di Động |
| Nhóm thực hiện | Huy (Red team), Hưng (Sensor), Khang (Blue team) |
| Người phê duyệt phạm vi | Giảng viên hướng dẫn |
| Thời gian hiệu lực | Trong suốt thời gian thực hiện đồ án (theo lịch học phần) |

## 2. Phạm vi được phép (In-Scope)

| Tài sản | Vai trò | Quyền sở hữu |
|---|---|---|
| Router TL-WR940N | AP mục tiêu | Thuộc sở hữu nhóm |
| Client (điện thoại/laptop cũ) | Nạn nhân mô phỏng | Thuộc sở hữu nhóm |
| Switch + dây mạng | Hạ tầng lab | Thuộc sở hữu nhóm |
| AP phụ WPA3 (hotspot điện thoại / hostapd) | Demo phòng thủ | Thuộc sở hữu nhóm |

## 3. Ngoài phạm vi (Out-of-Scope) — tuyệt đối không được đụng tới

- Bất kỳ SSID/BSSID nào **không thuộc sở hữu của nhóm**, kể cả khi nằm trong tầm sóng khi test
  (Wi-Fi hàng xóm, quán cà phê, ký túc xá, trường học...).
- Hạ tầng mạng thật của nhà trường, ISP, hoặc bên thứ ba.
- Dữ liệu cá nhân của người không tham gia dự án.

## 4. Kỹ thuật được phép thực hiện

| Kỹ thuật | Giới hạn |
|---|---|
| Trinh sát (airodump-ng) | Chỉ quét, không lưu thông tin AP ngoài phạm vi |
| Deauthentication flood | Chỉ nhắm `<CLIENT_MAC>` thuộc thiết bị lab |
| Bắt handshake / PMKID | Chỉ từ AP trong phạm vi |
| Crack offline (aircrack-ng / hashcat) | Chỉ chạy trên capture từ AP trong phạm vi |
| Tấn công WPS | Chỉ khi WPS được bật có chủ đích trên AP lab |
| MAC spoofing | Chỉ trên card của thành viên nhóm |

**Nghiêm cấm:** tấn công từ chối dịch vụ (DoS) kéo dài ra ngoài khung giờ demo, tấn công diện rộng
(quét nhiều AP lạ), và bất kỳ hành vi nào vượt quá bảng trên.

## 5. Cửa sổ thời gian (Time Window)

- Chỉ thực hiện tấn công trong khung giờ đã thống nhất giữa 3 thành viên (tránh ảnh hưởng mạng
  Wi-Fi dùng chung của nơi ở nếu lab đặt chung không gian).
- Dừng ngay nếu phát hiện AP lạ bị ảnh hưởng ngoài ý muốn (nhiễu sóng chéo kênh).

## 6. Liên lạc khi có sự cố

Nếu phát sinh ảnh hưởng ngoài phạm vi (vd: deauth vô tình lan sang AP hàng xóm do cùng kênh) →
**dừng ngay lập tức**, thông báo giữa 3 thành viên, ghi nhận vào `docs/04-ket-qua/` kèm thời điểm.

## 7. Phê duyệt

Văn bản này được xem là **đã phê duyệt nội bộ nhóm** khi cả Huy, Hưng, Khang đều xác nhận đã đọc,
trước khi bắt đầu Phase 3 (Tấn công) trong `docs/01-ke-hoach/roadmap.md`.

Tham chiếu: `docs/LEGAL_ETHICS.md` (cơ sở pháp lý), `docs/01-ke-hoach/roadmap.md` (lịch trình).
