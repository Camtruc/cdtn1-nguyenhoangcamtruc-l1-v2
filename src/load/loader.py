import sqlite3
import pandas as pd
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DB_PATH = ROOT / "data" / "mekong_warehouse.db"

def init_dwh(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_customer (
        customer_key INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id VARCHAR(20) UNIQUE NOT NULL,
        full_name VARCHAR(100) NOT NULL,
        masked_phone VARCHAR(15) NOT NULL,
        address VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dim_date (
        date_key INTEGER PRIMARY KEY,
        full_date DATE UNIQUE NOT NULL,
        day_of_week VARCHAR(15) NOT NULL,
        month INTEGER NOT NULL,
        quarter INTEGER NOT NULL,
        year INTEGER NOT NULL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fact_purchase (
        purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_key INTEGER NOT NULL,
        date_key INTEGER NOT NULL,
        order_id VARCHAR(20) UNIQUE NOT NULL,
        total_amount BIGINT NOT NULL,
        recency_days INTEGER NOT NULL,
        frequency_count INTEGER NOT NULL,
        monetary_amount BIGINT NOT NULL,
        rfm_segment VARCHAR(50) NOT NULL,
        FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key),
        FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
    );
    """)
    conn.commit()

def load_data_to_dwh(df_final: pd.DataFrame, customers_df: pd.DataFrame = None):
    conn = sqlite3.connect(DB_PATH)
    init_dwh(conn)
    cursor = conn.cursor()

    for cid in df_final['customer_id'].unique():
        cursor.execute("""
        INSERT OR IGNORE INTO dim_customer (customer_id, full_name, masked_phone, address)
        VALUES (?, ?, ?, ?);
        """, (cid, f"Khach hang {cid}", "090****567", "Ho Chi Minh"))
    conn.commit()
    cust_map = dict(cursor.execute("SELECT customer_id, customer_key FROM dim_customer").fetchall())

    inserted_count = 0
    for _, r in df_final.iterrows():
        order_date_str = str(r['order_date']).strip()
        try:
            dt = datetime.strptime(order_date_str, "%Y-%m-%d")
        except ValueError:
            continue
        d_key = int(dt.strftime("%Y%m%d"))
        cursor.execute("""
        INSERT OR IGNORE INTO dim_date (date_key, full_date, day_of_week, month, quarter, year)
        VALUES (?, ?, ?, ?, ?, ?);
        """, (d_key, order_date_str, dt.strftime("%A"), dt.month, (dt.month - 1) // 3 + 1, dt.year))

        c_key = cust_map.get(str(r['customer_id']).strip())
        if c_key:
            cursor.execute("""
            INSERT OR IGNORE INTO fact_purchase (
                customer_key, date_key, order_id, total_amount,
                recency_days, frequency_count, monetary_amount, rfm_segment
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
            """, (
                c_key, d_key, str(r['order_id']), int(r['total_amount']),
                int(r['recency_days']), int(r['frequency_count']),
                int(r['monetary_amount']), str(r['rfm_segment'])
            ))
            if cursor.rowcount > 0:
                inserted_count += 1
    conn.commit()
    total_fact = cursor.execute("SELECT COUNT(*) FROM fact_purchase").fetchone()[0]
    conn.close()
    return inserted_count, total_fact
