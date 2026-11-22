# Phase 05 — Đo lường & Phân tích định lượng (Khang chủ trì)

> **Phụ thuộc:** Phase 03 + Phase 04 phải hoàn tất.  
> **Mục tiêu:** Biến log thực tế thành số liệu nghiên cứu định lượng (thời gian phát hiện trung bình, tỉ lệ phát hiện đúng, tỉ lệ cảnh báo sai / false positive và phân tích vùng mù của WIDS).  
> **Tham chiếu:** [`docs/03-kich-ban/kich-ban-demo.md`](../kich-ban-demo.md) (Mục 5), [`docs/04-ket-qua/nhat-ky-phien-16-11-2026.md`](../../04-ket-qua/nhat-ky-phien-16-11-2026.md) (Mục 5).

## Checklist tuần tự

- [ ] **Bước 1 (Huy):** Chạy lặp lại màn tấn công Deauth (đúng chế độ "one client" nhắm vào MAC của iPhone) **~10 lần**, mỗi lần cách nhau ít nhất 30–60 giây. Ghi lại chính xác mốc thời gian (`HH:MM:SS`) lúc bấm lệnh của từng lần.  
      → **Báo OK** kèm danh sách mốc thời gian 10 lần bắn Deauth (cùng mốc giờ của Màn 1 Recon và Màn 4 Nmap/Camera).

- [ ] **Bước 2 (Khang):** Trong Wazuh Dashboard (Security Events), áp bộ lọc chuẩn theo đúng BSSID của lab (**chú ý: MAC lưu dạng chữ thường** `data.bssid: "ac:15:a2:80:26:99"`) và `rule.id: (100110 OR 100111)`.  
      → **Báo OK** khi bộ lọc chỉ trả về sự kiện của router nhóm, không lẫn nhiễu hàng xóm.

- [ ] **Bước 3 (Khang):** Với từng lần tấn công trong 10 lần:
      - Kéo chọn zoom vào đúng khung giờ trên biểu đồ histogram.
      - Sắp xếp cột `timestamp` tăng dần, tìm bản ghi **Rule `100111` (Level 12) đầu tiên** của đợt đó.
      - Lấy `T_alert_100111 - T_attack_Huy` → ra **Thời gian phát hiện (Detection Latency)** của lần thử đó.  
      → **Báo OK** kèm bảng thời gian phát hiện của 10 lần thử và giá trị trung bình (giây).

- [ ] **Bước 4 (Khang):** Đếm tổng số sự kiện `100110` (level 4) và `100111` (level 12) sinh ra trong mỗi đợt tấn công để đưa vào thống kê mật độ cảnh báo.  
      → **Báo OK** kèm số liệu thống kê.

- [ ] **Bước 5 (Khang):** Lọc **ngoài** các khung giờ tấn công (khi mạng chạy Baseline ở Màn 0 hoặc khi Huy chỉ đang quét Nmap/xem Camera ở Màn 4, cùng điều kiện BSSID `ac:15:a2:80:26:99`) → đếm số lần nổ nhầm Rule `100111` (**False Positive**, kỳ vọng = `0`).  
      → **Báo OK** kèm số liệu False Positive.

- [ ] **Bước 6 (Khang):** Điền hoàn chỉnh bảng số liệu vào [`docs/04-ket-qua/BAO-CAO-FINDINGS.md`](../../04-ket-qua/BAO-CAO-FINDINGS.md) (Mục 5) và rút ra nhận xét khoa học:
      - WIDS tầng 2 phát hiện **100%** các đợt Deauth flood (và hành vi ép rớt mạng để bắt Handshake) với độ trễ chỉ vài giây.
      - WIDS tầng 2 **không phát hiện** Recon thụ động (Màn 1), Crack Offline (Màn 3), và Quét LAN Nmap / Xem HTTP Camera sau khi đã vào mạng hợp lệ (Màn 4) → chứng minh tính tất yếu của kiến trúc phòng thủ đa lớp (Mật khẩu mạnh + Tách mạng khách Guest Network Isolation + 802.11w PMF).  
      → **Báo OK** khi bảng số liệu và biểu đồ hoàn chỉnh.

## Verify (Điều kiện qua Phase 05)

- [ ] Bảng số liệu định lượng hoàn chỉnh (có trung bình 10 lần đo, tỉ lệ phát hiện, false positive) kèm phân tích rõ điểm mạnh và vùng mù của WIDS.

## Ship

Cập nhật số liệu vào [`README.md`](../../../README.md), [`docs/04-ket-qua/BAO-CAO-FINDINGS.md`](../../04-ket-qua/BAO-CAO-FINDINGS.md) và Chương 4 của báo cáo.
