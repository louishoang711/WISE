# Kịch bản đồ án: Tấn công & Giám sát an toàn mạng không dây

> Môn: An Toàn Mạng Không Dây và Di Động (WISE432380)
> Đề tài: Nghiên cứu tấn công mạng không dây bằng công cụ AirHunt và xây dựng hệ thống
> giám sát – phát hiện xâm nhập (WIDS) trên thiết bị thực bằng Wazuh.
> Nhóm 3 người: A (Red team), B (Sensor), C (Blue team).

---

## 1. Bối cảnh thực tế (để kể trong báo cáo & khi bảo vệ)

Mô phỏng một **quán café / văn phòng nhỏ** có một Wi-Fi cho khách (AP = router TL-WR940N).
Một kẻ tấn công ngồi trong quán (hoặc ngoài bãi xe) dùng laptop tấn công Wi-Fi này. Chủ quán
đã lắp một **cảm biến giám sát không dây (WIDS)** âm thầm theo dõi, nối về một máy chủ Wazuh
đặt trong quầy. Mục tiêu đồ án: chứng minh hệ thống giám sát **phát hiện được** cuộc tấn công
gần như tức thì, đo được hiệu quả, và chỉ ra cách vá để lần sau tấn công thất bại.

Đây là tình huống **có thật** ở mọi nơi có Wi-Fi công cộng — đó là tính thực tiễn của đề tài.

---

## 2. Sơ đồ & thành phần

Sơ đồ kiến trúc tổng thể: xem `so-do/kien-truc-tong-the.svg`.
Bản đồ các kiểu tấn công & khả năng phát hiện: xem `so-do/ban-do-tan-cong.svg`.

```
   [A: Attacker]  ))) sóng tấn công )))        ((( sóng bình thường (((  [AP: TL-WR940N]
    Kali + AirHunt                                                        + [Client: điện thoại cũ]
    card wifi monitor+inject                                                     |
          \                                                                      | (LAN)
           \____ )))  B nghe lén cả 2 bên qua monitor mode  ((( ______________   |
                                         |                                       |
                                  [B: Sensor - Kismet]----(cáp)----[Switch]----(cáp)----[C: Wazuh]
```

| Thành phần | Là gì | Yêu cầu |
|---|---|---|
| A – Attacker | Người | Laptop Kali/Ubuntu, card Wi-Fi **monitor + injection** (đã test `aireplay-ng --test`) |
| B – Sensor | Người | Máy riêng, card Wi-Fi **monitor** (chỉ cần nghe), nối dây vào switch |
| C – Blue team | Người | Máy chạy Wazuh manager (máy ảo được), nối dây vào switch, **không cần Wi-Fi** |
| AP | Thiết bị | Router TL-WR940N, cấu hình WPA2-PSK, bật/tắt WPS để test |
| Client | Thiết bị | 1 điện thoại/laptop cũ, kết nối sẵn vào AP, đóng vai "nạn nhân thật" |
| Switch | Thiết bị | Nối Sensor + AP(LAN) + Wazuh thành mạng lab cách ly |

> **Lưu ý đạo đức & pháp lý:** toàn bộ thực hiện trên thiết bị của chính nhóm, trong mạng lab
> cách ly, không đụng tới Wi-Fi của người khác. Ghi rõ điều này ở đầu báo cáo.

### 2b. Danh sách thiết bị & phân bổ máy (đã kiểm tra thực tế)

| Thiết bị | Trạng thái | Kết quả test | Vai |
|---|---|---|---|
| Laptop "hungs" (`wlp1s0`) | Có sẵn | `Injection is working!`, Found 8 APs, 100% | **A — Attacker** |
| Laptop MSI Katana (`wlo1`) | Có sẵn | monitor mode OK (inject không cần cho vai này) | **B — Sensor** |
| Laptop thứ 3 | Có sẵn | không cần Wi-Fi | **C — Wazuh** |
| Router TL-WR940N | Có sẵn | cấu hình qua web 192.168.0.1 | AP nạn nhân |
| Điện thoại cũ | Có sẵn | kết nối vào AP | Client nạn nhân |
| Switch | Có sẵn | nối mạng lab | hạ tầng |
| **Dây mạng (Ethernet) × 3** | **CẦN MUA** | nối B, AP-LAN, C vào switch | hạ tầng |
| AP phụ WPA3/PMF | Tùy chọn | dùng hotspot điện thoại mới hoặc hostapd | demo vá 802.11w |

