# Kịch bản đồ án: Từ Wi-Fi yếu đến lộ Camera nội bộ & Giám sát WIDS bằng Wazuh

> **Môn học:** An Toàn Mạng Không Dây và Di Động (WISE432380)  
> **Đề tài:** Nghiên cứu tấn công mạng không dây bằng công cụ AirHunt và xây dựng hệ thống giám sát – phát hiện xâm nhập (WIDS) trên thiết bị thực bằng Wazuh.  
> **Nhóm thực hiện (3 thành viên):** **Huy** (A — Red Team / Attacker) · **Hưng** (B — Wireless Sensor) · **Khang** (C — Blue Team / Wazuh & Hạ tầng).  
> **Checklist thực thi từng bước:** xem thư mục [`docs/03-kich-ban/phase/`](phase/README.md).

---

## 1. Bối cảnh thực tế & Câu chuyện Demo

Mô phỏng **Quán cà phê An** (hoặc văn phòng nhỏ) sử dụng một router Wi-Fi duy nhất (**TP-Link TL-WR940N**) phục vụ chung cho cả khách uống cà phê và **camera quan sát nội bộ** đặt tại quầy (mô phỏng bằng **iPhone chạy ứng dụng IP Camera nội bộ** phát luồng video HTTP không yêu cầu xác thực).

Một kẻ tấn công (**Huy**) ngồi trong phạm vi phủ sóng dùng laptop chạy **AirHunt** tấn công mạng Wi-Fi này để lấy mật khẩu, sau đó kết nối vào mạng nội bộ, dùng **Nmap** dò tìm địa chỉ IP/cổng dịch vụ và mở xem trực tiếp hình ảnh camera của quán.

Ở chiều ngược lại, chủ quán đã triển khai một **cảm biến giám sát không dây (WIDS — Hưng)** âm thầm lắng nghe ở chế độ Monitor Mode và đẩy log qua dây LAN về máy chủ **Wazuh SIEM (Khang)**.

### Chuỗi 3 điều kiện rủi ro cần chứng minh
1. **Lớp vô tuyến (Wi-Fi):** Không có 802.11w (PMF) + mật khẩu WPA2-PSK yếu tạo cơ hội cho kẻ tấn công bắn Deauth ép kết nối lại, thu 4-way handshake và crack ra mật khẩu để vào mạng.
2. **Lớp kiến trúc mạng (LAN):** Dùng chung một mạng phẳng cho khách và thiết bị nội bộ (không tách Guest Network / VLAN) cho phép kẻ có mật khẩu Wi-Fi quét và chạm tới IP của camera.
3. **Lớp dịch vụ ứng dụng:** Dịch vụ xem camera thiếu kiểm soát truy cập (không bật xác thực) làm lộ hình ảnh trực tiếp ngay khi bị tìm ra URL.

> [!IMPORTANT]
> **Nhận định khoa học xuyên suốt:**
> - Bắt được *handshake* không đồng nghĩa với việc đã phá được WPA2 (phụ thuộc hoàn toàn vào độ mạnh mật khẩu).
> - Biết mật khẩu Wi-Fi không đồng nghĩa với việc tự động "chiếm quyền điều khiển iPhone", mà là mở được đường mạng đi tới dịch vụ camera đang mở cổng thiếu xác thực.
> - Một cảnh báo *Deauth flood* trên Wazuh là tín hiệu cảnh báo sớm ở tầng liên kết dữ liệu (L2), không tự động đồng nghĩa "đã lộ hình ảnh camera" (vốn diễn ra ở tầng mạng/ứng dụng L3–L7).

---

## 2. Sơ đồ kiến trúc & Phân bổ thiết bị thực tế

* Sơ đồ kiến trúc lab chi tiết: [`assets/so-do/chuyen-nghiep/01-kien-truc-lab.svg`](../../assets/so-do/chuyen-nghiep/01-kien-truc-lab.svg)
* Sơ đồ pipeline giám sát Wazuh: [`assets/so-do/chuyen-nghiep/02-pipeline-giam-sat.svg`](../../assets/so-do/chuyen-nghiep/02-pipeline-giam-sat.svg)
* Bản đồ bề mặt tấn công & khả năng phát hiện: [`assets/so-do/ban-do-tan-cong.svg`](../../assets/so-do/ban-do-tan-cong.svg)

