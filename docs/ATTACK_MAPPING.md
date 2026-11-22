# Ánh xạ MITRE ATT&CK

> Ánh xạ chuỗi tấn công trong [`docs/03-kich-ban/kich-ban-demo.md`](03-kich-ban/kich-ban-demo.md) sang khung **MITRE ATT&CK**
> (Enterprise Matrix). Mục đích: trình bày kịch bản theo ngôn ngữ chuẩn mà SOC / Blue Team thực tế sử dụng,
> thay vì chỉ mô tả bằng tên công cụ.
>
> **Lưu ý về độ tin cậy:** các mã **Tactic** (`TAxxxx`) và các **Technique** tầng mạng (`T1110`, `T1046`, `T1557`...) đã được xác nhận trên
> [attack.mitre.org](https://attack.mitre.org/). Riêng hành vi đặc thù lớp quản lý 802.11 (như Deauthentication) hiện **chưa có Technique ID riêng** trong Enterprise Matrix — ô này được ghi rõ thay vì gán ID tùy tiện.

| Màn / Kỹ thuật | Tactic (Xác nhận) | Technique (Xác nhận) | Mô tả kỹ thuật trong kịch bản Lab |
|---|---|---|---|
| **Màn 1 — Recon** | **TA0043** Reconnaissance | — | Quét thụ động `SSID` / `BSSID` / `Channel` / `CLIENT_MAC` bằng AirHunt (`airodump-ng`) — tương đương trinh sát hạ tầng không dây, chưa có sub-technique 802.11 riêng trong Enterprise Matrix |
| **Màn 2 — Deauth Flood** | **TA0040** Impact | — | Ép ngắt kết nối client (iPhone) bằng Management Frame `0x0c` giả mạo BSSID của AP — tương đồng khái niệm Denial of Service ở tầng liên kết dữ liệu (L2), gần với **T1498** (Network DoS) nhưng diễn ra ở lớp MAC 802.11 |
| **Màn 3 — Bắt Handshake & Crack** | **TA0006** Credential Access | **T1110** Brute Force (`T1110.002` Password Cracking) | Thu 4-Way Handshake khi client kết nối lại sau Deauth, sau đó dò mật khẩu WPA2-PSK ngoại tuyến bằng wordlist (`aircrack-ng`) |
| **Màn 4 — Quét LAN & Xem trộm Camera IP** | **TA0007** Discovery, **TA0009** Collection | **T1046** Network Service Discovery | Sau khi vào mạng Wi-Fi bằng mật khẩu vừa crack, dùng `nmap` quét host và cổng TCP (`T1046`) để tìm dịch vụ HTTP của iPhone IP Camera thiếu xác thực và xem trực tiếp luồng hình ảnh nội bộ (`DEMO-01`/`DEMO-02`) |
| **Màn phụ — WPS Attack** | **TA0006** Credential Access | **T1110** Brute Force | Dò mã PIN 8 chữ số của WPS (`wash` + `reaver`) — cùng họ kỹ thuật Brute Force với Màn 3 nhưng khai thác bề mặt giao thức WPS |
| **MAC Spoofing** | **TA0005** Defense Evasion | — | Giả mạo địa chỉ MAC của client hợp lệ để vượt qua bộ lọc MAC Filtering trên AP |
| **Rogue AP / Evil Twin** *(Rule 100130 dự phòng)* | **TA0006** Credential Access | **T1557** Adversary-in-the-Middle | Phát AP giả trùng SSID để đánh lừa client kết nối vào |

## Cách dùng bảng này trong báo cáo

- Dùng cột **Tactic & Technique** làm tiêu đề phụ khi viết **Chương 3 (Triển khai tấn công)** và bảng tổng hợp trong [`docs/04-ket-qua/BAO-CAO-FINDINGS.md`](04-ket-qua/BAO-CAO-FINDINGS.md) — đúng chuẩn báo cáo Pentest / Threat Intelligence.
- Chỉ ra rõ sự chuyển dịch qua các tầng mạng trong chuỗi tấn công:
  - **Màn 1 → Màn 3** diễn ra ở **tầng Vật lý / Liên kết dữ liệu (L1–L2, IEEE 802.11)** → thuộc phạm vi giám sát trực tiếp của cảm biến WIDS (`sensor-wids.py`).
  - **Màn 4 (`T1046` Network Service Discovery & HTTP Camera)** diễn ra ở **tầng Mạng / Ứng dụng (L3–L7)** sau khi kẻ tấn công đã có khóa WPA2 hợp lệ → nằm ngoài tầm nhìn của WIDS tầng 2, giải thích vì sao cần kết hợp **cảnh báo sớm Deauth trên Wazuh** với **tách mạng khách (Guest Network Isolation)** và **xác thực ứng dụng**.
- Tham khảo bổ sung tiêu chuẩn chuyên biệt cho mạng không dây: **NIST SP 800-153** (*Guidelines for Securing Wireless Local Area Networks*).
