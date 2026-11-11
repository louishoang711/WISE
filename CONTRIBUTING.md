# Đóng góp (CONTRIBUTING)

Repo này phục vụ đồ án môn **WISE432380**, đóng góp chủ yếu từ 3 thành viên nhóm. Hướng dẫn dưới
đây giữ lịch sử commit sạch và tránh phá vỡ cấu hình của người khác.

## Quy tắc git

1. **Không bao giờ push trực tiếp lên `main`.** Luôn tạo branch riêng:
   ```bash
   git checkout -b <loai>/<mo-ta-ngan>
   # ví dụ: feat/wps-detection, fix/decoder-regex, docs/chuong-1
   ```
2. Sau khi clone, chạy một lần để bật hook chặn push `main`:
   ```bash
   sh setup.sh
   ```
3. Push branch rồi tạo Pull Request vào `main`, xin review từ 1 thành viên khác trước khi merge.

## Commit message

- Viết ngắn gọn, mô tả **việc đã làm**, không mô tả quá trình.
- Tiền tố gợi ý: `docs:`, `feat:`, `fix:`, `chore:`.
- Không thêm dòng attribution của công cụ AI vào commit message hay PR.

## Khi sửa file kỹ thuật (`code/wazuh/`, `code/sensor/`)

- Test lại bằng `wazuh-logtest` (xem `code/wazuh/README.md`) trước khi commit rule/decoder mới.
- Nếu đổi định dạng log cảm biến, cập nhật đồng thời cả `local_decoder.xml` và
  `code/sensor/sensor-wids.py` — hai file này phải khớp nhau.

## Khi thêm kịch bản tấn công mới

- Mọi kỹ thuật mới phải tuân thủ `docs/LEGAL_ETHICS.md` (chỉ trên thiết bị của nhóm, lab cách ly).
- Ghi rõ lệnh **đã kiểm chứng chạy được** trên phiên bản công cụ đang dùng; nếu chưa test, ghi chú
  "chưa kiểm chứng — đối chiếu tài liệu chính thức" thay vì đoán cú pháp.

## Báo lỗi / đề xuất

Mở Issue hoặc nhắn trực tiếp trong nhóm. Với vấn đề liên quan bảo mật của chính script trong repo,
xem mục "Báo cáo vấn đề bảo mật" trong `docs/LEGAL_ETHICS.md`.