```
  [A: Huy — Attacker]  ))) sóng Deauth / bắt Handshake )))     ((( sóng Wi-Fi (((  [AP: TL-WR940N v6]
   Kali/Linux + AirHunt + Nmap                                                      SSID: Lab-Cafe-Wifi / WISE-Cafe-Staff
   Card Wi-Fi: monitor + injection                                                  + [Client: iPhone IP Camera]
         \                                                                                 |
          \___ )))  [B: Hưng — Sensor] nghe lén cả 2 bên qua monitor mode  ((( ____________| (4 cổng LAN tích hợp)
                     tshark -> sensor-wids.py -> Wazuh Agent                               |
                                      |                                                    |
                                      +------------ (cáp LAN trực tiếp) -------------------+
                                                                                           |
                                                                           (cáp LAN + USB-to-Ethernet)
                                                                                           |
                                                                           [C: Khang — Wazuh Manager]
                                                                            Wazuh 4.9.2 + Decoder/Rule + Dashboard
```

### Danh sách thiết bị & thông số đã kiểm chứng thực tế (Phiên 16/11/2026)

| Thành phần | Thiết bị thực tế | Thông số / Trạng thái đã test | Vai trò trong Lab |
|---|---|---|---|
| **A – Attacker (Huy)** | Laptop `hungs` (`wlp1s0`) | `Injection is working!` (100%), có sẵn AirHunt, Aircrack-ng, Reaver, Nmap | Thực hiện Recon, Deauth, bắt Handshake, Crack, quét Nmap & mở Camera |
| **B – Sensor (Hưng)** | Laptop MSI Katana (`wlo1`) | Monitor mode hoạt động tốt (chỉ cần nghe thụ động), nối cáp LAN vào Router | Chạy `tshark` + `code/sensor/sensor-wids.py` + Wazuh Agent (`002 hungs`) |
| **C – Blue Team (Khang)** | Laptop thứ 3 (`enxec1ac3125c1b`) | Wazuh 4.9.2 (Manager + Indexer + Dashboard) ổn định, nối LAN qua USB-to-Ethernet | Giám sát cảnh báo thời gian thực, phân tích log, cấu hình AP & phòng thủ |
| **AP mục tiêu** | Router **TP-Link TL-WR940N v6** | BSSID thực: `AC:15:A2:80:26:99` · Kênh cố định (6 hoặc 7) · IP quản trị `192.168.0.1` | Phát Wi-Fi WPA2-PSK; 4 cổng LAN tích hợp đóng vai trò switch nối B và C |
| **Client & Camera** | **iPhone** (iOS 18.4+ / iOS 12+) | Chạy app **SimpleIPCamera** (hoặc **ipCam**), chỉ quay tờ giấy mã cảnh `DEMO-01`/`DEMO-02` | Vừa là nạn nhân bị Deauth/bắt Handshake, vừa là máy chủ IP Camera nội bộ |
| **AP phụ (Phase 4)** | Hotspot điện thoại đời mới / `hostapd` | Hỗ trợ chuẩn **WPA3-SAE / 802.11w (PMF)** | Dùng riêng ở Màn 5 để kiểm chứng chống Deauth flood bằng chữ ký frame quản lý |

> [!NOTE]
> **Ghi chú hạ tầng thực tế:**
> 1. **Không cần Switch rời:** 4 cổng LAN phía sau router TL-WR940N là đủ để nối trực tiếp máy Hưng (`192.168.0.100`) và máy Khang (`192.168.0.102`).
> 2. **Lưu ý chia máy A/B:** Card Wi-Fi trên máy `hungs` hỗ trợ packet injection (`Injection is working!`), trong khi card Intel trên máy `Katana` chỉ hỗ trợ monitor mode thụ động. Do đó máy `hungs` luôn đảm nhận vai **Attacker**, máy `Katana` đảm nhận vai **Sensor**.
> 3. **Phạm vi đạo đức & pháp lý:** Chỉ thực hiện trên router, iPhone và laptop của nhóm; camera chỉ quay tờ giấy `DEMO-01` / `DEMO-02`, tuyệt đối không quay người thật và không đụng tới BSSID ngoài phạm vi (xem [`docs/ROE.md`](../ROE.md) và [`docs/LEGAL_ETHICS.md`](../LEGAL_ETHICS.md)).

---

## 3. Mạch kịch bản Demo 6 màn (Từ xâm nhập Wi-Fi → Lộ Camera → Giám sát → Phòng thủ)

