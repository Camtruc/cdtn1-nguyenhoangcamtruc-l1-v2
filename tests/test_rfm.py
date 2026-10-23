import pytest
import pandas as pd
from datetime import datetime
from src.pipeline import transform_and_validate, calculate_rfm

def test_1_valid_pipeline_flow():
    """Luồng đúng: Đơn hợp lệ được giữ lại."""
    data = pd.DataFrame([{"order_id": "DH1", "customer_id": "KH1", "order_date": "2026-10-10", "order_status": "Completed", "total_amount": 1000000}])
    clean = transform_and_validate(data)
    assert len(clean) == 1

def test_2_reject_invalid_date():
    """Dữ liệu sai: Ngày không hợp lệ bị loại sang rejects."""
    data = pd.DataFrame([{"order_id": "DH2", "customer_id": "KH2", "order_date": "sai_ngay", "order_status": "Completed", "total_amount": 1000000}])
    clean = transform_and_validate(data)
    assert len(clean) == 0

def test_3_reject_cancelled_order():
    """Nghiệp vụ QT-01: Đơn huỷ không được tính."""
    data = pd.DataFrame([{"order_id": "DH3", "customer_id": "KH3", "order_date": "2026-10-10", "order_status": "Cancelled", "total_amount": 1000000}])
    clean = transform_and_validate(data)
    assert len(clean) == 0

def test_4_boundary_vip_segment():
    """Giá trị biên: Đạt ngưỡng 20.000.000 VND là VIP."""
    data = pd.DataFrame([{"order_id": "DH4", "customer_id": "KH_VIP", "order_date": "2026-10-10", "total_amount": 20000000}])
    rfm = calculate_rfm(data)
    assert rfm.iloc[0]['rfm_segment'] == "VIP"

def test_5_boundary_dormant_segment():
    """Giá trị biên: Không mua trên 180 ngày là Ngủ đông."""
    data = pd.DataFrame([{"order_id": "DH5", "customer_id": "KH_OLD", "order_date": "2026-03-01", "total_amount": 500000}])
    rfm = calculate_rfm(data)
    assert rfm.iloc[0]['rfm_segment'] == "Ngu_dong"
