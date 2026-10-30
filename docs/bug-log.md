# Nhật ký sửa lỗi (Bug Log) - BT2
- **Lỗi gặp phải:** ModuleNotFoundError khi chạy pytest do thiếu khai báo đường dẫn PYTHONPATH.
- **Cách gỡ (4 bước):** 
  1. Tái lập: Chạy 'pytest' báo lỗi không tìm thấy module 'src'.
  2. Khoanh vùng: Kiểm tra cấu trúc thư mục và thiết lập môi trường Python.
  3. Sửa nguyên nhân: Chạy test bằng lệnh 'python -m pytest tests/'.
  4. Xác nhận: Bộ 5 test chạy PASS hoàn toàn.
