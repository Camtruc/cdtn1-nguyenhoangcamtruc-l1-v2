import os
import pandas as pd
from datetime import datetime
from pathlib import Path
from src.load.loader import load_data_to_dwh

ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = ROOT / "data" / "raw" / "transactions.csv"
REJECT_FILE = ROOT / "data" / "rejects" / "reject_records.csv"
SNAPSHOT_DATE = "2026-10-18"

def extract():
    print("--- [1/4] EXTRACT: Doc du lieu nguon ---")
    if not RAW_FILE.exists():
        raise FileNotFoundError(f"Khong tim thay file {RAW_FILE}")
    df = pd.read_csv(RAW_FILE)
    print(f"Tong so dong doc duoc: {len(df)}")
    return df

def transform_and_validate(df):
    print("--- [2/4] TRANSFORM & VALIDATE: Lam sach & Tach loi ---")
    valid_rows, reject_rows = [], []
    for idx, row in df.iterrows():
        try:
            datetime.strptime(str(row['order_date']).strip(), "%Y-%m-%d")
        except Exception:
            reject_rows.append({**row.to_dict(), "reject_reason": "Dinh dang ngay khong hop le"})
            continue
        if str(row['order_status']).strip() != "Completed":
            reject_rows.append({**row.to_dict(), "reject_reason": "Don hang bi huy hoac chua hoan tat"})
            continue
        valid_rows.append(row.to_dict())
    df_clean = pd.DataFrame(valid_rows)
    df_reject = pd.DataFrame(reject_rows)
    if not df_reject.empty:
        df_reject.to_csv(REJECT_FILE, index=False, encoding='utf-8')
        print(f"Da tach {len(df_reject)} dong loi vao {REJECT_FILE}")
    print(f"So dong hop le giu lai: {len(df_clean)}")
    return df_clean

def calculate_rfm(df_clean):
    print("--- [3/4] RFM SEGMENTATION: Tinh toan phan khuc ---")
    snapshot_dt = datetime.strptime(SNAPSHOT_DATE, "%Y-%m-%d")
    cust_groups = df_clean.groupby('customer_id')
    rfm_list = []
    for cid, group in cust_groups:
        max_dt = datetime.strptime(group['order_date'].max(), "%Y-%m-%d")
        r_days = (snapshot_dt - max_dt).days
        f_count = len(group)
        m_total = group['total_amount'].sum()
        if m_total >= 20000000:
            seg = "VIP"
        elif r_days > 180:
            seg = "Ngu_dong"
        elif r_days <= 30:
            seg = "Moi"
        else:
            seg = "Thuong_xuyen"
        rfm_list.append({
            "customer_id": cid,
            "recency_days": max(r_days, 0),
            "frequency_count": f_count,
            "monetary_amount": m_total,
            "rfm_segment": seg
        })
    df_rfm = pd.DataFrame(rfm_list)
    df_final = df_clean.merge(df_rfm, on='customer_id', how='left')
    return df_final

def run_pipeline():
    df_raw = extract()
    df_clean = transform_and_validate(df_raw)
    df_final = calculate_rfm(df_clean)
    print("--- [4/4] LOAD DWH: Goi module src/load/loader.py ---")
    inserted, total = load_data_to_dwh(df_final)
    print(f"So dong moi nap vao fact_purchase: {inserted}")
    print(f"Tong so dong hien tai trong fact_purchase: {total}")
    print("\n>>> PIPELINE CHAY END-TO-END THANH CONG! <<<")

if __name__ == "__main__":
    run_pipeline()
