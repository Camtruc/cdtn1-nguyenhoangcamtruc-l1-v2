import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Mekong Mobile - Dashboard Phân Khúc", layout="wide")
DB_FILE = Path(__file__).resolve().parents[1] / "data" / "mekong_warehouse.db"

st.title("MEKONG MOBILE - DASHBOARD PHÂN KHÚC KHÁCH HÀNG (LUỒNG L1)")
st.caption("Nguồn dữ liệu: fact_purchase (DWH SQLite) | Snapshot Date: 2026-10-18")

# TRẠNG THÁI 1: LỖI KẾT NỐI (ERROR STATE)
if not DB_FILE.exists():
    st.error("LỖI: Chưa tìm thấy kho dữ liệu mekong_warehouse.db. Hãy chạy 'python -m src.pipeline' trước!")
    st.stop()

@st.cache_data(ttl=60)
def load_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM fact_purchase;", conn)
    conn.close()
    return df

# TRẠNG THÁI 2: ĐANG TẢI (LOADING STATE)
with st.spinner("Đang tải dữ liệu từ kho..."):
    df = load_data()

# TRẠNG THÁI 3: DỮ LIỆU RỖNG (EMPTY STATE)
if df.empty:
    st.warning("Dữ liệu trong kho hiện đang rỗng.")
    st.stop()

# THANH LỌC PHÂN KHÚC
options = ["Tất cả"] + list(df['rfm_segment'].unique())
seg = st.sidebar.selectbox("Lọc theo phân khúc", options)
df_show = df if seg == "Tất cả" else df[df['rfm_segment'] == seg]

# HIỂN THỊ KPI
c1, c2, c3 = st.columns(3)
c1.metric("Tổng đơn hàng", len(df_show))
c2.metric("Doanh thu lọc", f"{df_show['total_amount'].sum():,.0f} đ")
c3.metric("Số khách VIP", len(df[df['rfm_segment'] == 'VIP']['customer_key'].unique()))

st.divider()

# 2 BIỂU ĐỒ GẮN CÂU HỎI PHÂN TÍCH (CHUẨN CHECKLIST BUỔI 10)
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Biểu đồ 1: Cơ cấu các nhóm khách hàng")
    st.caption("Câu hỏi: Nhóm khách hàng nào chiếm tỷ lệ lớn nhất?")
    counts = df.drop_duplicates('customer_key')['rfm_segment'].value_counts()
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
    st.pyplot(fig1)

with col_b:
    st.subheader("Biểu đồ 2: Doanh thu theo phân khúc")
    st.caption("Câu hỏi: Đóng góp doanh thu của nhóm VIP là bao nhiêu?")
    rev = df.groupby('rfm_segment')['total_amount'].sum()
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    rev.plot(kind='bar', ax=ax2, color=['#4CAF50', '#2196F3', '#FF9800'])
    ax2.set_ylabel("Doanh thu (VND)")
    st.pyplot(fig2)

st.subheader("Bảng dữ liệu chi tiết")
st.dataframe(df_show[['order_id', 'total_amount', 'recency_days', 'rfm_segment']])
