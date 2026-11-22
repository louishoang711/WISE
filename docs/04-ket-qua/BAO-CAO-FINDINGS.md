# Báo cáo kết quả đánh giá bảo mật (Findings Report)

> Mẫu theo cấu trúc một **Pentest & Detection Report** thực tế — điền số liệu hoàn chỉnh sau khi kết thúc [Phase 03–05](../03-kich-ban/phase/README.md).  
> Tài liệu này tổng hợp cả chuỗi lỗ hổng (từ Wi-Fi yếu đến lộ Camera nội bộ) lẫn hiệu quả phát hiện của hệ thống **Wazuh WIDS**.

## 1. Tóm tắt điều hành (Executive Summary)

> *Gợi ý khung tóm tắt (cập nhật số liệu cuối sau Phase 05):*  
> Nhóm đã thực hiện đánh giá bảo mật thực nghiệm trên mô hình mạng không dây của quán cà phê / văn phòng nhỏ sử dụng router **TP-Link TL-WR940N v6** (`BSSID: AC:15:A2:80:26:99`) và **iPhone IP Camera nội bộ**. Kết quả cho thấy sự kết hợp của **3 lỗ hổng liên tiếp** (thiếu 802.11w PMF + mật khẩu WPA2 yếu → mạng phẳng không cách ly khách → dịch vụ camera không xác thực) cho phép kẻ tấn công từ bên ngoài phá khóa Wi-Fi, quét mạng LAN bằng `nmap` và xem trực tiếp hình ảnh camera nội bộ chỉ trong vài phút.  
> Ở chiều phòng thủ, hệ thống giám sát **Wazuh WIDS** (`tshark` + `sensor-wids.py` + Custom Decoder/Rules) đã phát hiện **100%** các đợt tấn công **Deauthentication Flood (Rule 100111, Level 12)** theo thời gian thực ngay ở giai đoạn đầu của chuỗi tấn công. Toàn bộ lỗ hổng sau đó đã được khắc phục và kiểm chứng thành công bằng 4 lớp phòng thủ: Mật khẩu mạnh, Tách mạng khách (*Guest Network Isolation*), Tắt WPS và chuẩn **802.11w (PMF)**.

## 2. Phạm vi & Phương pháp

- **Phạm vi được phép (In-Scope):** Xem [`docs/ROE.md`](../ROE.md).
- **Kịch bản & quy trình thực nghiệm:** Xem [`docs/03-kich-ban/kich-ban-demo.md`](../03-kich-ban/kich-ban-demo.md) và [`docs/03-kich-ban/phase/`](../03-kich-ban/phase/README.md).
- **Ánh xạ kỹ thuật tấn công:** Theo khung MITRE ATT&CK tại [`docs/ATTACK_MAPPING.md`](../ATTACK_MAPPING.md).

## 3. Bảng tổng hợp lỗ hổng (Findings Summary)

| ID | Tiêu đề lỗ hổng | Mức độ nghiêm trọng | Tactic / Technique (ATT&CK) | Trạng thái phát hiện bởi Wazuh WIDS | Trạng thái khắc phục (Phase 04) |
|---|---|---|---|---|---|
| **F-01** | AP không hỗ trợ/bật 802.11w (PMF) → bị tấn công Deauth Flood gây rớt mạng & lộ Handshake | **Cao** | `TA0040` Impact | ✅ **Phát hiện tức thì** (`Rule 100111`, Level 12 — đã test nổ 5,000+ alert ngày 16/11) | ✅ Kiểm chứng chống Deauth trên AP phụ bật 802.11w/WPA3 |
| **F-02** | Mật khẩu WPA2-PSK yếu dễ bị dò khóa từ điển ngoại tuyến (Offline Crack) | **Cao** | `TA0006` Credential Access (`T1110.002`) | ⚠️ Phát hiện hành vi Deauth ép lấy Handshake; **không** phát hiện bước crack offline | ✅ Đổi mật khẩu mạnh → crack lại bằng cùng wordlist thất bại |
| **F-03** | Dùng chung mạng phẳng & dịch vụ IP Camera nội bộ không xác thực → bị quét `Nmap` & lộ hình ảnh trực tiếp | **Cao** | `TA0007` Discovery (`T1046`), `TA0009` Collection | ❌ **Không phát hiện bởi WIDS L2** (lưu lượng đi trong Data Frame hợp lệ ở L3–L7) | ✅ Bật **Guest Network Isolation** trên TL-WR940N → chặn hoàn toàn truy cập từ mạng khách tới Camera |
| **F-04** | Tính năng WPS bật sẵn trên Router, tiềm ẩn nguy cơ bị dò mã PIN 8 chữ số | **Trung bình** | `TA0006` Credential Access (`T1110`) | ⚠️ Có sẵn `Rule 100120` (cần mở rộng sensor đếm burst gói Auth/Assoc) | ✅ Tắt hoàn toàn WPS trên Router → chạy lại `wash`/`reaver` thất bại |
| **F-05** | Bộ lọc địa chỉ MAC (MAC Filtering) dễ dàng bị vượt qua bằng kỹ thuật giả mạo MAC | **Thấp** | `TA0005` Defense Evasion | ❌ Không phát hiện (ngoài phạm vi cảm biến hiện tại) | ✅ Loại bỏ sự phụ thuộc vào lọc MAC trong chính sách an ninh |

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
