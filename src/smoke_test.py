# Script smoke test kiem tra moi truong phat trien - Luong L1
orders = [
    {"order_id": "DH001", "customer": "Nguyen Van A", "total": 250000, "status": "Pending"},
    {"order_id": "DH002", "customer": "Tran Thi B", "total": 540000, "status": "Completed"},
    {"order_id": "DH003", "customer": "Le Van C", "total": 1200000, "status": "Processing"},
]

print("========================================")
print("   SMOKE TEST - CHUYEN DE TOT NGHIEP 1   ")
print("========================================")
print("Moi truong Python va runtime chay thanh cong!")
print(f"Khoi tao du lieu mau: {len(orders)} don hang.")
print("----------------------------------------")
for order in orders:
    print(f"- Ma DH: {order['order_id']} | Khach: {order['customer']} | Tong: {order['total']:,} VND | Trang thai: {order['status']}")
print("========================================")