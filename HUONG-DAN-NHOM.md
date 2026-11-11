# Hướng dẫn chi tiết cả nhóm — Đồ án An toàn mạng không dây

> Phân vai: **Huy = Attacker (A)** · **Hưng = Sensor (B)** · **Khang = Wazuh (C) + hạ tầng**
> Đọc kèm: `kich-ban-do-an.md` (kịch bản demo), `ROADMAP.md` (chia phase).

---

## 0. CẢNH BÁO PHẦN CỨNG — đọc trước khi chia máy

Kết quả test thực tế:
- Máy **`hungs`** (`wlp1s0`) → `Injection is working!` ✓ → **tiêm gói được** → hợp vai **Attacker**.
- Máy **`huy-Katana`** (`wlo1`) → chỉ monitor được, test injection ra `0 APs` (nhiều khả năng card
  Intel không hỗ trợ injection) → **chỉ hợp vai Sensor** (nghe).

**Vấn đề:** Huy được giao vai Attacker (cần injection), nhưng máy Katana của Huy có thể không
inject được. Cần chọn 1 trong 3 cách:

| Cách | Làm gì | Ưu / nhược |
|---|---|---|
| **1 (khuyên dùng)** | Huy test lại Katana ĐÚNG kênh AP. Nếu `Injection is working!` thì dùng luôn | Miễn phí; nhưng card Intel thường vẫn fail |
| **2** | Huy mua 1 card USB (Alfa AWUS036NHA ~150-250k) cắm vào Katana để attack | Mỗi người giữ máy mình; tốn ít tiền |
| **3** | Huy attack bằng máy `hungs` (inject ✓), Hưng làm Sensor bằng máy Katana | Không tốn tiền; nhưng 2 người đổi máy cho nhau |

> **QUYẾT ĐỊNH ĐÃ CHỐT (mặc định đề xuất):** vai Attacker **phải chạy trên máy inject được**.
> Hiện chỉ có máy `hungs` test ra `Injection is working!`. Trình tự quyết:
> 1. Huy test lại Katana ĐÚNG kênh AP. Nếu `Injection is working!` → Huy attack trên Katana. Xong.
> 2. Nếu Katana không inject → **chọn cách 3**: Huy attack trên máy `hungs`, Hưng làm Sensor trên
>    Katana (chỉ cần monitor). Zero chi phí, dùng được ngay. Đây là mặc định nếu bước 1 thất bại.
> 3. Chỉ mua card USB (cách 2) nếu bắt buộc mỗi người giữ đúng máy mình và Katana không inject.
>
> Ghi lại lựa chọn cuối vào báo cáo TRƯỚC khi bắt đầu Phase 0.

Cách test lại cho Huy (đúng kênh AP, giả sử kênh 6):
```bash
sudo airmon-ng check kill
sudo airmon-ng start wlo1 6
sudo aireplay-ng --test -a <BSSID_cua_AP> wlo1mon
```
Thấy `Injection is working!` → Katana dùng được. Không thấy → dùng cách 2 hoặc 3.

---

## 1. KHANG — Hạ tầng + Wazuh (vai C)

Khang lo **router, switch, đi dây cho cả nhóm**, rồi dựng Wazuh.

### 1.1 Đi dây & switch
- Cắm điện router TL-WR940N, cắm điện switch.
- Dùng 3 dây mạng nối vào switch: (1) cổng LAN router → switch, (2) máy Hưng → switch,
  (3) máy Khang (Wazuh) → switch.
- Switch để mặc định (không cần VLAN). Nếu switch có quản lý thì để tất cả cùng 1 VLAN.

### 1.2 Cấu hình router (AP nạn nhân)
- Vào trình duyệt: `http://192.168.0.1` (mặc định admin/admin, hoặc đặt mật khẩu lần đầu).
- Wireless → đặt **SSID = `Lab-Cafe-Wifi`**.
- Wireless Security → **WPA2-PSK (AES)**, mật khẩu **yếu** ban đầu: ví dụ `12345678`
  (quan trọng: phải có trong file rockyou.txt để Huy crack ra được).
- Wireless → **Channel = 6** (cố định, KHÔNG để Auto). Ghi lại số 6 này báo cho cả nhóm.
- Ghi lại **BSSID (MAC)** của router (xem trong trang Status) — Huy và Hưng cần.
- WPS → **bật** (để Huy demo tấn công WPS; sẽ tắt ở Phase 4).
- Không cần cắm cổng WAN ra Internet.

