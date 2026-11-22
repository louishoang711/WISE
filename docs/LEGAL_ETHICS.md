# Pháp lý & Đạo đức

> Tài liệu này ràng buộc **mọi kỹ thuật tấn công** trình bày trong repo này, bất kể giấy phép MIT
> của phần mã nguồn (`code/`) cho phép những gì.

## Phạm vi được phép

Toàn bộ nội dung kiểm thử xâm nhập trong dự án (Deauthentication, bắt 4-Way Handshake, crack mật khẩu WPA2, tấn công WPS, MAC Spoofing, quét mạng LAN bằng `nmap` và truy cập luồng IP Camera mô phỏng) **chỉ được thực hiện khi cả 3 điều kiện sau đều đúng**:

1. **Thiết bị thuộc sở hữu của chính nhóm** — Router AP (TL-WR940N), iPhone đóng vai IP Camera (chỉ quay tờ giấy mã cảnh `DEMO-01`/`DEMO-02`), và các laptop đều do nhóm tự trang bị.
2. **Mạng lab cách ly** — không kết nối ra Internet thật trong lúc tấn công, không chạm vào Wi-Fi hoặc camera của người khác (hàng xóm, quán cà phê, công ty, trường học) dù vô tình nằm trong tầm phủ sóng.
3. **Mục đích học thuật** — phục vụ môn **An Toàn Mạng Không Dây và Di Động (WISE432380)**, dưới sự hướng dẫn của giảng viên.

## Nghiêm cấm

- Tấn công bất kỳ mạng Wi-Fi hoặc quét/truy cập bất kỳ thiết bị camera/IoT nào **không thuộc quyền sở hữu hoặc không có ủy quyền bằng văn bản**.
- Dùng tài liệu/script trong repo này cho mục đích **thương mại trái phép, phá hoại, nghe lén, quay lén hoặc xâm nhập trái phép** vào hệ thống của bên thứ ba.
- Chia sẻ mật khẩu, dữ liệu cá nhân hoặc thông tin mạng xung quanh vô tình thu được ra ngoài phạm vi nhóm/giảng viên.

## Cơ sở pháp lý (Việt Nam)

Truy cập trái phép vào hệ thống mạng, cản trở hoạt động của mạng máy tính hoặc thu thập trái phép thông tin của người khác có thể cấu thành hành vi vi phạm theo:
- **Bộ luật Hình sự 2015** (sửa đổi, bổ sung 2017) — các điều về tội phạm trong lĩnh vực công nghệ thông tin, mạng viễn thông (Điều 288, 289, 290...).
- **Luật An ninh mạng 2018.**
- **Luật An toàn thông tin mạng 2015.**

Nhóm không tư vấn pháp lý chuyên sâu — đây là ghi chú để nhắc nhở phạm vi an toàn học thuật, không thay thế ý kiến luật sư.

## Trách nhiệm

Nhóm thực hiện (Huy, Hưng, Khang) và giấy phép MIT đi kèm **không chịu trách nhiệm** cho bất kỳ hành vi sử dụng sai mục đích nào của bên thứ ba khi lấy mã nguồn/kịch bản từ repo này.

## Báo cáo vấn đề bảo mật

Nếu phát hiện lỗ hổng trong chính các script của repo (ví dụ decoder Wazuh bị lỗi phân tích hoặc script cảm biến có lỗi bảo mật), vui lòng xem quy trình tại [`SECURITY.md`](../SECURITY.md).
