import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="列印金庫-全自動版", layout="centered")
st.title("🖨️ 列印金庫 (一鍵存檔)")

# 建立 Google Sheets 連線
conn = st.connection("gsheets", type=GSheetsConnection)

# 讀取現有資料
df = conn.read(ttl="0s") # ttl=0s 確保每次都讀最新資料

# --- 側邊欄：顯示餘額 ---
st.sidebar.header("💰 目前餘額")
for index, row in df.iterrows():
    st.sidebar.metric(label=row["姓名"], value=f"${row['餘額']:.1f}")

# --- 主畫面 ---
tab1, tab2 = st.tabs(["📉 扣款", "💰 儲值"])

with tab1:
    u1 = st.selectbox("選擇扣款人", df["姓名"].tolist(), key="pay_user")
    amt1 = st.number_input("扣除金額", min_value=0.0, step=0.1, key="pay_amt")
    if st.button("確認扣款"):
        # 計算新餘額並更新 DataFrame
        df.loc[df["姓名"] == u1, "餘額"] -= amt1
        conn.update(data=df) # 寫回 Google Sheets
        st.success(f"✅ 扣款成功！{u1} 的新餘額已存入雲端。")
        st.balloons()

with tab2:
    u2 = st.selectbox("選擇儲值對象", df["姓名"].tolist(), key="add_user")
    amt2 = st.number_input("儲值金額", min_value=0.0, step=10.0, key="add_amt")
    if st.button("確認儲值"):
        # 計算新餘額並更新 DataFrame
        df.loc[df["姓名"] == u2, "餘額"] += amt2
        conn.update(data=df) # 寫回 Google Sheets
        st.success(f"💰 儲值成功！雲端資料已更新。")
        st.snow()

st.divider()
st.info("提示：若餘額沒有即時更新，請手動重新整理網頁。")
