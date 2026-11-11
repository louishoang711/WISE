#!/bin/sh
# Chạy 1 lần sau khi clone: kích hoạt hook chặn push lên main
git config core.hooksPath .githooks
echo "Đã bật hook. Từ giờ không thể push trực tiếp lên main."
