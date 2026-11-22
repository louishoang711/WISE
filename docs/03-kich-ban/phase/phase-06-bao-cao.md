# Phase 06 — Báo cáo 5 Chương & Slide Bảo vệ (Cả nhóm, Ship cuối)

> **Phụ thuộc:** Phase 00–05 phải hoàn tất (đã có số liệu từ Phase 05 và bằng chứng trước/sau vá từ Phase 03–04).  
> **Mục tiêu:** Ghép toàn bộ kết quả thành báo cáo hoàn chỉnh (5 chương trong `docs/05-bao-cao/`), điền `BAO-CAO-FINDINGS.md` và chuẩn bị slide bảo vệ 15–18 phút.  
> **Tham chiếu:** [`docs/03-kich-ban/kich-ban-demo.md`](../kich-ban-demo.md) (Mục 6 & Mục 7).

## Checklist tuần tự

- [ ] **Bước 1 (Huy):** Hoàn thiện **Chương 2** (Phân tích & Đánh giá công cụ AirHunt, bao gồm phát hiện lỗi thiếu `airmon-ng check kill` và giới hạn tính năng) và **Chương 3** (Triển khai kịch bản tấn công thực nghiệm: Màn 1 Recon → Màn 2 Deauth → Màn 3 Handshake/Crack → Màn 4 Quét Nmap & Lộ hình ảnh Camera iPhone `DEMO-01`/`DEMO-02`).  
      → **Báo OK** khi bản thảo Chương 2 & Chương 3 xong.

- [ ] **Bước 2 (Hưng):** Hoàn thiện phần cảm biến WIDS (`tshark` / `sensor-wids.py`, Monitor Mode vs Managed Mode) trong **Chương 1 & Chương 4**, cung cấp trích đoạn log `/var/log/wifi-wids.log` thực tế và phân tích bài toán lọc nhiễu BSSID mạng hàng xóm.  
      → **Báo OK** khi bản thảo và log mẫu xong.

- [ ] **Bước 3 (Khang):** Hoàn thiện **Chương 4** (Kiến trúc Wazuh Manager/Decoder/Rule `100100`–`100111`, bảng số liệu định lượng từ Phase 05, giới hạn định danh kẻ tấn công của frame quản lý 802.11) và **Chương 5** (Kiểm chứng phòng thủ 4 lớp từ Phase 04: Mật khẩu mạnh, Tách mạng khách Guest Network Isolation chặn truy cập Camera, Tắt WPS, 802.11w PMF + Chính sách an ninh WLAN). Điền hoàn tất [`docs/04-ket-qua/BAO-CAO-FINDINGS.md`](../../04-ket-qua/BAO-CAO-FINDINGS.md).  
      → **Báo OK** khi bản thảo Chương 4, Chương 5 và Findings Report xong.

- [ ] **Bước 4 (Cả nhóm):** Ghép 5 chương thống nhất văn phong tại [`docs/05-bao-cao/`](../../05-bao-cao/), nhúng bộ sơ đồ chuẩn từ `assets/so-do/`:
      - `assets/so-do/chuyen-nghiep/01-kien-truc-lab.svg` (hoặc `.png`)
      - `assets/so-do/chuyen-nghiep/02-pipeline-giam-sat.svg` (hoặc `.png`)
      - `assets/so-do/ban-do-tan-cong.svg`  
      → **Báo OK** khi báo cáo 5 chương hoàn chỉnh.

- [ ] **Bước 5 (Cả nhóm):** Thiết kế Slide bảo vệ bám sát kịch bản 15–18 phút ở Mục 6 của [`kich-ban-demo.md`](../kich-ban-demo.md):
      1. Bối cảnh Quán cà phê An & Chuỗi 3 rủi ro (Wi-Fi yếu → Mạng phẳng → Camera không xác thực).
      2. Kiến trúc Lab thực tế & Pipeline giám sát Wazuh WIDS.
      3. Demo / Video thực nghiệm tấn công (AirHunt Deauth → Wazuh nổ Alert Level 12 → Crack Handshake → Nmap mở Camera iPhone `DEMO-01`/`DEMO-02`).
      4. Phân tích số liệu phát hiện & 4 phát hiện kỹ thuật thực tế (giới hạn định danh 802.11, vùng mù L2 vs L3–L7, lọc nhiễu BSSID, lỗi code AirHunt).
      5. Kiểm chứng phòng thủ đa lớp (Mật khẩu mạnh, Guest Network Isolation chặn xem camera, Tắt WPS, 802.11w PMF).  
      → **Báo OK** khi Slide hoàn tất.

- [ ] **Bước 6 (Cả nhóm):** Tập khớp lời dẫn và thao tác chuyển vai giữa Huy – Hưng – Khang theo đúng phân bổ thời gian 15–18 phút (chuẩn đầu ra **G3.2**).  
      → **Báo OK** khi cả nhóm đã tập dượt trôi chảy, sẵn sàng bảo vệ.

## Verify (Điều kiện qua Phase 06)

- [ ] Báo cáo phủ đầy đủ các chuẩn đầu ra môn học: **G1.2, G2.1, G2.2, G3.1, G3.2, G4.1, G4.2** (theo bảng đối chiếu ở [`kich-ban-demo.md`](../kich-ban-demo.md) Mục 7).

## Ship

Nộp báo cáo cuối kỳ + Slide và bảo vệ trước giảng viên/hội đồng.
