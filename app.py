import streamlit as st
import pandas as pd
from datetime import datetime

# --- 這裡填入你的資料 ---
# 1. 之前在試算表「發佈到網路」拿到的 CSV 連結
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSum58yVAkFdh7baIrQ0PnrYys2FnSp4xGbG-oiAILDztPH6MDEtc4-q2fiijT3hO4PfvhUOjcaHkF5/pub?output=csv"
# 2. 你的試算表一般網址
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ueZBzNShwS-szB7zUU2bAeEp7v2X2ZQszm2FqYJA6fE/edit?usp=sharing"

st.set_page_config(page_title="列印計算器", layout="centered")
st.title("🖨️ 列印金庫 (手動同步版)")

# 讀取資料 (加上時間戳記防止快取)
def load_data():
    try:
        url = f"{CSV_URL}&t={datetime.now().timestamp()}"
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # 側邊欄：顯示目前雲端的餘額
    st.sidebar.header("💰 雲端同步餘額")
    for i, r in df.iterrows():
        st.sidebar.metric(label=r["姓名"], value=f"${r['餘額']:.1f}")

    # 主畫面：扣款計算
    st.subheader("📉 扣款計算器")
    user = st.selectbox("誰印了東西？", df["姓名"].tolist())
    
    # 抓取該使用者的目前餘額
    current_val = df.loc[df["姓名"] == user, "餘額"].values[0]
    
    amount = st.number_input("花了多少錢？", min_value=0.0, step=0.1, format="%.1f")
    
    if amount > 0:
        new_val = round(current_val - amount, 1)
        st.error(f"⚠️ 請注意：{user} 的新餘額應改為 **{new_val}**")
        st.link_button("🚀 點我打開 Excel 改錢", SHEET_URL)
        st.info("在 Excel 改完後，回到這裡重新整理，數字就會變了！")
else:
    st.error("讀取失敗，請檢查試算表是否已發佈為 CSV。")
