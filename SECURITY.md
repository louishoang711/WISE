# Security Policy

## Phạm vi chính sách này

Áp dụng cho **mã nguồn** trong `code/` (decoder Wazuh, rule Wazuh, script cảm biến
`sensor-wids.py`). Không áp dụng cho các kỹ thuật tấn công Wi-Fi mô tả trong `docs/` — những kỹ
thuật đó không phải lỗ hổng của repo, mà là đối tượng nghiên cứu; xem `docs/LEGAL_ETHICS.md` cho
phạm vi sử dụng hợp lệ.

## Báo cáo lỗ hổng trong mã nguồn

Nếu phát hiện vấn đề trong chính các script/cấu hình của repo (ví dụ: decoder có thể bị injection
qua input không được kiểm tra, rule logic có lỗ hổng bypass, script cảm biến chạy với quyền thừa
kế không cần thiết):

1. **Không mở Issue công khai** nếu lỗ hổng có thể bị lợi dụng trước khi vá.
2. Liên hệ trực tiếp maintainer qua GitHub: [@louishoang711](https://github.com/louishoang711).
3. Mô tả: file bị ảnh hưởng, bước tái hiện, mức độ ảnh hưởng ước tính.

## Thời gian phản hồi dự kiến

Đây là repo học thuật duy trì bởi 1 nhóm sinh viên, không phải sản phẩm thương mại — phản hồi
trong khoảng **3–7 ngày**, không có cam kết SLA chính thức.

## Phiên bản được hỗ trợ

| Thành phần | Trạng thái |
|---|---|
| `code/wazuh/local_decoder.xml`, `local_rules.xml` | Đang duy trì |
| `code/sensor/sensor-wids.py` | Đang duy trì |

Không có phiên bản release chính thức (semver) — repo theo dõi theo nhánh `main` và các branch
tính năng, xem `CONTRIBUTING.md`.
