# Phase 04 — Phòng thủ đa lớp & Kiểm chứng thực nghiệm (Cả nhóm)

> **Phụ thuộc:** Phase 03 phải hoàn tất (đã có đầy đủ kết quả "trước khi vá" để đối chiếu).  
> **Mục tiêu:** Chứng minh bằng thực nghiệm **"vá đúng chỗ thì tấn công thất bại"** trên cả 4 lớp: (1) Mật khẩu WPA2 mạnh, (2) Tách mạng khách Guest Network Isolation chặn truy cập Camera, (3) Tắt WPS & kiểm chứng lọc MAC, (4) Bật 802.11w (PMF) chống Deauth flood.  
> **Tham chiếu:** [`docs/03-kich-ban/kich-ban-demo.md`](../kich-ban-demo.md) (Màn 5).

---

## Checklist tuần tự

### Lớp 1 — Chính sách mật khẩu mạnh (Chống crack Handshake)

- [ ] **Bước 1 (Khang):** Vào trang quản trị router (`192.168.0.1`), đổi mật khẩu mạng Wi-Fi chính (`Lab-Cafe-Wifi` / `WISE-Cafe-Staff`) sang một **mật khẩu mạnh** (dài ≥ 14 ký tự, gồm chữ hoa, chữ thường, chữ số, ký tự đặc biệt, hoàn toàn ngẫu nhiên). Kết nối lại iPhone vào Wi-Fi với mật khẩu mới và bật lại `SimpleIPCamera`.  
      → **Báo OK** khi iPhone đã kết nối lại với mật khẩu mạnh.

- [ ] **Bước 2 (Huy):** Bật lại Monitor Mode, bắn Deauth để bắt 4-way handshake mới lưu vào `lab/strong/capture-strong.cap`. Chạy lại `aircrack-ng` với cùng wordlist như ở Phase 03 (`rockyou.txt` / `demo-wordlist.txt`).  
      → **Báo OK** kèm ảnh chụp màn hình **`Passphrase not in dictionary` (Crack thất bại)** — chứng minh: handshake vẫn bắt được nhưng mật khẩu mạnh vô hiệu hóa hoàn toàn bước dò khóa offline.

### Lớp 2 — Phân đoạn mạng & Cách ly khách (Guest Network Isolation — Chặn truy cập Camera)

- [ ] **Bước 3 (Khang):** Trên trang quản trị router **TL-WR940N v6**:
      - Vào mục *Guest Network → Wireless Settings*, bật mạng khách với **SSID = `WISE-Cafe-Guest`** và đặt mật khẩu riêng cho khách.
      - **Quan trọng nhất:** Tắt tùy chọn **"Allow Guest To Access My Local Network"** (Cho phép khách truy cập mạng cục bộ = **Tắt/Disable**).
      - Giữ iPhone Camera kết nối ở mạng chính (`WISE-Cafe-Staff`); cung cấp mật khẩu mạng khách `WISE-Cafe-Guest` cho Huy.  
      → **Báo OK** kèm ảnh chụp cấu hình Guest Network đã tắt quyền truy cập LAN.

- [ ] **Bước 4 (Huy + Khang):**
      - **Huy** (ở chế độ Managed Mode, không cắm dây LAN) kết nối vào mạng khách **`WISE-Cafe-Guest`**, mở cửa sổ trình duyệt ẩn danh (để tránh cache cũ) và truy cập lại đúng URL camera `http://<IP_iPhone>:<PORT>` (và thử `nmap`/`ping` tới IP của iPhone).
      - **Cùng lúc đó, Khang** (đứng ở mạng quản trị/mạng chính) mở URL camera và đổi tờ giấy trước ống kính sang mã mới.  
      → **Báo OK** khi xác nhận: **máy Huy bị chặn hoàn toàn (Connection Timeout / Unreachable)**, trong khi **máy Khang vẫn xem được hình ảnh camera trực tiếp bình thường!** (Loại trừ khả năng app camera bị treo).

### Lớp 3 — Tắt WPS & Đánh giá giới hạn của MAC Filtering

- [ ] **Bước 5 (Huy + Khang — Kiểm chứng trước/sau khi tắt WPS):**
      - *(Nếu chưa chạy màn phụ WPS ở Phase 03)*: Khi WPS đang bật trên router, Huy chạy `sudo wash -i <iface_mon>` và `sudo reaver -i <iface_mon> -b AC:15:A2:80:26:99 -c <kênh> -vv` để ghi nhận trạng thái tấn công được (hoặc router kích hoạt `WPS Locked`).
      - **Khang** vào trang quản trị router **Tắt hoàn toàn WPS (Disable WPS)**.
      - **Huy** chạy lại `wash` / `reaver` → xác nhận không còn thấy WPS hoặc công cụ báo lỗi thất bại ngay lập tức.  
      → **Báo OK** kèm cặp ảnh chụp trước và sau khi tắt WPS.

- [ ] **Bước 6 (Khang + Huy — Tùy chọn: Chứng minh không nên tin cậy lọc MAC):**
      - Nếu bật MAC Filtering trên AP, Huy chỉ cần đọc MAC của client hợp lệ từ bước Recon (`airodump-ng`) rồi đổi MAC card mạng của mình (`ip link set dev <iface> address <CLIENT_MAC>` hoặc chức năng MAC Spoofing trong AirHunt) là vượt qua được ngay.  
      → **Báo OK** với kết luận đưa vào Chính sách an ninh (Chương 5): không dùng MAC Filtering làm cơ chế bảo mật chính.

### Lớp 4 — Bật chuẩn 802.11w (PMF / WPA3) chống Deauth Flood tận gốc

- [ ] **Bước 7 (Cả nhóm — Dựng AP phụ hỗ trợ 802.11w/WPA3):**
      - Vì phần cứng router TL-WR940N (firmware gốc) không hỗ trợ chuẩn 802.11w (Protected Management Frames), nhóm bật **Hotspot chuẩn WPA3-Personal (bắt buộc PMF)** trên một điện thoại đời mới (hoặc dựng `hostapd` trên laptop với cấu hình `ieee80211w=2`), rồi cho 1 thiết bị client kết nối vào.  
      → **Báo OK** khi AP phụ WPA3/PMF đã có client kết nối ổn định.

- [ ] **Bước 8 (Huy — Bắn lại Deauth vào AP đã bật 802.11w):**
      - Huy chuyển card sang đúng kênh của AP phụ và chạy lại lệnh `aireplay-ng --deauth` nhắm vào client đó.  
      → **Báo OK** kèm ảnh/clip chứng minh: **Client hoàn toàn KHÔNG bị rớt mạng** (vì các frame Deauthentication giả mạo không có chữ ký mật mã IGTK/BIP hợp lệ nên bị từ chối ngay tại tầng MAC). Đây là mảnh ghép khép kín vòng lặp: *Lỗ hổng → Khai thác → Phát hiện (Wazuh) → Vá lỗi → Kiểm chứng*.

---

## Verify (Điều kiện qua Phase 04)

- [ ] Mỗi biện pháp phòng thủ (Mật khẩu mạnh, Tách mạng khách Guest Isolation, Tắt WPS, 802.11w PMF) đều có đủ cặp bằng chứng đối chiếu: **Trước khi vá (Tấn công thành công)** vs **Sau khi vá (Tấn công thất bại)**.

## Ship

Tổng hợp bảng so sánh kết quả Trước/Sau khi vá và ảnh chụp minh chứng để đưa vào Chương 5 của báo cáo và mục 4 của [`docs/04-ket-qua/BAO-CAO-FINDINGS.md`](../../04-ket-qua/BAO-CAO-FINDINGS.md).