### 1.3 Dựng Wazuh
- Cài Wazuh manager + dashboard (máy ảo được). Đặt IP tĩnh cùng dải switch.
- Cài decoder + rule: xem `wazuh/README.md` (đã viết sẵn file `local_decoder.xml`,
  `local_rules.xml`).
- Phối hợp với Hưng đăng ký agent của Hưng về manager.

### 1.4 Đo lường (Phase 5)
- Chạy mỗi màn tấn công nhiều lần, ghi thời gian phát hiện, tỉ lệ đúng/sai.
- Tinh chỉnh ngưỡng rule (frequency/timeframe) và ghi lại lý do.

---

## 2. HƯNG — Cảm biến giám sát (vai B)

Hưng dựng cảm biến nghe lén và chuyển log về Wazuh của Khang.

### 2.1 Chuẩn bị máy
- Cài Ubuntu/Kali + `tshark` (`sudo apt install tshark`) + Wazuh agent.
- Card Wi-Fi chỉ cần monitor (máy Katana hoặc máy nào có monitor đều được).

### 2.2 Bật monitor mode đúng kênh AP (kênh 6 theo Khang)
```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0 6        # thay wlan0 bằng card thật (xem `iw dev`)
```

### 2.3 Chạy cảm biến
- Dùng script đã viết sẵn `sensor/sensor-wids.py`:
```bash
sudo python3 sensor/sensor-wids.py wlan0mon
```
- Script ghi mỗi frame deauth thành 1 dòng vào `/var/log/wifi-wids.log`.

### 2.4 Nối vào Wazuh
- Thêm khối `<localfile>` trỏ `/var/log/wifi-wids.log` vào `ossec.conf` (xem `wazuh/README.md`).
- Restart agent. Báo Khang kiểm tra log đã về manager chưa.

### 2.5 Khi demo
- Luôn **bật cảm biến TRƯỚC khi Huy tấn công**. Giữ máy trong vùng nghe được cả Huy và AP.

---

## 3. HUY — Tấn công (vai A)

Huy chạy AirHunt và thực hiện các màn tấn công.

### 3.1 Chuẩn bị máy
- Cài Kali (hoặc Ubuntu) + AirHunt + aircrack-ng suite.
- Card Wi-Fi **phải inject được** (xem mục 0 — test `Injection is working!`).
- Tải sẵn wordlist `rockyou.txt` (có trong Kali tại `/usr/share/wordlists/`).

### 3.2 Bật monitor mode
```bash
sudo airmon-ng check kill
sudo airmon-ng start wlan0 6        # kênh 6 theo Khang
```

### 3.3 Các kịch bản (xem mục 4 bên dưới) — ghi nhật ký thời điểm từng thao tác.

---

## 4. CÁC KỊCH BẢN TẤN CÔNG (6 màn)

Mỗi màn: Hưng + Khang bật ghi trước, Huy ghi mốc thời gian bắt đầu/kết thúc.

| Màn | Tên | Huy làm | Kỳ vọng ở Wazuh (Khang) |
|---|---|---|---|
| **0** | Baseline | Không tấn công, client lướt web | Dashboard sạch, không alert |
| **1** | Recon (quét) | Quét liệt kê AP/client/kênh | Khó bắt (ghi nhận là giới hạn) |
| **2** | Deauth flood | Gửi đợt deauth vào client | **Alert "Deauth flood" mức cao** |
| **3** | Handshake + crack | Bắt handshake, crack mật khẩu yếu → đổi sang mật khẩu mạnh, crack lại | Bắt được hành vi ép rớt mạng |
| **phụ** | WPS attack | Tấn công WPS (khi WPS bật) | Alert WPS — tùy chọn (xem ghi chú dưới) |
| **4** | PMKID | Lấy PMKID, không deauth | **Khó bắt** (giới hạn hệ thống) |

Chi tiết từng màn: xem `kich-ban-do-an.md` mục 3.

