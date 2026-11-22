# Báo cáo kết quả đánh giá bảo mật (Findings Report)

> Mẫu theo cấu trúc một **Pentest & Detection Report** thực tế — điền số liệu hoàn chỉnh sau khi kết thúc [Phase 03–05](../03-kich-ban/phase/README.md).  
> Tài liệu này tổng hợp cả chuỗi lỗ hổng (từ Wi-Fi yếu đến lộ Camera nội bộ) lẫn hiệu quả phát hiện của hệ thống **Wazuh WIDS**.

## 1. Tóm tắt điều hành (Executive Summary)

Kịch bản lab mô phỏng mạng Wi-Fi dùng chung với camera nội bộ trên router **TP-Link TL-WR940N v6**. Nhóm đánh giá rủi ro gián đoạn Wi-Fi, thông tin xác thực yếu và truy cập camera từ mạng dùng chung.

Phiên 16/11/2026 ghi nhận hơn 23.387 sự kiện Wazuh, trong đó có 5.000 cảnh báo Deauth Flood mức 12 (`Rule 100111`). Tỉ lệ phát hiện, độ trễ và bằng chứng trước và sau phòng thủ sẽ được bổ sung từ Phase 04–05. [Nhật ký thực nghiệm](nhat-ky-phien-16-11-2026.md) · [Ma trận phạm vi phát hiện](../../assets/so-do/ban-do-tan-cong.svg)

## 2. Phạm vi & Phương pháp

- **Phạm vi được phép (In-Scope):** Xem [`docs/ROE.md`](../ROE.md).
- **Kịch bản & quy trình thực nghiệm:** Xem [`docs/03-kich-ban/kich-ban-demo.md`](../03-kich-ban/kich-ban-demo.md) và [`docs/03-kich-ban/phase/`](../03-kich-ban/phase/README.md).
- **Ánh xạ kỹ thuật tấn công:** Theo khung MITRE ATT&CK tại [`docs/ATTACK_MAPPING.md`](../ATTACK_MAPPING.md).

## 3. Bảng tổng hợp lỗ hổng (Findings Summary)

| ID | Tiêu đề lỗ hổng | Mức độ nghiêm trọng | Tactic / Technique (ATT&CK) | Trạng thái phát hiện bởi Wazuh WIDS | Trạng thái khắc phục (Phase 04) |
|---|---|---|---|---|---|
| **F-01** | AP không hỗ trợ/bật 802.11w (PMF) → bị tấn công Deauth Flood gây rớt mạng & lộ Handshake | **Cao** | `TA0040` Impact | Đã ghi nhận 5.000 cảnh báo mức 12 từ `Rule 100111` ngày 16/11 | Kiểm chứng trên AP phụ hỗ trợ 802.11w/WPA3 theo Phase 04 |
| **F-02** | Mật khẩu WPA2-PSK yếu dễ bị dò khóa từ điển ngoại tuyến (Offline Crack) | **Cao** | `TA0006` Credential Access (`T1110.002`) | WIDS có thể thấy Deauth đi kèm. Dò khóa ngoại tuyến nằm ngoài phạm vi quan sát. | Kiểm chứng tác dụng của mật khẩu mạnh theo Phase 04 |
| **F-03** | Dùng chung mạng phẳng & dịch vụ IP Camera nội bộ không xác thực → bị quét `Nmap` & lộ hình ảnh trực tiếp | **Cao** | `TA0007` Discovery (`T1046`), `TA0009` Collection | Luồng LAN/HTTP nằm ngoài phạm vi của cảm biến frame quản lý 802.11. | Kiểm chứng Guest Network Isolation theo Phase 04 |
| **F-04** | Tính năng WPS bật sẵn trên Router, tiềm ẩn nguy cơ bị dò mã PIN 8 chữ số | **Trung bình** | `TA0006` Credential Access (`T1110`) | Đã có `Rule 100120`. Cảm biến hiện chưa sinh sự kiện WPS. | Kiểm chứng sau khi tắt WPS theo Phase 04 |
| **F-05** | Bộ lọc địa chỉ MAC (MAC Filtering) dễ dàng bị vượt qua bằng kỹ thuật giả mạo MAC | **Thấp** | `TA0005` Defense Evasion | Thiếu dữ liệu để xác minh định danh từ frame thu được. | Giảm phụ thuộc vào lọc MAC trong chính sách an ninh |