**Nguyên tắc vàng:** **Hưng (B) và Khang (C) luôn bật ghi log & mở Dashboard TRƯỚC khi Huy (A) gõ lệnh tấn công.** Ở mỗi màn, Huy ghi lại mốc thời gian bắt đầu/kết thúc để đối chiếu chính xác với thời điểm nổ cảnh báo trên Wazuh.

### Màn 0 — Thiết lập Baseline & Khởi chạy Camera nội bộ
- **Khang:**
  - Cấu hình router TL-WR940N: SSID `Lab-Cafe-Wifi` (hoặc `WISE-Cafe-Staff`), kênh cố định (ví dụ kênh 7 hoặc 6, độ rộng 20 MHz), bảo mật **WPA2-PSK (AES)**, mật khẩu yếu phục vụ thực nghiệm (ví dụ `12345678` trong `rockyou.txt` hoặc `CafeDemo2026` trong `demo-wordlist.txt`).
  - Kết nối iPhone vào Wi-Fi trên, mở ứng dụng **SimpleIPCamera** (cấp quyền Camera & Local Network), bấm **Start Server**, đặt tờ giấy mã cảnh **`DEMO-01`** trước ống kính.
  - Mở thử URL hiển thị trên màn hình iPhone (dạng `http://192.168.0.101:<PORT>`) từ trình duyệt máy Khang để xác nhận xem được luồng video trực tiếp không cần mật khẩu.
- **Hưng & Khang:** Hưng bật `sensor-wids.py`, Khang xác nhận Wazuh Dashboard ở trạng thái **"sạch" (0 cảnh báo)** khi mạng hoạt động bình thường.

### Màn 1 — Trinh sát vô tuyến (Wireless Reconnaissance)
- **Huy:** Chạy `sudo airmon-ng check kill` rồi mở **AirHunt** (hoặc `airodump-ng`) bật Monitor Mode, quét liệt kê các mạng xung quanh để xác định đúng mục tiêu của nhóm:
  - Thu thập: `SSID`, `BSSID` (`AC:15:A2:80:26:99`), `Channel` cố định, chuẩn mã hóa `WPA2-CCMP/PSK`, và địa chỉ MAC của `STATION` đang kết nối (chính là iPhone Camera).
- **Kỳ vọng tại Wazuh (Khang):** **Không có cảnh báo.** Trinh sát vô tuyến hoàn toàn thụ động (chỉ thu, không phát frame nào ra không khí) → ghi nhận là **giới hạn tự nhiên đầu tiên** của mọi hệ thống WIDS.

### Màn 2 — Tấn công Deauth Flood (DoS) & Phát hiện tức thì trên Wazuh (*Màn chủ lực WIDS*)
- **Huy:**
  - Mở cửa sổ thu gói khóa đúng kênh và BSSID của AP để chờ bắt handshake.
  - Dùng chức năng Deauth trong **AirHunt** (`aireplay-ng --deauth 20 -a <AP_BSSID> -c <CLIENT_MAC> <iface_mon>`) bắn một loạt frame Deauthentication giả mạo BSSID của AP nhắm thẳng vào iPhone.
- **Hiện tượng phía nạn nhân:** iPhone bị rớt kết nối Wi-Fi tạm thời (luồng video camera trên máy Khang bị đứng hình), sau đó iPhone tự động kết nối lại vào AP.
- **Kết quả tại Wazuh (Hưng & Khang):**
  - `sensor-wids.py` trên máy Hưng bắt tức thì chuỗi frame `0x0c` (deauth) / `0x0a` (disassoc) và ghi vào `/var/log/wifi-wids.log`.
  - Wazuh Agent đẩy log về Manager → Decoder `wifi-wids` bóc tách `bssid`, `client` → **Rule `100110` (level 4)** kích hoạt cho từng gói lẻ và ngay khi đạt ngưỡng **≥ 5 gói / 10 giây** vào cùng một client, **Rule `100111` (level 12 — `"WIDS: TAN CONG Deauth flood"`) nổ cảnh báo mức cao** trên Dashboard trong vài giây!
  - Khang đo **thời gian phát hiện (Detection Latency)** = `T_alert - T_attack`.

