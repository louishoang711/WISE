# Wazuh — hướng dẫn cho Khang (Blue team / Phase 2 + 5)

Thư mục này chứa decoder và rule tùy biến để Wazuh phát hiện tấn công Wi-Fi.

## Luồng hoạt động

```
Cảm biến (Hưng) ghi log  →  Wazuh agent gửi về  →  DECODER bóc trường  →  RULE xét ngưỡng  →  Alert dashboard
```

- `local_decoder.xml` — bóc dòng log thô thành các trường: attack_type, bssid, client, channel, count.
- `local_rules.xml` — xét các trường, sinh cảnh báo (deauth flood, WPS, rogue AP).

## Các bước cài trên máy Wazuh manager

1. Chép 2 file vào đúng chỗ:
   ```bash
   sudo cp local_decoder.xml /var/ossec/etc/decoders/local_decoder.xml
   sudo cp local_rules.xml   /var/ossec/etc/rules/local_rules.xml
   ```
2. Kiểm tra cú pháp + thử decode một dòng log mẫu bằng wazuh-logtest:
   ```bash
   sudo /var/ossec/bin/wazuh-logtest
   ```
   Rồi dán vào dòng:
   ```
   WIFI-WIDS type=deauth bssid=A0:B1:C2:D3:E4:F5 client=11:22:33:44:55:66 channel=6 count=1
   ```
   Kỳ vọng: thấy `decoder: 'wifi-wids'` và các trường được bóc ra, rule 100110 khớp.
3. Khởi động lại manager để áp dụng:
   ```bash
   sudo systemctl restart wazuh-manager
   ```

## Nhận log từ cảm biến của Hưng

Trên **máy của Hưng** (đã cài Wazuh agent), thêm vào `/var/ossec/etc/ossec.conf`:
```xml
<localfile>
  <log_format>syslog</log_format>
  <location>/var/log/wifi-wids.log</location>
</localfile>
```
Rồi `sudo systemctl restart wazuh-agent`. Đăng ký agent với manager của Khang (dùng
`manage_agents` hoặc `agent-auth` theo tài liệu Wazuh).

## Kiểm thử end-to-end

1. Hưng chạy script cảm biến (xem `code/sensor/sensor-wids.py`).
2. Huy gửi một đợt deauth thử.
3. Khang xem dashboard: rule 100111 "Deauth flood" phải nổ ở mức 12 trong vài giây.

## Tinh chỉnh ngưỡng (Phase 5)

Trong `local_rules.xml`, rule 100111 có `frequency="5" timeframe="10"` = 5 gói trong 10 giây.
Nếu báo nhầm nhiều (false positive) → tăng frequency. Nếu bắt chậm → giảm. Ghi lại giá trị
đã chọn và lý do vào báo cáo (phần đo lường).