→ Card Wi-Fi: **không cần mua thêm** — máy A đã inject được, máy B chỉ cần monitor (có sẵn).
Món duy nhất cần mua là **dây mạng**.

---

## 3. Mạch demo 5 màn (escalation: từ ồn ào → tinh vi → vá lỗi)

Nguyên tắc vàng: **B và C phải bật ghi trước khi A tấn công** (như camera phải quay trước khi
diễn). Mỗi màn A ghi lại mốc thời gian bắt đầu/kết thúc để sau đối chiếu với cảnh báo của C.

### Màn 0 — Baseline (trạng thái bình thường)
- Client dùng mạng bình thường (lướt web). B ghi log nền, C xác nhận dashboard "sạch", không
  cảnh báo. Mục đích: có mốc so sánh để chứng minh cảnh báo sau là do tấn công, không phải nhiễu.

### Màn 1 — Trinh sát (Reconnaissance)
- A quét liệt kê AP, client, kênh, chuẩn mã hóa (không gửi gì, chỉ nghe).
- Kỳ vọng phát hiện: thấp — đây là giai đoạn khó bắt, ghi nhận như một **giới hạn** của WIDS.

### Màn 2 — Deauth flood (DoS) — *màn chủ lực*
- A gửi một đợt deauth giả mạo AP nhắm vào client → client rớt mạng.
- Kỳ vọng: C **nổ cảnh báo mức cao** "Deauthentication flood" trong vài giây. Đo **thời gian
  phát hiện** (từ lúc A bấm tấn công tới lúc alert hiện).

### Màn 3 — Bắt handshake & so sánh mật khẩu yếu/mạnh
- Deauth khiến client tự kết nối lại → A bắt được 4-way handshake.
- **Lưu ý thuật ngữ:** handshake LUÔN bắt được dù mật khẩu mạnh hay yếu. Cái khác nhau là
  *crack được hay không*, không phải *bắt được hay không*.
- Chạy cùng quy trình, chỉ đổi mật khẩu trên AP:

  | Lần | Mật khẩu AP | Bắt handshake | Crack | Thời gian |
  |---|---|---|---|---|
  | 1 | Yếu (có trong wordlist, vd lấy từ rockyou.txt) | ✓ | ✓ ra mật khẩu | giây–phút |
  | 2 | Mạnh (dài, hoa/thường/số/ký tự đặc biệt, không phải từ có nghĩa) | ✓ | ✗ thất bại | chạy hết wordlist vẫn không ra |

- Thông điệp: tấn công bắt handshake **không ngăn được** (là cơ chế WPA2); độ an toàn cuối cùng
  phụ thuộc hoàn toàn vào **độ mạnh mật khẩu**. Đây là bằng chứng thực nghiệm cho Password Policy.

### Màn 4 — Né tránh: PMKID (nâng cao) — *màn thể hiện chiều sâu*
- A lấy PMKID chỉ bằng một yêu cầu tới AP, **không deauth ai**.
- Kỳ vọng: C **khó/không phát hiện** (không có deauth flood để bắt). Đây là phần **"giới hạn hệ
  thống & hướng phát triển"** — rất ghi điểm vì nhóm dám chỉ ra điểm yếu của chính mình.

### Màn 5 — Vá lỗi & kiểm chứng (Mitigation) — *màn chốt hạ*
- Bật biện pháp phòng thủ, rồi **chạy lại Màn 2** để chứng minh tấn công thất bại:
  - **802.11w (PMF – Protected Management Frames):** ký xác thực frame quản lý → deauth giả bị từ chối.
  - Lưu ý phần cứng: TL-WR940N (firmware gốc) **không hỗ trợ 802.11w**. Để demo vế vá lỗi, dùng
    một trong các cách: (a) AP phụ hỗ trợ WPA3/PMF (điện thoại đời mới phát hotspot WPA3, hoặc
    router mới hơn); (b) dựng AP bằng `hostapd` trên laptop có bật `ieee80211w=2`. Nêu rõ ràng
    hạn chế này trong báo cáo thay vì giấu.
