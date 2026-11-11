# ROADMAP đồ án (cấu trúc GSD) — chia phase & phân công A/B/C

> Áp theo tinh thần GSD: mỗi phase đi qua vòng lặp **Discuss → Plan → Execute → Verify → Ship**.
> Các phase có thể chạy song song khi không phụ thuộc nhau (gọi là "wave").
> Vai: **A** = Attacker (máy hungs), **B** = Sensor (máy Katana), **C** = Blue team/Wazuh (máy 3).

---

## Bản đồ phụ thuộc giữa các phase

```
Phase 0 (Hạ tầng) ──┬──> Phase 2 (Pipeline giám sát: B+C) ──┐
                    │                                        ├──> Phase 3 (Tấn công: A) ──> Phase 4 (Phòng thủ) ──> Phase 5 (Đo lường) ──> Phase 6 (Báo cáo)
                    └──> Phase 1 (Lý thuyết: song song) ─────┘
```

Wave song song:
- **Wave 1:** Phase 0 (cả nhóm dựng hạ tầng) + Phase 1 (viết lý thuyết — làm nền lúc rảnh).
- **Wave 2:** Phase 2 (B+C dựng pipeline) — A hỗ trợ tạo traffic test.
- **Wave 3:** Phase 3 → 4 → 5 → 6 (tuần tự, vì mỗi cái cần kết quả cái trước).

---

## PHASE 0 — Hạ tầng & môi trường (cả nhóm) — *nền móng, làm trước tiên*

**Goal:** Có một mạng lab cách ly chạy được, 3 máy sẵn sàng đúng vai.

**Thứ tự cấu hình (làm đúng thứ tự này):**
1. **Mua & đấu nối phần cứng:** 3 dây mạng. Nối B, cổng LAN router, C vào switch. Cắm điện router.
2. **Cấu hình AP (người phụ trách AP, có thể là C):**
   - Vào `192.168.0.1`, đặt SSID `Lab-Cafe-Wifi`.
   - Bảo mật **WPA2-PSK**, đặt **mật khẩu yếu** (có trong rockyou.txt) cho giai đoạn đầu.
   - **Cố định kênh** (vd 6), tắt Auto. Ghi lại số kênh.
   - Bật WPS (để sau demo), ghi lại BSSID (MAC) của router.
3. **Client:** điện thoại cũ kết nối vào `Lab-Cafe-Wifi`, để nguyên trạng thái online.
4. **Máy A:** cài Kali/Ubuntu + AirHunt + aircrack-ng suite. Test injection:
   `sudo airmon-ng start wlan0 6` → `sudo aireplay-ng --test wlan0mon` → phải thấy `Injection is working!`
5. **Máy B:** cài Ubuntu + Kismet. Bật monitor mode đúng kênh 6, xác nhận thấy traffic.
6. **Máy C:** cài Wazuh manager (máy ảo được). Đặt IP tĩnh cùng dải với switch.

**Verify (điều kiện qua phase):**
- [ ] Client lướt web bình thường qua AP.
- [ ] 3 máy nối switch ping được nhau.
- [ ] Máy A: `Injection is working!`.
- [ ] Máy B: Kismet thấy được AP + client trên kênh 6.
- [ ] Máy C: mở được dashboard Wazuh.

**Ship:** commit cấu hình + ảnh chụp trạng thái vào repo (branch riêng).

---

## PHASE 1 — Lý thuyết nền & tài liệu (song song, mỗi người tự viết)

**Goal:** Hoàn thành các mục lý thuyết của báo cáo, không phụ thuộc thiết bị.

- **A viết:** frame quản lý 802.11, cơ chế deauth, 4-way handshake, PMKID (Earle Ch5, Ch13);
  **đánh giá công cụ AirHunt** (Earle Ch16 → chuẩn đầu ra **G4.2**).
- **B viết:** monitor mode vs managed mode, khái niệm WIDS, giới thiệu tshark/Kismet.
- **C viết:** WEP/WPA/WPA2/WPA3, 802.1X, chính sách an ninh (Earle Ch12, Ch14; Osterhage mục 3.7);
  **kiến trúc phòng thủ** (Earle Ch15 → chuẩn đầu ra **G4.1**).

**Verify:** mỗi mục có trích dẫn nguồn đúng chuẩn.
**Ship:** gom vào Chương 1–2 của báo cáo.

---

## PHASE 2 — Pipeline giám sát (B + C) — *phải xong TRƯỚC khi tấn công*

**Goal:** Log từ cảm biến chảy tới dashboard Wazuh và sinh được cảnh báo.

**Thứ tự cấu hình:**
1. **B:** chạy cảm biến `sensor/sensor-wids.py` (tshark lọc frame deauth/disassoc) ghi ra
   `/var/log/wifi-wids.log` theo định dạng cố định. (Kismet là phương án thay thế nếu muốn WIDS đầy đủ.)
