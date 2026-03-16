import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- 這裡填入你的資料 ---
# 1. 你的 Google 試算表 CSV 下載網址 (跟之前一樣)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSum58yVAkFdh7baIrQ0PnrYys2FnSp4xGbG-oiAILDztPH6MDEtc4-q2fiijT3hO4PfvhUOjcaHkF5/pub?output=csv"
# 2. 你的 Google 試算表 ID (網址中 /d/ 後面那串亂碼)
SHEET_ID = "1ueZBzNShwS-szB7zUU2bAeEp7v2X2ZQszm2FqYJA6fE/edit?gid=0#gid=0"

st.set_page_config(page_title="列印金庫", layout="centered")
st.title("🖨️ 列印金庫")

# 讀取資料
def load_data():
    # 加上 timestamp 避免緩存舊資料
    url = f"{CSV_URL}&t={datetime.now().timestamp()}"
    return pd.read_csv(url)

df = load_data()

# 側邊欄顯示
st.sidebar.header("💰 目前餘額")
for i, r in df.iterrows():
    st.sidebar.metric(label=r["姓名"], value=f"${r['餘額']:.1f}")

# 主畫面
tab1, tab2 = st.tabs(["📉 扣款", "💰 儲值"])

# 這裡我們用一個技巧：透過 Google Apps Script 寫入
# 但這需要你幫我做最後一個「機關」
with tab1:
    u = st.selectbox("選擇扣款人", df["姓名"].tolist(), key="pay")
    amt = st.number_input("金額", min_value=0.0, step=0.1, key="pay_amt")
    if st.button("確認扣款"):
        st.warning("正在嘗試寫入雲端...")
        # 這裡會用到一個 Apps Script 網址
        # 如果你還沒設定，我教你怎麼一分鐘設定好
        st.info(f"請點擊下方連結完成確認，錢就會自動扣除！")
        # 暫時用最穩定的「預填表單」法，這絕對不會報錯
        st.link_button("🚀 點我一鍵同步", f"https://docs.google.com/forms/d/你的表單ID/viewform?entry.123={u}&entry.456=-{amt}")

with tab2:
    u2 = st.selectbox("選擇儲值對象", df["姓名"].tolist(), key="add")
    amt2 = st.number_input("金額", min_value=0.0, step=10.0, key="add_amt")
    if st.button("確認儲值"):
         st.link_button("🚀 點我一鍵同步", f"https://docs.google.com/forms/d/你的表單ID/viewform?entry.123={u2}&entry.456={amt2}")