- Kết quả kỳ vọng: cùng lệnh deauth nhưng client **không rớt** nữa → vòng lặp khoa học khép kín:
  *lỗ hổng → khai thác → phát hiện → vá → kiểm chứng*.

---

## 3b. Phòng thủ — mỗi kiểu tấn công có biện pháp chống

Phần này là "vế thủ" của đồ án. Với mỗi tấn công ở mục 3, nhóm trình bày biện pháp chống và
đánh dấu cái nào **kiểm chứng được** trên thiết bị đang có (TL-WR940N đời cũ hạn chế WPA3/802.11w).

| Tấn công | Biện pháp phòng thủ | Kiểm chứng được trên lab? |
|---|---|---|
| Deauth flood | Bật **802.11w (PMF)** — ký xác thực frame quản lý, deauth giả bị từ chối | ⚠️ Cần AP phụ WPA3/PMF (hotspot điện thoại mới hoặc hostapd) — TL-WR940N không hỗ trợ |
| Bắt handshake → crack | **Mật khẩu mạnh** (đã chứng minh ở Màn 3); nâng lên **WPA3-SAE** chống crack offline | ✅ Mật khẩu mạnh test ngay trên TL-WR940N; WPA3 cần AP phụ |
| Tấn công WPS | **Tắt WPS** trên router | ✅ Test ngay: bật WPS → tấn công được; tắt WPS → tấn công thất bại |
| MAC spoofing / bypass MAC filter | Không dựa vào lọc MAC làm bảo mật chính; dùng WPA2/WPA3 + 802.1X | ✅ Chứng minh lọc MAC bị vượt dễ dàng → kết luận không nên tin |
| PMKID | Tắt tính năng roaming/PMKID caching nếu AP hỗ trợ; WPA3 | ⚠️ Tuỳ AP; nêu như hướng phát triển |
| Giám sát tổng thể | **Triển khai WIDS (Wazuh + Kismet)** — chính hệ thống của nhóm | ✅ Là sản phẩm lõi của đồ án |

Vòng lặp kiểm chứng (ghi điểm nhất): bật WPS → A tấn công WPS thành công → **tắt WPS** →
A chạy lại → thất bại. Cùng cách với mật khẩu yếu→mạnh. Đây là chứng minh *"vá rồi thì tấn công
hết tác dụng"* bằng thực nghiệm, không nói suông.

## 4. Số liệu phải đo (biến báo cáo thành "nghiên cứu")

Lập bảng cho mỗi màn tấn công:

| Màn | Thời gian phát hiện (s) | Có cảnh báo đúng? | Cảnh báo sai (false positive)? | Mức độ alert |
|---|---|---|---|---|
| 1 Recon | ? | ? | | |
| 2 Deauth | ? | ✓ (kỳ vọng) | | Cao |
| 3 Handshake | ? | | | |
| phụ WPS | ? | tùy chọn (xem ghi chú) | | — |
| 4 PMKID | ? | ✗ (kỳ vọng) | | — |

**Ghi chú về phát hiện WPS:** tấn công WPS (reaver/bully) tạo ra một loạt gói
authentication/association dồn dập tới AP. Rule Wazuh đã có sẵn ID 100120 cho `type=wps`,
**nhưng** cảm biến mặc định chỉ bắt frame deauth, chưa phát sinh sự kiện `type=wps`. Nên chọn 1
trong 2 hướng và ghi rõ trong báo cáo:
- **(Tối thiểu)** coi màn WPS là *tấn công minh họa, không đo phát hiện* — đánh dấu "không đo".
- **(Nâng cao)** mở rộng cảm biến để đếm burst gói auth/assoc tới AP rồi ghi `type=wps` → khi đó
  rule 100120 sẽ nổ và đo được như các màn khác.

