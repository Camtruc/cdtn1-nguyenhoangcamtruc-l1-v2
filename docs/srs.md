# BẢN ĐẶC TẢ YÊU CẦU PHẦN MỀM (SRS RÚT GỌN) & ĐẶC TẢ DỮ LIỆU
**Học phần:** Chuyên đề Tốt nghiệp 1 (HK1 2026-2027)
**Sinh viên:** Nguyễn Hoàng Cẩm Trúc - MSSV: 2374802010526
**Track:** Data Analytics (DA) | **Luồng nghiệp vụ:** L1 - Hồ sơ khách hàng & Phân khúc
*(Tài liệu biên soạn theo tinh thần chuẩn ISO/IEC/IEEE 29148)*

## 1. GIỚI THIỆU VÀ PHẠM VI
- Bối cảnh: Chuỗi bán lẻ Mekong Mobile phát sinh lượng giao dịch lớn nhưng chưa khai thác phân khúc khách hàng, dẫn đến tiếp thị đại trà kém hiệu quả.
- Phát biểu phạm vi: Thu thập và xử lý lịch sử giao dịch khách hàng, sau đó áp dụng mô hình phân tích RFM để phân nhóm khách hàng thành các phân khúc (VIP, Thường xuyên, Mới, Ngủ đông) và trực quan hóa lên dashboard.
- Điều CHỦ Ý KHÔNG LÀM (MoSCoW - WON'T): Không xây dựng mô hình Deep Learning dự đoán tương lai; không tích hợp hệ thống tự động gửi tin nhắn tiếp thị; không can thiệp cổng thanh toán.
- Bảng thuật ngữ: RFM (Recency, Frequency, Monetary), Grain, Fact table, Dimension table.

## 2. CÁC BÊN LIÊN QUAN VÀ VAI TRÒ NGƯỜI DÙNG (ACTORS)
- Nhân viên Marketing: Khai thác danh sách khách hàng theo phân khúc, phân tích xu hướng chi tiêu để lập chiến dịch.
- Nhân viên Bán hàng: Tra cứu nhanh phân khúc và lịch sử mua của khách hàng bằng số điện thoại để tư vấn phù hợp.
- Quản lý Cửa hàng: Xem dashboard tổng hợp tỷ lệ phân bố phân khúc và theo dõi tỷ lệ biến động khách hàng.
- Hệ thống Scheduler: Tự động chạy tiến trình tổng hợp và phân loại RFM định kỳ theo lịch.

## 3. YÊU CẦU CHỨC NĂNG (FR) VÀ USER STORY
- FR1: Hệ thống tổng hợp dữ liệu giao dịch để tính toán 3 chỉ số R, F, M cho từng khách hàng duy nhất.
- FR2: Hệ thống tự động phân loại khách hàng thành 4 phân khúc (VIP, Thường xuyên, Mới, Ngủ đông) theo ngưỡng RFM.
- FR3: Hệ thống cho phép tra cứu hồ sơ và phân khúc khách hàng bằng số điện thoại hoặc mã khách hàng.
- FR4: Hệ thống trực quan hóa cơ cấu phân khúc và tổng chi tiêu theo phân khúc lên Dashboard phân tích.
- FR5: Hệ thống cho phép lọc danh sách khách hàng nhóm "Ngủ đông" để hỗ trợ chiến dịch kích hoạt lại.

Danh sách User Story:
- US1 [MUST]: Là nhân viên Marketing, tôi muốn tính tổng giá trị mua hàng của từng khách hàng để đánh giá mức độ đóng góp tài chính.
- US2 [MUST]: Là nhân viên Marketing, tôi muốn tính số ngày từ lần mua gần nhất và số lần mua hàng để đánh giá mức độ tương tác.
- US3 [MUST]: Là nhân viên Marketing, tôi muốn hệ thống tự động gán nhãn phân khúc (VIP, Thường xuyên, Mới, Ngủ đông) theo thang điểm RFM để quản lý tệp khách hàng.
- US4 [MUST]: Là nhân viên Bán hàng, tôi muốn tra cứu phân khúc khách hàng bằng số điện thoại để đưa ra tư vấn và ưu đãi phù hợp.
- US5 [SHOULD]: Là quản lý Cửa hàng, tôi muốn xem biểu đồ phân bố tỷ lệ khách hàng theo các nhóm RFM trên dashboard để đánh giá chất lượng tệp khách hàng.
- US6 [SHOULD]: Là quản lý Cửa hàng, tôi muốn xem danh sách khách hàng "Ngủ đông" có tổng chi tiêu lịch sử cao để ưu tiên liên hệ chăm sóc.
- US7 [COULD]: Là nhân viên Marketing, tôi muốn xuất danh sách mã khách hàng theo phân khúc ra file CSV để phục vụ chiến dịch quảng cáo ngoài.
- US8 [COULD]: Là nhân viên Bán hàng, tôi muốn xem danh sách 3 sản phẩm khách hàng mua gần nhất khi tra cứu để gợi ý phụ kiện phù hợp.

## 4. YÊU CẦU PHI CHỨC NĂNG (NFR)
- NFR1 (Hiệu năng): Làm sạch và tính điểm RFM cho 50.000 dòng giao dịch hoàn thành dưới 20 giây trên máy 8GB RAM.
- NFR2 (Bảo mật): Số điện thoại khách hàng trên giao diện Dashboard hiển thị che 4 số ở giữa (090****567).
- NFR3 (Khả dụng): Dashboard phân tích phản hồi thao tác lọc theo phân khúc/thời gian dưới 1,5 giây.

## 5. RÀNG BUỘC VÀ QUY TẮC NGHIỆP VỤ
- QT-01: Chỉ các đơn hàng có trạng thái "Completed" mới được tính vào Frequency và Monetary.
- QT-02: Kỳ phân tích RFM được giới hạn trong 365 ngày gần nhất.
- QT-03: Khóa nhận diện khách hàng duy nhất là customer_id, khử trùng theo số điện thoại chuẩn 10 chữ số.

## 6. BẢNG TRUY VẾT YÊU CẦU
- FR1 -> US1, US2 -> UC1 -> MUST -> TC_DA_01, TC_DA_02
- FR2 -> US3 -> UC2 -> MUST -> TC_DA_03
- FR3 -> US4, US8 -> UC3 -> MUST -> TC_DA_04
- FR4 -> US5 -> UC4 -> SHOULD -> TC_DA_05
- FR5 -> US6 -> UC5 -> SHOULD -> TC_DA_06
- FR6 -> US7 -> UC6 -> COULD -> (Khong hien thuc)

## 7. ĐẶC TẢ YÊU CẦU DỮ LIỆU (DATA SPEC)
- Grain: Một dòng trong bảng fact_customer_rfm đại diện cho CÁC CHỈ SỐ VÀ PHÂN KHÚC RFM CỦA MỘT KHÁCH HÀNG trong MỘT KỲ PHÂN TÍCH.
- Nguồn: orders_2024_2026.csv và customers.csv (Mekong Mobile).
- Tiêu chuẩn CL1-CL4: Tỉ lệ thiếu của customer_id, order_date, total_amount sau làm sạch bằng 0%. 100% ngày chuyển về chuẩn ISO YYYY-MM-DD.