### Màn 3 — Bắt 4-Way Handshake & Kiểm chứng Crack mật khẩu WPA2
- **Huy:**
  - Ngay khi iPhone tự kết nối lại sau đợt Deauth ở Màn 2, công cụ thu gói xác nhận đã bắt được **`WPA handshake: AC:15:A2:80:26:99`** (lưu ra file `.cap`).
  - Dùng chức năng Crack Handshake bằng Wordlist trong **AirHunt** (`aircrack-ng -w <wordlist> -b <AP_BSSID> <file.cap>`):
    - **Lượt 1 (Mật khẩu yếu):** Dùng `rockyou.txt` (hoặc `demo-wordlist.txt` có chứa mật khẩu lab) → **Crack thành công (`KEY FOUND!`)** chỉ trong vài giây.
    - **Lượt 2 (So sánh với mật khẩu mạnh ở Màn 5):** Cũng bắt được handshake y hệt nhưng chạy cạn wordlist vẫn **thất bại (`Passphrase not in dictionary`)**.
- **Kỳ vọng tại Wazuh (Khang):** WIDS chỉ phát hiện hành vi **Deauth ép rớt mạng** để lấy handshake, hoàn toàn **không phát hiện được quá trình crack offline** diễn ra cục bộ trên máy của Huy.

### Màn 4 — Hậu quả sau khi lộ Wi-Fi: Quét LAN (`Nmap`) & Xem trộm Camera nội bộ
- **Huy:**
  1. Tắt Monitor Mode trong AirHunt, chuyển card Wi-Fi về chế độ **Managed Mode** và kết nối trực tiếp vào Wi-Fi quán cà phê bằng mật khẩu vừa crack được ở Màn 3 (ngắt mọi dây LAN phụ nếu có để đảm bảo đi thuần qua đường Wi-Fi).
  2. Kiểm tra subnet nhận được qua DHCP:
     ```bash
     ip -4 addr
     ip -4 route
     ```
  3. Dùng **Nmap** quét khám phá các thiết bị đang hoạt động trong mạng LAN của quán (`192.168.0.0/24`):
     ```bash
     sudo nmap -sn 192.168.0.0/24
     ```
  4. Loại trừ IP của Router (`192.168.0.1`) và IP máy mình, Huy quét cổng dịch vụ trên IP ứng viên của iPhone (ví dụ `192.168.0.101`):
     ```bash
     nmap -sV --version-light -p 80,443,554,8000,8080,8081,8888 192.168.0.101
     # Nếu ứng dụng dùng cổng ngẫu nhiên khác, quét toàn bộ cổng TCP đang mở:
     nmap -sT -p- --open 192.168.0.101
     ```
  5. Khi phát hiện cổng HTTP của dịch vụ camera, Huy mở trình duyệt truy cập `http://192.168.0.101:<PORT>` → **xem trực tiếp hình ảnh camera của quán mà không bị hỏi mật khẩu!**
  6. **Kiểm chứng thời gian thực:** Khang đổi tờ giấy trước ống kính iPhone từ **`DEMO-01`** sang **`DEMO-02`** → màn hình trình duyệt của Huy lập tức hiển thị **`DEMO-02`** (chứng minh luồng hình trực tiếp, không phải ảnh chụp cũ).
- **Kỳ vọng tại Wazuh (Hưng & Khang):**
  - Cảm biến `sensor-wids.py` **không sinh cảnh báo** ở màn này vì khi Huy đã có mật khẩu WPA2 hợp lệ, toàn bộ gói tin Nmap và HTTP đi trong khung dữ liệu (Data Frame) đã mã hóa ở tầng 2 và diễn ra ở tầng mạng/ứng dụng (L3–L7).
  - **Ý nghĩa học thuật:** Chỉ ra rõ ranh giới giữa **WIDS vô tuyến (L2)** và **NIDS nội bộ (L3–L7)**, đồng thời chứng minh vì sao cảnh báo Deauth ở Màn 2 phải được xử lý ngay trước khi kẻ tấn công kịp leo thang vào LAN.

### Màn phụ — Tấn công WPS (Tùy chọn / Làm trước bước tắt WPS)
- **Huy:** Quét các AP bật WPS bằng `sudo wash -i <iface_mon>` (kiểm tra cột `WPS Locked = No`), sau đó chạy `reaver` (hoặc chức năng WPS trong AirHunt):
  ```bash
  sudo reaver -i <iface_mon> -b <AP_BSSID> -c <channel> -vv
  ```