- Chạy mỗi màn **nhiều lần** (vd 10 lần) để lấy trung bình, không chạy 1 lần rồi kết luận.
- Tính **tỉ lệ phát hiện** (bắt được / tổng số lần tấn công) và **false positive** (báo nhầm khi
  không tấn công — chạy Màn 0 kéo dài để đếm).

---

## 5. Phân vai chi tiết

### Người A — Red team (tấn công)
- Dựng Kali + AirHunt, card Wi-Fi đã test injection.
- Thực hiện Màn 1–4, ghi nhật ký thời điểm từng thao tác.
- Viết lý thuyết: frame quản lý, cơ chế deauth, 4-way handshake, PMKID (giáo trình Earle Ch5, Ch13).
- Đánh giá công cụ AirHunt: chức năng, so sánh aircrack-ng / wifite2 / airgeddon (Earle Ch16).

### Người B — Sensor (giám sát không dây)
- Đặt card ở monitor mode, vị trí nghe được cả A và AP.
- **Thiết kế cảm biến đã chốt:** dùng `tshark` lọc frame deauth/disassoc, ghi log định dạng cố
  định cho Wazuh — đây là cách đã hiện thực trong `sensor/sensor-wids.py`. Kismet là phương án
  thay thế (đọc alert qua REST API rồi ghi cùng định dạng) nếu muốn WIDS đầy đủ hơn.
- Cấu hình Wazuh agent (`<localfile>`) đọc file log, gửi về manager.
- Thu thập & bàn giao log mẫu cho C. (khớp Lab 4: Wireless Security Monitoring)

### Người C — Blue team (phát hiện & chính sách)
- Dựng Wazuh manager + dashboard.
- Viết `local_decoder.xml` (regex tách field) + `local_rules.xml` (đếm ngưỡng deauth, ID ≥ 100000).
- (Nâng cao) active response: webhook cảnh báo / tự chặn MAC.
- Đo số liệu phát hiện, lập bảng ở mục 4.
- Viết **chính sách an ninh WLAN** (Earle Ch14): password policy, access policy, physical security;
  và kiến trúc phòng thủ (Earle Ch15): WPA3, tắt WPS, 802.11w.

---

## 6. Phủ chuẩn đầu ra môn học

| Phần đồ án | Chuẩn đầu ra | Chương Earle | Lab đề cương |
|---|---|---|---|
| Lý thuyết frame quản lý, deauth | G1.2 | Ch5 | — |
| Router (AP) + client (end device) | G1.2 | Ch10, Ch11 | — |
| Đánh giá AirHunt | **G4.2** | **Ch16** | Lab 1 |
| Thực hiện tấn công | **G2.1** | **Ch13** | Lab 6 |
| Giám sát Wazuh | G2.1 | — | **Lab 3, Lab 4** |
| Chính sách an ninh | **G2.2** | **Ch14** | Lab 5 |
| Kiến trúc phòng thủ | G4.1 | Ch15 | — |
| Làm nhóm, báo cáo | G3.1, G3.2 | — | — |

→ Phủ **G1.2, G2.1, G2.2, G3.x, G4.1, G4.2** — đủ cho bài thi cuối kỳ (KT#5) và điểm lab (KT#4).

---

## 7. Cấu trúc báo cáo cuối (5 chương)

1. **Tổng quan** — an toàn WLAN, 802.11, frame quản lý, các lỗ hổng.
2. **Công cụ AirHunt** — kiến trúc, chức năng, so sánh công cụ cùng loại.
3. **Triển khai tấn công** — lab thật, Màn 1–4, kết quả.
4. **Hệ thống giám sát Wazuh** — pipeline, decoder/rule, bảng số liệu phát hiện.
5. **Phòng thủ & kiểm chứng** — Màn 5 vá lỗi, chính sách an ninh WLAN, kiến trúc đề xuất.

Tài liệu tham khảo: [1] Aaron E. Earle, *Wireless Security Handbook*, Auerbach, 2006;
[2] W. Osterhage, *Wireless Network Security, 2nd ed.*, CRC Press, 2018; tài liệu Wazuh & Kismet.
