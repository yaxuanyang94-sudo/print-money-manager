import streamlit as st
import pandas as pd
from datetime import datetime

# 設定網頁標題
st.set_page_config(page_title="列印餘額管理系統", layout="centered")
st.title("🖨️ 列印餘額管理")

# 這裡模擬初始資料 (實務上可串接 Google Sheets 或 Database)
if 'data' not in st.session_state:
    st.session_state.data = {
        "你": 500.0,
        "謝明洋": 500.0
    }
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 側邊欄：顯示餘額 ---
st.sidebar.header("💰 目前餘額")
for name, balance in st.session_state.data.items():
    st.sidebar.metric(label=name, value=f"${balance:.1f}")

# --- 主畫面：扣款功能 ---
st.subheader("新增列印紀錄")
col1, col2 = st.columns(2)

with col1:
    user = st.selectbox("選擇使用者", list(st.session_state.data.keys()))
with col2:
    amount = st.number_input("扣除金額", min_value=0.0, step=0.1, format="%.1f")

reason = st.text_input("備註 (例如：電磁學講義 10頁)", placeholder="可不填")

if st.button("確認扣款", use_container_width=True):
    if st.session_state.data[user] >= amount:
        st.session_state.data[user] -= amount
        # 紀錄歷史紀錄
        log = {
            "時間": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "使用者": user,
            "金額": f"-{amount}",
            "備註": reason
        }
        st.session_state.history.insert(0, log)
        st.success(f"✅ 成功！{user} 的餘額已更新。")
        st.balloons()
    else:
        st.error("餘額不足！請先儲值。")

# --- 顯示近期紀錄 ---
st.divider()
st.subheader("📋 最近 10 筆紀錄")
if st.session_state.history:
    df = pd.DataFrame(st.session_state.history)
    st.table(df.head(10))
else:
    st.info("目前還沒有紀錄喔！")