**Thang mức độ nghiêm trọng** (định tính dựa trên Khả năng khai thác × Tác động thực tế): **Nghiêm trọng > Cao > Trung bình > Thấp > Thông tin**.

## 4. Chi tiết từng lỗ hổng (Finding Details)

Mẫu trình bày chi tiết cho từng mã `F-01` → `F-05` trong báo cáo chính thức:

```markdown
### F-0X — {Tiêu đề lỗ hổng}

- **Mức độ nghiêm trọng:** {Cao / Trung bình / Thấp}
- **Thành phần ảnh hưởng:** {Router TL-WR940N v6 / iPhone IP Camera / Giao thức IEEE 802.11}
- **Mô tả kỹ thuật:** {Giải thích nguyên nhân gốc rễ, ví dụ: Management Frame 0x0c không có chữ ký số IGTK/BIP...}
- **Bằng chứng khai thác (PoC):** {Lệnh đã chạy trên AirHunt/Nmap, trích đoạn log `/var/log/wifi-wids.log`, ảnh chụp cảnh báo Wazuh Rule 100111 hoặc ảnh trình duyệt xem mã cảnh `DEMO-02`}
- **Tác động:** {Gián đoạn kết nối, lộ mật khẩu Wi-Fi, hoặc kẻ tấn công xem trộm hình ảnh camera nội bộ của quán}
- **Khuyến nghị & Kết quả kiểm chứng sau khi vá:** {Tham chiếu kết quả thực nghiệm ở Phase 04 — kèm ảnh đối chiếu Trước vá vs Sau vá}
```

## 5. Số liệu định lượng hệ thống giám sát Wazuh (Metrics — Điền sau Phase 05)

| Màn / Kỹ thuật | Thời gian phát hiện TB (s) | Tỉ lệ phát hiện đúng (%) | False Positive (sau lọc BSSID) | Ghi chú đánh giá WIDS |
|---|---|---|---|---|
| **Màn 0 — Baseline** | — | — | `0` (kỳ vọng) | Mốc đối chiếu khi mạng hoạt động bình thường |
| **Màn 1 — Recon (`airodump-ng`)** | Không phát hiện | `0%` | `0` | Giới hạn tự nhiên: trinh sát hoàn toàn thụ động |
| **Màn 2 — Deauth Flood** | `___ giây` | `100%` (kỳ vọng) | `0` | **Thế mạnh cốt lõi của WIDS** (`Rule 100110` → `100111`) |
| **Màn 3 — Handshake + Crack** | `___ giây` (ở pha Deauth) | Phát hiện pha ép rớt mạng | `0` | Bắt được hành vi cưỡng bức lấy Handshake; mù trước crack offline |
| **Màn 4 — Nmap LAN & HTTP Camera** | Không phát hiện bởi WIDS L2 | `0%` | `0` | Lưu lượng tầng L3–L7 của client đã xác thực WPA2; cần NIDS hoặc Guest Isolation |
| **Màn phụ — WPS Attack** | Tùy chọn | Tùy chọn | — | Có sẵn `Rule 100120` trong `local_rules.xml` |

## 6. Kết luận & Khuyến nghị theo thứ tự ưu tiên

1. **Ưu tiên 1 (Khắc phục ngay trên thiết bị hiện có — Chi phí 0đ):**
   - Áp dụng mật khẩu WPA2-PSK mạnh (≥ 14 ký tự ngẫu nhiên) và **tắt ngay WPS** trên Router TL-WR940N.
   - Bật **Guest Network (`WISE-Cafe-Guest`)** cho khách và **tắt tùy chọn *"Allow Guest To Access My Local Network"*** để cách ly hoàn toàn mạng khách khỏi mạng nội bộ chứa IP Camera.
   - Bật xác thực tài khoản/mật khẩu trên ứng dụng/thiết bị IP Camera.
2. **Ưu tiên 2 (Giám sát liên tục):**
   - Duy trì cảm biến **Wazuh WIDS** (`sensor-wids.py` có lọc theo BSSID của quán) để phát hiện tức thì mọi đợt tấn công Deauth / ép bắt Handshake ngay từ bước đầu tiên.
3. **Ưu tiên 3 (Nâng cấp phần cứng dài hạn):**
   - Nâng cấp Access Point lên thiết bị hỗ trợ **WPA3-SAE** và bắt buộc bật **802.11w (PMF — Protected Management Frames)** để loại bỏ hoàn toàn khả năng giả mạo gói Deauthentication.
