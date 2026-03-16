import streamlit as st
import pandas as pd
from datetime import datetime

# --- 設定區 ---
# 請在這裡貼上你的 Google 試算表網址
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ueZBzNShwS-szB7zUU2bAeEp7v2X2ZQszm2FqYJA6fE/edit?usp=sharing"
# 將網址轉換為 CSV 下載格式
CSV_URL = SHEET_URL.replace("/edit?usp=sharing", "/export?format=csv").replace("/edit#gid=0", "/export?format=csv")

st.set_page_config(page_title="列印金庫-永久儲存版", layout="centered")
st.title("🖨️ 列印金庫 (資料已連動)")

# 從 Google Sheets 讀取資料
def load_data():
    try:
        # 加上 timestamp 防止快取
        df = pd.read_csv(f"{CSV_URL}&t={datetime.now().timestamp()}")
        return df
    except:
        st.error("讀取資料失敗，請檢查試算表權限是否已開啟「編輯者」給任何人。")
        return pd.DataFrame(columns=["姓名", "餘額"])

df = load_data()

# --- 側邊欄：即時餘額顯示 ---
st.sidebar.header("💰 目前餘額")
if not df.empty:
    for index, row in df.iterrows():
        st.sidebar.metric(label=row["姓名"], value=f"${row['餘額']:.1f}")

# --- 主畫面 ---
tab1, tab2 = st.tabs(["📉 扣款", "💰 儲值"])

with tab1:
    user = st.selectbox("選擇扣款人", df["姓名"].tolist() if not df.empty else [])
    amount = st.number_input("扣除金額", min_value=0.0, step=0.1, format="%.1f")
    if st.button("確認扣款", use_container_width=True):
        # 這裡會提醒你去 Google Sheets 手動更新或查看
        st.info(f"請到 Google 試算表將 {user} 的餘額減去 {amount}")
        st.warning("提示：目前的簡易部署版建議搭配 Google Sheets App 直接修改數字，網站會即時同步！")

with tab2:
    st.write("請直接打開手機的 Google Sheets APP 進行儲值，本網頁會自動更新顯示。")
    st.link_button("打開我的 Google 試算表", SHEET_URL)

st.divider()
st.caption("註：目前為了安全性與簡便性，建議直接在 Google Sheets 修改數字，本網站負責展示與計算。")