2. **B:** kiểm tra log sinh đúng định dạng khi có deauth thử.
3. **B:** cài Wazuh agent, cấu hình `<localfile>` trỏ vào file log, đăng ký agent với manager của C.
4. **C:** viết `local_decoder.xml` (regex tách bssid, client_mac, attack_type, count).
5. **C:** viết `local_rules.xml` (ID ≥ 100000, đếm ngưỡng deauth trong X giây → alert mức cao).
6. **C:** restart Wazuh manager, tạo view trên dashboard.

**Verify:** A gửi thử một đợt deauth ngắn → trong vài giây dashboard C hiện alert.
**Ship:** commit decoder/rule/script vào repo.

---

## PHASE 3 — Thực hiện tấn công (A chủ trì, B+C ghi nhận) — *cần Phase 0 + 2*

**Goal:** Chạy đủ các màn tấn công, thu log & mốc thời gian.

**Nguyên tắc:** B+C bật ghi TRƯỚC, rồi A mới tấn công. A ghi nhật ký thời điểm từng thao tác.

- **Màn 0:** baseline (không tấn công) — C xác nhận dashboard sạch.
- **Màn 1:** recon (quét) — ghi nhận WIDS khó bắt.
- **Màn 2:** deauth flood — C đo thời gian phát hiện.
- **Màn 3:** bắt handshake → crack với mật khẩu yếu (ra) rồi đổi AP sang mật khẩu mạnh (không ra).
- **Màn phụ:** WPS attack (khi WPS đang bật).
- **Màn 4:** PMKID — ghi nhận WIDS khó bắt (giới hạn hệ thống).

**Verify:** mỗi màn có log của B, cảnh báo (hoặc không) của C, khớp mốc thời gian của A.
**Ship:** bảng kết quả thô cho Phase 5.

---

## PHASE 4 — Phòng thủ & kiểm chứng (cả nhóm) — *cần Phase 3*

**Goal:** Chứng minh "vá rồi thì tấn công hết tác dụng".

- **Tắt WPS** trên AP → A chạy lại WPS attack → thất bại.
- **Mật khẩu mạnh** (đã làm ở Màn 3) → crack thất bại.
- **(Nâng cao) 802.11w/WPA3** trên AP phụ (hotspot điện thoại mới / hostapd) → A deauth → client KHÔNG rớt.

**Verify:** mỗi biện pháp có 2 ảnh/clip: trước khi vá (tấn công được) và sau khi vá (thất bại).
**Ship:** số liệu so sánh trước/sau cho Chương 5.

---

## PHASE 5 — Đo lường & phân tích (C chủ trì) — *cần Phase 3 + 4*

**Goal:** Biến log thành số liệu nghiên cứu.

- Chạy mỗi màn tấn công nhiều lần (vd 10 lần), tính **thời gian phát hiện trung bình**.
- Tính **tỉ lệ phát hiện** và **false positive** (chạy baseline kéo dài).
- Lập bảng + biểu đồ cho từng kiểu tấn công.

**Verify:** bảng số liệu đầy đủ, có nhận xét WIDS mạnh/yếu ở đâu.
**Ship:** Chương 4 (kết quả giám sát).

---

## PHASE 6 — Báo cáo & slide (cả nhóm) — *ship cuối*

**Goal:** Ghép tất cả thành báo cáo + slide bảo vệ.

- Ghép Chương 1–5 (xem cấu trúc trong `kich-ban-do-an.md` mục 7).
- Chèn 2 sơ đồ (`so-do/*.svg`).
- Chuẩn bị slide theo mạch: bối cảnh → kiến trúc → tấn công → giám sát → phòng thủ → kết luận.
- Tập thuyết trình (G3.2).

**Verify:** báo cáo phủ đủ G1.2, G2.1, G2.2, G3.x, G4.1, G4.2.
**Ship:** nộp + bảo vệ.

---

## Ai giữ vai chính ở phase nào (tóm tắt)

| Phase | A (Attacker) | B (Sensor) | C (Blue team) |
|---|---|---|---|
| 0 Hạ tầng | cài Kali, test inject | cài Kismet | cài Wazuh, cấu hình AP |
| 1 Lý thuyết | frame/deauth | monitor/WIDS | WPA/chính sách |
| 2 Pipeline | hỗ trợ test | Kismet + script + agent | decoder + rule + dashboard |
| 3 Tấn công | **chủ trì** | ghi log | đo cảnh báo |
| 4 Phòng thủ | chạy lại tấn công | ghi log | cấu hình vá |
| 5 Đo lường | cấp dữ liệu | cấp log | **chủ trì phân tích** |
| 6 Báo cáo | phần tấn công | phần giám sát | phần phòng thủ + tổng hợp |

> Ghi chú GSD: khi mở phiên Claude Code trong Ubuntu (đã cài gsd-core), có thể dùng
> `/gsd-plan-phase` cho từng phase ở trên để sinh plan chi tiết hơn, `/gsd-execute-phase` để
> thực thi. File này đóng vai ROADMAP mà GSD tham chiếu.
