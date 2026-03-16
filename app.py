import streamlit as st
import pandas as pd
from datetime import datetime

# --- 設定區 ---
# 1. 這裡貼上你之前在試算表「發佈到網路」拿到的 CSV 連結
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSum58yVAkFdh7baIrQ0PnrYys2FnSp4xGbG-oiAILDztPH6MDEtc4-q2fiijT3hO4PfvhUOjcaHkF5/pub?output=csv"
# 2. 這裡貼上你的試算表一般網址，方便一鍵跳轉去改錢
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ueZBzNShwS-szB7zUU2bAeEp7v2X2ZQszm2FqYJA6fE/edit?usp=sharing"

st.set_page_config(page_title="列印金庫-手動同步版", layout="centered")
st.title("🖨️ 列印金庫")

# 讀取資料
def load_data():
    # 加上 timestamp 避免緩存
    url = f"{CSV_URL}&t={datetime.now().timestamp()}"
    return pd.read_csv(url)

try:
    df = load_data()
    # 側邊欄：即時餘額顯示
    st.sidebar.header("💰 目前餘額")
    for i, r in df.iterrows():
        st.sidebar.metric(label=r["姓名"], value=f"${r['餘額']:.1f}")

    # 主畫面
    st.subheader("📉 扣款計算器")
    u = st.selectbox("選擇扣款人", df["姓名"].tolist())
    current_balance = df.loc[df["姓名"] == u, "餘額"].values[0]
    
    amt = st.number_input("輸入扣除金額", min_value=0.0, step=0.1)
    new_balance = current_balance - amt

    if amt > 0:
        st.warning(f"💡 扣完錢後，{u} 的餘額應該要改成： **${new_balance:.1f}**")
        st.link_button("👉 點我打開 Excel 去修改數字", SHEET_URL)
        
    st.divider()
    st.info("提示：在 Excel 改完數字後，回到這裡重新整理網頁，餘額就會更新了！")

except Exception as e:
    st.error("讀取失敗，請確認試算表已『發佈到網路』為 CSV 格式。")