- **Ghi chú phạm vi giám sát:** `local_rules.xml` đã thiết kế sẵn **Rule `100120`** cho `type=wps`, nhưng cảm biến `sensor-wids.py` mặc định chỉ lọc frame deauth/disassoc (`0x0c`/`0x0a`). Do đó màn WPS được dùng làm **tấn công minh họa để kiểm chứng trước/sau khi tắt WPS**, hoặc nâng cao bằng cách mở rộng sensor đếm burst gói Authentication/Association.

### Màn 5 — Phòng thủ đa lớp & Kiểm chứng thực nghiệm (*Màn chốt hạ*)
Nhóm lần lượt đóng từng lỗ hổng trong chuỗi tấn công và **chạy lại đúng thao tác tấn công** để chứng minh các biện pháp phòng thủ phát huy tác dụng:

| Lớp phòng thủ | Thao tác cấu hình (Khang) | Kiểm chứng tấn công lại (Huy) | Kết quả thực nghiệm trên Lab |
|---|---|---|---|
| **1. Mật khẩu WPA2 mạnh** *(Password Policy)* | Đổi mật khẩu Wi-Fi chính sang chuỗi dài, ngẫu nhiên (hoa/thường/số/ký tự đặc biệt, không nằm trong từ điển) | Bắt lại handshake mới vào `lab/strong/` và chạy lại `aircrack-ng` với cùng wordlist | ✅ **Crack thất bại** — bảo vệ lớp truy cập Wi-Fi |
| **2. Tách mạng khách & Cách ly LAN** *(Guest Network Isolation)* | Trên TL-WR940N v6, bật **Guest Network (`WISE-Cafe-Guest`)**, tắt tùy chọn *"Allow Guest To Access My Local Network"*. Giữ iPhone Camera ở mạng chính; chỉ cấp mạng khách cho Huy | Huy kết nối vào `WISE-Cafe-Guest`, mở lại URL camera `http://192.168.0.101:<PORT>` (cửa sổ ẩn danh). Cùng lúc Khang mở URL từ mạng quản trị | ✅ **Huy bị chặn hoàn toàn** (không kết nối được tới IP camera), trong khi **Khang vẫn xem được hình trực tiếp** |
| **3. Tắt WPS & Không phụ thuộc lọc MAC** | Tắt WPS trong trang quản trị Router; chứng minh lọc MAC dễ bị vượt qua bằng MAC spoofing | Huy chạy lại `wash` / `reaver` | ✅ **Tấn công WPS thất bại ngay lập tức** |
| **4. Bật 802.11w (PMF) / WPA3** *(Chống Deauth tận gốc)* | Dựng AP phụ hỗ trợ **WPA3 / 802.11w (PMF)** (dùng hotspot điện thoại đời mới hoặc `hostapd` với `ieee80211w=2` do firmware gốc TL-WR940N không có 802.11w) | Huy bắn lại lệnh Deauth flood vào client đang nối AP phụ WPA3/PMF | ✅ **Client KHÔNG rớt mạng** — các frame quản lý giả mạo không có chữ ký hợp lệ bị từ chối |
| **5. Bảo vệ dịch vụ Camera** | Khuyến nghị bật tài khoản/mật khẩu riêng cho camera, đổi port mặc định, tắt truy cập từ xa khi không cần | Kiểm tra truy cập HTTP khi có lớp xác thực ứng dụng | ✅ Chặn lộ hình ảnh ngay cả khi cùng mạng LAN |

---

## 4. Các phát hiện kỹ thuật & Giới hạn hệ thống (Điểm nhấn nghiên cứu)

Thay vì giấu nhẹm các hạn chế, báo cáo phân tích sâu **4 phát hiện kỹ thuật thực tế** rút ra từ quá trình dựng lab (phiên 14–16/11/2026):

1. **Giới hạn định danh kẻ tấn công của chuẩn 802.11:**
   - Hệ thống WIDS phát hiện chính xác **đang có tấn công Deauth flood** nhắm vào AP và Client nào, nhưng **không thể xác định địa chỉ MAC thật của kẻ tấn công**.
   - *Nguyên nhân:* Trong chuẩn IEEE 802.11 cổ điển (trước 802.11w), các Management Frame (Deauthentication `0x0c`, Disassociation `0x0a`) không có trường chữ ký mật mã. Công cụ tấn công luôn ghi đè địa chỉ nguồn (`wlan.sa`) bằng chính BSSID của AP (`ac:15:a2:80:26:99`). Do đó, giải pháp đúng đắn trong thực tế là bật **802.11w (PMF)** để vô hiệu hóa gói giả mạo, chứ không phải dựa vào MAC nguồn trong gói deauth để "truy vết" hay chặn MAC.
