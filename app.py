import streamlit as st
import pandas as pd
from datetime import datetime

# 基本網頁設定
st.set_page_config(page_title="列印餘額管理系統", layout="centered")
st.title("🖨️ 列印金庫管理")

# 初始化資料 (如果網頁重啟會恢復成這些數字)
if 'data' not in st.session_state:
    st.session_state.data = {
        "楊雅絢": 0,
        "顏子庭": 0,
        "吳郁姍": 0
    }
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 側邊欄：即時餘額顯示 ---
st.sidebar.header("💰 目前餘額")
for name, balance in st.session_state.data.items():
    st.sidebar.metric(label=name, value=f"${balance:.1f}")

# --- 主畫面：功能切換 ---
tab1, tab2 = st.tabs(["📉 扣款 (列印紀錄)", "💰 儲值 (加錢)"])

# 頁籤 1：扣款
with tab1:
    st.subheader("新增列印扣款")
    u1 = st.selectbox("選擇扣款人", list(st.session_state.data.keys()), key="user_pay")
    amt1 = st.number_input("扣除金額", min_value=0.0, step=0.1, format="%.1f", key="pay_amt")
    note1 = st.text_input("扣款備註", placeholder="例：印電子學結報", key="pay_note")
    
    if st.button("確認扣款", use_container_width=True):
        if st.session_state.data[u1] >= amt1:
            st.session_state.data[u1] -= amt1
            log = {"時間": datetime.now().strftime("%m-%d %H:%M"), "使用者": u1, "動作": "扣款", "金額": f"-{amt1}", "備註": note1}
            st.session_state.history.insert(0, log)
            st.success(f"✅ 扣款成功！{u1} 剩餘 ${st.session_state.data[u1]:.1f}")
            st.balloons()
        else:
            st.error("錢不夠啦！快去儲值。")

# 頁籤 2：儲值
with tab2:
    st.subheader("餘額儲值")
    u2 = st.selectbox("選擇儲值對象", list(st.session_state.data.keys()), key="user_add")
    amt2 = st.number_input("儲值金額", min_value=0.0, step=10.0, format="%.1f", key="add_amt")
    
    if st.button("確認儲值", use_container_width=True):
        st.session_state.data[u2] += amt2
        log = {"時間": datetime.now().strftime("%m-%d %H:%M"), "使用者": u2, "動作": "儲值", "金額": f"+{amt2}", "備註": "手動儲值"}
        st.session_state.history.insert(0, log)
        st.success(f"💰 儲值成功！{u2} 目前餘額為 ${st.session_state.data[u2]:.1f}")
        st.snow()

# --- 歷史紀錄顯示 ---
st.divider()
st.subheader("📋 最近交易紀錄")
if st.session_state.history:
    st.table(pd.DataFrame(st.session_state.history).head(10))
else:
    st.info("目前還沒有任何紀錄。")
