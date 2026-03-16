import streamlit as st
import pandas as pd
from datetime import datetime

# --- 設定區 ---
# 1. 這裡填入你的 Google 試算表 CSV 下載連結
# (試算表點「檔案」>「共用」>「發佈到網路」> 選擇「整個文件」和「CSV」)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSum58yVAkFdh7baIrQ0PnrYys2FnSp4xGbG-oiAILDztPH6MDEtc4-q2fiijT3hO4PfvhUOjcaHkF5/pub?output=csv"
# 2. 這裡填入你的 Google 試算表網址，方便點擊去手動改錢
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ueZBzNShwS-szB7zUU2bAeEp7v2X2ZQszm2FqYJA6fE/edit?usp=sharing"

st.set_page_config(page_title="列印金庫-穩定版", layout="centered")
st.title("🖨️ 列印金庫")

# 讀取資料
def load_data():
    return pd.read_csv(f"{CSV_URL}&t={datetime.now().timestamp()}")

df = load_data()

st.sidebar.header("💰 目前餘額")
for i, r in df.iterrows():
    st.sidebar.metric(label=r["姓名"], value=f"${r['餘額']:.1f}")

tab1, tab2 = st.tabs(["📉 扣款", "💰 儲值"])

with tab1:
    u = st.selectbox("選擇扣款人", df["姓名"].tolist())
    amt = st.number_input("金額", min_value=0.0, step=0.1)
    if st.button("確認"):
        st.success(f"已記錄！請點下方連結進入試算表，將 {u} 的餘額改為 {df.loc[df['姓名']==u, '餘額'].values[0] - amt}")
        st.link_button("打開試算表動手改錢", SHEET_URL)

with tab2:
    st.info("儲值請直接點擊下方按鈕，在 Excel 裡修改數字即可同步！")
    st.link_button("打開試算表去加錢", SHEET_URL)