2. **Ranh giới hiển thị của cảm biến WIDS tầng 2 (`sensor-wids.py`):**
   - Cảm biến hiện tại chỉ bắt frame `0x0c` (deauth) và `0x0a` (disassoc) và gán nhãn chung `type=deauth`, `channel=0`.
   - Do đó, WIDS **bắt cực nhạy** ở Màn 2 (Deauth flood) và gián tiếp bắt được Màn 3 (ép kết nối lại lấy Handshake), nhưng **mù** ở Màn 1 (Recon thụ động), bước Crack Offline (Màn 3), và Màn 4 (quét Nmap / xem HTTP Camera ở tầng 3–7 sau khi đã vào mạng hợp lệ).
3. **Nhiễu vô tuyến từ các mạng hàng xóm & Bài toán lọc tại nguồn:**
   - Trong phiên test thực tế đầu tiên (16/11/2026), Wazuh ghi nhận tới **23,387+ sự kiện** và **5,000 cảnh báo mức 12 (Rule 100111)**, nhưng trong đó lẫn cả các frame deauth/disassoc tự nhiên của những Wi-Fi xung quanh (`AMR_WIFI`, `UBND`, `Mandan`...).
   - *Khắc phục:* Cần lọc theo đúng BSSID của lab (`data.bssid: "ac:15:a2:80:26:99"` — lưu ý `tshark` xuất địa chỉ MAC ở dạng **chữ thường**) ngay tại `sensor-wids.py` hoặc trên bộ lọc truy vấn của Wazuh Dashboard để đảm bảo số liệu đo không bị nhiễu.
