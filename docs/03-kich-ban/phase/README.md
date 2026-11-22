# Chia Phase Thực Thi & Hướng Dẫn Từng Thành Viên (Checklist Tuần Tự)

> **Tài liệu gốc:** Kịch bản tổng thể nằm ở [`docs/03-kich-ban/kich-ban-demo.md`](../kich-ban-demo.md); nhật ký dựng hạ tầng nằm ở [`docs/04-ket-qua/nhat-ky-phien-16-11-2026.md`](../../04-ket-qua/nhat-ky-phien-16-11-2026.md).  
> **Phân vai:** **Huy = A (Attacker / Red Team)** · **Hưng = B (Wireless Sensor)** · **Khang = C (Blue Team / Wazuh + Hạ tầng)**.

---

## 📌 Trạng thái hiện tại: Hạ tầng & Cài đặt Wazuh ĐÃ XONG — Chạy lại kịch bản từ đầu

Toàn bộ phần **cài đặt hạ tầng (Phase 00)** và **cài đặt Wazuh Manager + Wazuh Agent cho Hưng + Decoder/Rule (Phase 02)** **đã được cài đặt và kết nối thành công**.

Vì vậy, khi nhóm **tiến hành chạy lại lab từ đầu** để thu bộ số liệu và ảnh/video minh chứng sạch:
1. **Không cần cài lại** Wazuh, Agent hay cấu hình lại từ con số 0.
2. Chỉ cần làm nhanh **5 phút bật lại hệ thống** (cắm dây LAN, bật AP + Client, Hưng chạy `sensor-wids.py` có lọc BSSID `ac:15:a2:80:26:99`, Khang mở Dashboard xác nhận Agent `002 hungs` Active).
3. Bắt đầu chạy chính thức từ đầu tại **[`phase-03-tan-cong.md`](phase-03-tan-cong.md) → [`phase-04-phong-thu.md`](phase-04-phong-thu.md) → [`phase-05-do-luong.md`](phase-05-do-luong.md)**.

---

## Danh sách 7 Phase thực thi

| File | Phase | Người chủ trì | Trạng thái hiện tại | Ghi chú khi chạy lại Lab |
|---|---|---|---|---|
| [`phase-00-ha-tang.md`](phase-00-ha-tang.md) | **Phase 00** — Hạ tầng & Thiết bị | Cả nhóm (Khang điều phối) | ✅ **Đã xong hạ tầng** | Chỉ xem mục *"⚡ Bật nhanh trước buổi chạy (3 phút)"* |
| [`phase-01-ly-thuyet.md`](phase-01-ly-thuyet.md) | **Phase 01** — Lý thuyết nền & đánh giá AirHunt | Mỗi người tự viết (song song) | ⬜ Viết độc lập | Không phụ thuộc buổi chạy lab |
| [`phase-02-pipeline-giam-sat.md`](phase-02-pipeline-giam-sat.md) | **Phase 02** — Pipeline cảm biến → Wazuh | Hưng + Khang | ✅ **Đã cài xong Agent & Rule** | Chỉ bật `sensor-wids.py` kèm BSSID `ac:15:a2:80:26:99` |
| [`phase-03-tan-cong.md`](phase-03-tan-cong.md) | **Phase 03** — Thực hiện tấn công (Chạy lại từ Màn 0) | Huy (Hưng + Khang ghi nhận) | 🎯 **BẮT ĐẦU CHẠY LẠI TỪ ĐÂY** | Chạy tuần tự Màn 0 → Màn 1 → Màn 2 → Màn 3 (→ Màn 4) |
| [`phase-04-phong-thu.md`](phase-04-phong-thu.md) | **Phase 04** — Phòng thủ & kiểm chứng | Cả nhóm | ⬜ Chờ kết quả Phase 03 | Quay cặp bằng chứng Trước vá vs Sau vá |
| [`phase-05-do-luong.md`](phase-05-do-luong.md) | **Phase 05** — Đo lường định lượng & phân tích | Khang | ⬜ Chờ kết quả Phase 03 + 04 | Đo 10 lần Deauth lấy thời gian phát hiện TB |
| [`phase-06-bao-cao.md`](phase-06-bao-cao.md) | **Phase 06** — Ghép báo cáo 5 chương & Slide | Cả nhóm | ⬜ Ship cuối | Ghép Chương 1–5 + Slide bảo vệ |

## Quy tắc phối hợp khi chạy lại Lab: "Người này báo OK thì tới người kia"

1. Làm đúng thứ tự bước trong từng file, **không nhảy cóc**.
2. Xong bước của mình → báo **"OK `<tên>` xong bước N"** (kèm mốc giờ / ảnh chụp màn hình) → người kế tiếp mới thực hiện.
3. **Nguyên tắc vàng:** Hưng (`sensor-wids.py`) và Khang (`Wazuh Dashboard`) luôn bật sẵn **TRƯỚC** khi Huy bấm bất kỳ lệnh tấn công nào.
