# Báo cáo kết quả đánh giá (Findings Report)

> Mẫu theo đúng cấu trúc một **pentest report** thật — điền vào sau khi hoàn thành Phase 3–5.
> Không phải báo cáo học thuật thông thường; đây là tài liệu nộp được cho khách hàng/giảng viên
> như một bài đánh giá bảo mật thực thụ.

## 1. Tóm tắt điều hành (Executive Summary)

> Viết 1 đoạn ngắn, không thuật ngữ kỹ thuật, dành cho người không rành kỹ thuật đọc được: mục
> tiêu đánh giá, số lỗ hổng tìm thấy theo mức độ, kết luận tổng quan về khả năng giám sát (WIDS).

_(Điền sau khi có số liệu)_

## 2. Phạm vi & phương pháp

- Phạm vi: xem `docs/ROE.md`.
- Phương pháp: tấn công thực nghiệm trên lab cách ly, đối chiếu với cảnh báo từ hệ thống giám sát
  Wazuh, đo thời gian phát hiện và tỉ lệ chính xác. Ánh xạ kỹ thuật theo `docs/ATTACK_MAPPING.md`.

## 3. Bảng tổng hợp lỗ hổng (Findings Summary)

| ID | Tiêu đề | Mức độ nghiêm trọng | Tactic (ATT&CK) | Trạng thái phát hiện bởi WIDS |
|---|---|---|---|---|
| F-01 | AP không bật 802.11w (PMF) → bị deauth giả mạo | **Cao** | TA0040 Impact | ✅ Phát hiện (Màn 2) |
| F-02 | Mật khẩu WPA2 yếu dễ bị crack offline | **Cao** | TA0006 Credential Access | ⚠️ Phát hiện hành vi ép rớt mạng, không phát hiện việc crack |
| F-03 | WPS bật, lộ PIN 8 số | **Trung bình** | TA0006 Credential Access | ⚠️ Tùy chọn (xem `docs/02-huong-dan/huong-dan-nhom.md` mục 4) |
| F-04 | PMKID lộ qua request đơn, không cần deauth | **Trung bình** | TA0006 / TA0009 | ❌ Không phát hiện (giới hạn hệ thống) |
| F-05 | MAC filtering có thể bị vượt qua bằng giả mạo | **Thấp** | TA0005 Defense Evasion | ❌ Không phát hiện (ngoài phạm vi cảm biến hiện tại) |

**Thang mức độ nghiêm trọng** (định tính, không dùng công thức CVSS tự động vì không có vector
chuẩn cho từng F-ID): **Nghiêm trọng > Cao > Trung bình > Thấp > Thông tin**, dựa trên khả năng
khai thác (độ khó) × tác động (mất dữ liệu/truy cập/gián đoạn dịch vụ).

## 4. Chi tiết từng lỗ hổng (Finding Detail)

Mẫu cho mỗi dòng ở bảng trên:

```
### F-0X — {Tiêu đề}

**Mức độ:** {Cao/Trung bình/Thấp}
**Thành phần ảnh hưởng:** {AP / Client / Giao thức}
**Mô tả:** {1–2 đoạn, kỹ thuật}
**Bằng chứng (PoC):** {lệnh đã chạy, ảnh chụp/log, không reproducible = không tính là finding}
**Tác động:** {điều gì xảy ra nếu bị khai thác thật}
**Khuyến nghị khắc phục:** {biện pháp cụ thể, tham chiếu docs/03-kich-ban/kich-ban-demo.md mục 3b}
**Trạng thái sau khắc phục:** {đã test lại / chưa test lại}
```

## 5. Số liệu định lượng (Metrics)

Điền bảng đo từ `docs/03-kich-ban/kich-ban-demo.md` mục 4 vào đây sau khi chạy đủ số lần lặp.

| Màn | Thời gian phát hiện TB (s) | Tỉ lệ phát hiện đúng | False positive |
|---|---|---|---|
| Deauth flood | | | |
| Handshake | | | |
| WPS | | | |
| PMKID | | | |

## 6. Kết luận & khuyến nghị tổng thể

_(Điền sau: tổng hợp khuyến nghị theo thứ tự ưu tiên khắc phục — thường bắt đầu từ finding mức
Cao trước)._