> **Ghi chú phát hiện WPS:** cảm biến mặc định (`sensor-wids.py`) chỉ bắt frame deauth. Rule Wazuh
> đã có sẵn ID 100120 cho `type=wps`, nhưng để nó nổ thì cảm biến phải phát sinh sự kiện `type=wps`
> (đếm burst gói auth/assoc tới AP). Nếu không mở rộng cảm biến → ghi màn WPS là "tấn công minh họa,
> không đo phát hiện". Đây là lựa chọn phạm vi, ghi rõ trong báo cáo.

### Màn 3 — chi tiết so sánh mật khẩu
1. Khang để AP mật khẩu yếu `12345678` → Huy bắt handshake → crack → **ra mật khẩu**.
2. Khang đổi AP sang mật khẩu mạnh (vd `Tr#9kL2$mXq8!vZ`) → Huy bắt handshake lại → crack →
   **chạy hết wordlist vẫn thất bại**.
3. Kết luận: handshake luôn bắt được, an toàn phụ thuộc độ mạnh mật khẩu.

---

## 5. PHẦN PHÒNG THỦ & KIỂM CHỨNG (Phase 4 — cả nhóm)

Chứng minh "vá rồi thì tấn công hết tác dụng". Mỗi biện pháp quay 2 cảnh: trước vá / sau vá.

| Biện pháp | Ai làm | Cách kiểm chứng | Test được trên TL-WR940N? |
|---|---|---|---|
| **Tắt WPS** | Khang (router) | Huy chạy lại WPS attack → thất bại | ✅ Được ngay |
| **Mật khẩu mạnh** | Khang (router) | Huy crack lại → thất bại | ✅ Được ngay (Màn 3) |
| **Không tin lọc MAC** | Khang + Huy | Huy đổi MAC vượt filter dễ dàng → kết luận không nên dùng lọc MAC làm bảo mật chính | ✅ Được |
| **802.11w (PMF)** | cả nhóm | Bật PMF trên **AP phụ WPA3** → Huy deauth → client KHÔNG rớt | ⚠️ Cần AP phụ (hotspot điện thoại đời mới của 1 bạn, hoặc dựng hostapd) |

---

## 6. PHẦN PHÁT HIỆN (DETECTED) — Wazuh của Khang

Đây là "vế thủ" lõi của đồ án. Khi Huy tấn công, Khang trình diễn:
1. Dashboard Wazuh hiện **alert thời gian thực** (rule 100111 "Deauth flood" mức 12).
2. Đối chiếu **thời điểm alert** với nhật ký tấn công của Huy → khớp = hệ thống hoạt động đúng.
3. Bảng số liệu: thời gian phát hiện trung bình, tỉ lệ bắt đúng, false positive.
4. Chỉ ra: màn Recon và PMKID **không** sinh alert → giới hạn của WIDS → hướng phát triển.
5. (Nâng cao) active response: Wazuh tự gửi cảnh báo qua webhook khi phát hiện tấn công.

---

## 7. ĐIỆN THOẠI (CLIENT) — ai dùng?

- **Client nạn nhân:** một điện thoại/laptop **cũ** bất kỳ (bạn nào có máy dư thì góp), Khang kết
  nối sẵn vào `Lab-Cafe-Wifi` lúc dựng lab. **Không ai thao tác** trong lúc demo — nó chỉ cần
  online để đóng vai người dùng thật bị deauth.
- **AP phụ WPA3 (chỉ Phase 4):** một điện thoại **đời mới** (bạn nào có) bật hotspot chuẩn WPA3
  để demo 802.11w. Chỉ dùng ở màn phòng thủ.

---

## 8. THỨ TỰ TỔNG THỂ (ai làm gì trước)

1. **Khang:** đi dây + cấu hình router + dựng Wazuh.  (Phase 0)
2. **Hưng + Khang:** dựng pipeline cảm biến → Wazuh, test thông.  (Phase 2)
3. **Huy:** test injection OK, chuẩn bị AirHunt.  (Phase 0)
4. Cả nhóm bật ghi → **Huy tấn công 6 màn**, Hưng/Khang ghi nhận.  (Phase 3)
5. **Phòng thủ:** Khang vá (tắt WPS, mật khẩu mạnh), Huy chạy lại chứng minh thất bại.  (Phase 4)
6. **Khang:** tổng hợp số liệu.  (Phase 5)
7. Cả nhóm viết báo cáo + slide.  (Phase 6)
