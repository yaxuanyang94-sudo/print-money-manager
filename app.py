import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# --- 設定區 ---
# 1. 之前那個 CSV 下載網址
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSum58yVAkFdh7baIrQ0PnrYys2FnSp4xGbG-oiAILDztPH6MDEtc4-q2fiijT3hO4PfvhUOjcaHkF5/pub?output=csv" 
# 2. 剛剛拿到的 Apps Script 網址
GAS_URL = "https://script.google.com/macros/s/AKfycbwxxuK_AHNNVU6_TbTXDGwvv44P7LrHkNpQjbxqxzRpOoEGwW4u0m9sbWwvllvH7Vc6/exec"

st.set_page_config(page_title="列印金庫-終極版", layout="centered")
st.title("🖨️ 列印金庫 (一鍵儲值)")

# 讀取資料
def load_data():
    url = f"{CSV_URL}&t={datetime.now().timestamp()}"
    return pd.read_csv(url)

df = load_data()

# 側邊欄顯示
st.sidebar.header("💰 目前餘額")
for i, r in df.iterrows():
    st.sidebar.metric(label=r["姓名"], value=f"${r['餘額']:.1f}")

# 處理寫入的函數
def update_balance(name, amount):
    try:
        response = requests.get(f"{GAS_URL}?name={name}&amount={amount}")
        if response.text == "Success":
            st.success(f"✅ 更新成功！{name} 的餘額已同步雲端。")
            st.balloons()
            st.rerun() # 重新整理網頁看到新餘額
        else:
            st.error("❌ 更新失敗，找不到該使用者。")
    except:
        st.error("❌ 連線到雲端時發生錯誤。")

# 主畫面
tab1, tab2 = st.tabs(["📉 扣款", "💰 儲值"])

with tab1:
    u1 = st.selectbox("選擇扣款人", df["姓名"].tolist(), key="p1")
    a1 = st.number_input("扣除金額", min_value=0.0, step=0.1, key="a1")
    if st.button("確認扣款"):
        update_balance(u1, -a1)

with tab2:
    u2 = st.selectbox("選擇儲值對象", df["姓名"].tolist(), key="p2")
    a2 = st.number_input("儲值金額", min_value=0.0, step=10.0, key="a2")
    if st.button("確認儲值"):
        update_balance(u2, a2)
