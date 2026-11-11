# Ánh xạ MITRE ATT&CK

> Ánh xạ các màn tấn công trong `docs/03-kich-ban/kich-ban-demo.md` sang khung **MITRE ATT&CK**
> (Enterprise Matrix). Mục đích: trình bày kịch bản theo ngôn ngữ chuẩn mà SOC/blue team thật dùng,
> thay vì chỉ mô tả bằng tên công cụ.
>
> **Lưu ý về độ tin cậy:** các mã **Tactic** (TAxxxx) là ổn định, đã xác nhận trên
> [attack.mitre.org](https://attack.mitre.org/). Một số **Technique** (Txxxx) cho hành vi đặc thù
> Wi-Fi (như deauthentication) **chưa có ID chính thức rõ ràng** trong Enterprise Matrix tại thời
> điểm viết — các ô này ghi "chưa xác nhận" thay vì đoán ID, và nhóm nên tự tra cứu lại trên
> ATT&CK Navigator trước khi đưa vào báo cáo chính thức.

| Màn | Tactic (xác nhận) | Technique (xác nhận) | Technique Wi-Fi cụ thể |
|---|---|---|---|
| 1 — Recon | **TA0043** Reconnaissance | — | Quét SSID/BSSID/client — tương đương trinh sát hạ tầng mạng không dây, chưa có sub-technique Wi-Fi riêng trong Enterprise Matrix |
| 2 — Deauth flood | **TA0040** Impact | — | Ép ngắt kết nối bằng management frame giả mạo — **chưa xác nhận ID chính thức**, gần khái niệm Denial of Service nhưng không khớp hoàn toàn T1498 (vốn mô tả DoS tầng mạng/ứng dụng diện rộng) |
| 3 — Bắt handshake + crack | **TA0006** Credential Access | **T1110** Brute Force | Crack offline bằng wordlist/hashcat là dạng con của Brute Force (dò thử credential ngoại tuyến) |
| phụ — WPS attack | **TA0006** Credential Access | **T1110** Brute Force | Dò PIN 8 số của WPS — cùng họ kỹ thuật brute-force với Màn 3, khác bề mặt tấn công |
| 4 — PMKID | **TA0006** Credential Access, **TA0009** Collection | **T1110**; liên quan **T1040** Network Sniffing | Thu thập PMKID qua một request duy nhất rồi crack ngoại tuyến — kết hợp thu thập thụ động và brute force |
| MAC spoofing | **TA0005** Defense Evasion | — | Giả mạo địa chỉ MAC để vượt qua MAC filtering — khái niệm gần với giả mạo định danh, **chưa gán ID cụ thể** ở đây để tránh gán sai |
| Rogue AP / Evil Twin (nếu triển khai) | **TA0006** Credential Access | **T1557** Adversary-in-the-Middle | AP giả cùng SSID để đánh lừa client — khớp mô tả chính thức của T1557 |

## Cách dùng bảng này trong báo cáo

- Dùng cột **Tactic** làm tiêu đề mục khi viết Chương 3 (Triển khai tấn công) — đúng cấu trúc một
  báo cáo threat intel/pentest thật.
- Với các ô "chưa xác nhận": **không trích dẫn như sự thật đã kiểm chứng**. Ghi trong báo cáo là
  "tương đồng về mặt khái niệm với [Tactic], song ATT&CK Enterprise hiện chưa có sub-technique
  chuyên biệt cho tấn công deauthentication 802.11" — đây là một nhận định học thuật hợp lệ, không
  phải điểm yếu của kịch bản.
- Tham khảo thêm khung chuyên biệt Wi-Fi: **NIST SP 800-153** (Guidelines for Securing WLANs),
  dùng để bổ sung phần không được ATT&CK Enterprise phủ tới.