4. **Phát hiện lỗi thực tế trong mã nguồn công cụ AirHunt (Chuẩn đầu ra G4.2):**
   - Qua kiểm tra mã nguồn [Debajyoti0-0/AirHunt](https://github.com/Debajyoti0-0/AirHunt), nhóm xác nhận công cụ này chỉ là wrapper gọi `aircrack-ng`, `reaver`, `bully`, `wifite` và **không hề hỗ trợ tấn công PMKID** (chỉ nhắc tên `hcxtools` ở tài liệu tham khảo).
   - Đặc biệt, hàm `start_monitor_mode()` trong code của AirHunt chỉ gọi `airmon-ng start <iface>` mà **thiếu bước `airmon-ng check kill`**, dẫn tới việc `NetworkManager` / `wpa_supplicant` trên Ubuntu/Kali liên tục giành lại card mạng làm `aireplay-ng` bị treo ở `"Waiting for beacon frame"`. Nhóm đã khắc phục bằng cách chạy tay `sudo airmon-ng check kill` trước khi khởi chạy AirHunt.

---

## 5. Bảng số liệu đo lường thực nghiệm (Dùng cho Phase 5 & Chương 4)

Chạy lặp lại các màn tấn công (khuyến nghị ~10 lần cho màn Deauth) và tổng hợp vào bảng định lượng:

| Màn / Kỹ thuật | Thời gian phát hiện TB (s) | Tỉ lệ phát hiện đúng (%) | Cảnh báo sai (False Positive) | Rule Wazuh kích hoạt | Mức độ Alert |
|---|---|---|---|---|---|
| **Màn 0 — Baseline** | — | — | Kỳ vọng = `0` (sau khi lọc BSSID) | Không | — |
| **Màn 1 — Recon (Thụ động)** | Không phát hiện | `0%` (Giới hạn tự nhiên) | `0` | Không | — |
| **Màn 2 — Deauth Flood** | `___ giây` | `___ %` (Đã test nổ 100%) | `0` | `100110` → **`100111`** | **Level 12 (Cao)** |
| **Màn 3 — Handshake + Crack** | `___ giây` (bắt ở pha Deauth) | Phát hiện pha ép rớt mạng | `0` | `100110` / `100111` | Level 4 / 12 |
| **Màn 4 — Nmap & Camera HTTP** | Không phát hiện bởi WIDS L2 | `0%` (Ngoài phạm vi L2) | `0` | Không (Cần NIDS L3–L7) | — |
| **Màn phụ — WPS Attack** | Tùy chọn | Tùy chọn (Rule `100120`) | — | `100120` (nếu mở rộng sensor) | Level 10 |

---

## 6. Kịch bản phân vai thuyết trình trên lớp (15–18 phút) & Phiếu ghi kết quả

### Lời dẫn và phối hợp theo từng mốc thời gian
* **Phút 00–03 (Màn 0 — Khang & Hưng):**
  * **Khang** giới thiệu bối cảnh Quán cà phê An dùng chung Wi-Fi cho khách và camera nội bộ; chiếu trực tiếp luồng video từ iPhone Camera đang quay tờ giấy **`DEMO-01`**.
  * **Hưng** xác nhận cảm biến `sensor-wids.py` và Wazuh Agent (`002 hungs`) đang hoạt động; **Khang** chiếu Wazuh Dashboard đang sạch cảnh báo.
* **Phút 03–07 (Màn 1, 2, 3 — Huy, Hưng & Khang):**
  * **Huy** dùng AirHunt quét mục tiêu (Màn 1), bật thu gói rồi bắn **Deauth flood** (Màn 2) vào iPhone.
  * **Khang** chỉ lên màn hình: luồng camera bị gián đoạn và ngay lập tức **Wazuh Dashboard nổ cảnh báo mức 12 (Rule 100111 — Deauth flood)**!
  * Khi iPhone tự kết nối lại, **Huy** thu được 4-way handshake và chạy wordlist dò ra mật khẩu Wi-Fi yếu (Màn 3).
* **Phút 07–10 (Màn 4 — Huy & Khang):**
  * **Huy** chuyển card Wi-Fi về Managed Mode, kết nối vào mạng Wi-Fi quán, dùng `nmap` quét dải LAN tìm ra IP và cổng HTTP của iPhone Camera, mở trình duyệt xem hình trực tiếp.
  * **Khang** đổi tờ giấy trước camera từ **`DEMO-01`** sang **`DEMO-02`** để hội đồng thấy hình ảnh trên máy kẻ tấn công cập nhật theo thời gian thực.
* **Phút 10–13 (Phân tích giám sát — Hưng & Khang):**
  * **Hưng** chiếu file `/var/log/wifi-wids.log` thực tế, giải thích cơ chế `tshark` lọc frame `0x0c`/`0x0a`.
  * **Khang** phân tích vì sao WIDS bắt cực nhạy ở Màn 2 nhưng không định danh được MAC thật của Huy và không thấy được lưu lượng HTTP Camera ở Màn 4 (dẫn dắt sang nhu cầu phòng thủ đa lớp).
* **Phút 13–18 (Màn 5 — Kiểm chứng phòng thủ — Cả nhóm):**
  * **Khang** đổi mật khẩu Wi-Fi chính sang mật khẩu mạnh (Huy crack lại → thất bại) và bật mạng khách **`WISE-Cafe-Guest`** có tắt quyền truy cập LAN (*Guest Isolation*).
  * **Huy** kết nối vào mạng khách, mở lại URL camera → **bị chặn hoàn toàn**, trong khi **Khang** mở trên máy quản trị vẫn xem được camera bình thường.
  * Nhóm trình bày thêm kết quả kiểm chứng tắt WPS và chống Deauth bằng **802.11w (PMF)** trên AP phụ, tổng kết bảng số liệu.

### Phiếu điền nhanh tại buổi Demo
```text
Ngày & giờ bắt đầu: ______________   BSSID Lab: AC:15:A2:80:26:99   Kênh cố định: ____
SSID chính: ______________________   SSID mạng khách: ________________________________
URL Camera iPhone: _______________   Phiên bản iOS & App: ____________________________
Wazuh Agent (Hưng): 002 hungs        IP Wazuh Manager (Khang): 192.168.0.102

[Màn 2] Giờ bắn Deauth: __________   Giờ nổ Alert 100111: _________ -> Độ trễ: _____ s
[Màn 3] Lượt mật khẩu yếu — File capture: ____________   Kết quả & thời gian crack: ____
[Màn 4] Quét Nmap thấy IP/Port: ______________________   Thấy mã cảnh DEMO-02: Có / Không
[Màn 5] Lượt mật khẩu mạnh — Kết quả với cùng wordlist: ______________________________
[Màn 5] Từ mạng khách mở URL Camera: Có / Không   (Máy quản trị mở đồng thời: Có / Không)
```

---

## 7. Bản đồ phủ Chuẩn đầu ra môn học (WISE432380) & Cấu trúc Báo cáo 5 chương

### Đối chiếu Chuẩn đầu ra
| Nội dung thực hiện trong đồ án | Chuẩn đầu ra | Chương giáo trình Earle [1] | Bài Lab đề cương |
|---|---|---|---|
| Lý thuyết frame quản lý 802.11, cơ chế Deauth, 4-way Handshake | **G1.2** | Chương 5 | — |
| Cấu hình AP (TL-WR940N) & thiết bị đầu cuối (iPhone Client/Camera) | **G1.2** | Chương 10, 11 | — |
| Khảo sát, thực nghiệm & phát hiện lỗi trong mã nguồn công cụ **AirHunt** | **G4.2** | **Chương 16** | Lab 1 |
| Thực thi chuỗi tấn công thực tế (Recon, Deauth, Handshake, Nmap Camera, WPS) | **G2.1** | **Chương 13** | Lab 6 |
| Xây dựng cảm biến `tshark` & giám sát phát hiện xâm nhập trên **Wazuh** | **G2.1** | — | **Lab 3, Lab 4** |
| Xây dựng chính sách an ninh WLAN (Password Policy, Guest Isolation) | **G2.2** | **Chương 14** | Lab 5 |
| Thiết kế kiến trúc phòng thủ đa lớp (WPA3, 802.11w PMF, Tắt WPS, Phân đoạn LAN) | **G4.1** | **Chương 15** | — |
| Phối hợp nhóm 3 vai (Red / Sensor / Blue), viết báo cáo & bảo vệ trực tiếp | **G3.1, G3.2** | — | — |

### Cấu trúc Báo cáo cuối kỳ (5 Chương — đặt tại `docs/05-bao-cao/`)
1. **Chương 1 — Tổng quan an toàn mạng không dây:** Kiến trúc IEEE 802.11, đặc tả Management Frame, cơ chế xác thực WPA2/WPA3 và tổng quan hệ thống WIDS.
2. **Chương 2 — Phân tích & Đánh giá công cụ AirHunt:** Kiến trúc, tính năng, phát hiện lỗi thiếu `airmon-ng check kill` trong mã nguồn, so sánh thực nghiệm với `aircrack-ng`, `wifite2`, `airgeddon`.
3. **Chương 3 — Triển khai kịch bản tấn công thực nghiệm:** Thiết lập lab, thực thi Màn 1 → Màn 4 (từ phá khóa Wi-Fi đến quét Nmap làm lộ hình ảnh IP Camera iPhone) và ánh xạ theo khung MITRE ATT&CK.
4. **Chương 4 — Hệ thống giám sát & Phát hiện xâm nhập (Wazuh WIDS):** Thiết kế `sensor-wids.py`, `local_decoder.xml`, `local_rules.xml`, xử lý bài toán lọc nhiễu BSSID và phân tích bảng số liệu đo lường.
5. **Chương 5 — Phòng thủ đa lớp & Kiểm chứng thực nghiệm:** Kiểm chứng trước/sau khi vá (Mật khẩu mạnh, Tách mạng khách Guest Network Isolation, Tắt WPS, 802.11w PMF), đề xuất chính sách an ninh WLAN hoàn chỉnh.

### Tài liệu tham khảo chính
1. Aaron E. Earle, *Wireless Security Handbook*, Auerbach Publications, 2006.
2. W. Osterhage, *Wireless Network Security: A Beginner's Guide, 2nd Edition*, CRC Press, 2018.
3. Debajyoti0-0, *AirHunt — Wireless Penetration Testing Toolkit*, [github.com/Debajyoti0-0/AirHunt](https://github.com/Debajyoti0-0/AirHunt).
4. Tài liệu chính thức: [Wazuh Documentation (Ruleset & Logtest)](https://documentation.wazuh.com/current/user-manual/ruleset/testing.html), [Aircrack-ng Suite](https://www.aircrack-ng.org/), [Nmap Network Scanning](https://nmap.org/book/), [TP-Link TL-WR940N v6 User Guide (Guest Network)](https://www.tp-link.com/us/user-guides/TL-WR940N_V6/chapter-4-configure-the-router-as-a-standard-wireless-router).
