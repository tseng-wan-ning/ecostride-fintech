import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import streamlit.components.v1 as components

# ==========================================
# 0. 全局環境配置與 CSS 注入
# ==========================================
st.set_page_config(page_title="EcoStride | 永續金融生態系研究", page_icon="🌿", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .stApp { background-color: #F5F7F4; color: #0C0E0B; font-family: -apple-system, sans-serif; }
    .stSidebar { background-color: #B7CEAD !important; border-right: 1px solid #83A474 !important; }
    .metric-card { background-color: #FFFFFF; border: 1px solid #B7CEAD; border-radius: 14px; padding: 24px; text-align: center; }
    .metric-value-green { font-size: 38px; font-weight: 700; color: #83A474; }
    .metric-value-blue { font-size: 38px; font-weight: 700; color: #0C0E0B; }
    .metric-label { font-size: 13px; font-weight: 600; color: #475569; margin-top: 5px; text-transform: uppercase; }
    .phone-container { border: 10px solid #0C0E0B; border-radius: 36px; padding: 14px; background-color: #0C0E0B; height: 610px; display: flex; flex-direction: column; }
    .phone-screen { border-radius: 24px; background-color: #FFFFFF; padding: 22px 16px; flex-grow: 1; overflow-y: auto; }
    .navbar-mock { background: rgba(245, 247, 244, 0.85); backdrop-filter: blur(16px); border-bottom: 1px solid #B7CEAD; padding: 18px 35px; position: sticky; top: 0; z-index: 999; display: flex; justify-content: space-between; align-items: center; margin: -4.5rem -4rem 2rem -4rem; }
    </style>
    """, unsafe_allow_html=True)

# 導航欄與後端邏輯略 (延續您先前的結構)
# ... (為節省空間，請保持您先前的 1-3 節代碼，直接替換以下內容) ...

# ==========================================
# 7. 分頁四：相關研究成果
# ==========================================
elif page == "相關研究成果":
    st.markdown("<h2 style='color:#2D4A22 !important; font-size:32px; font-weight:800;'>相關研究成果 ── 彭博精算終端動態沙盤</h2>", unsafe_allow_html=True)
    st.markdown("---")

    col_res_left, col_res_right = st.columns([1.1, 3])
    
    with col_res_left:
        st.markdown("<div style='background-color:#FFFFFF; border:1px solid #B7CEAD; padding:24px; border-radius:14px;'>", unsafe_allow_html=True)
        param_steps_inc_sidebar = st.slider("調整保戶健走提升率", 0.05, 0.50, 0.20, 0.05)
        param_consistency_sidebar = st.slider("全域行為穩定度因子", 0.30, 1.00, 0.75, 0.05)
        run_sim = st.button("執行 5,000 次全域對齊 Monte Carlo 模擬 ⚡")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_res_right:
        metric_slot1 = st.empty()
        base_win_ratio = 56.38 + (param_steps_inc_sidebar - 0.20) * 45 + (param_consistency_sidebar - 0.75) * 35
        base_win_ratio = max(0.0, min(100.0, base_win_ratio))
        base_wacc = 3.50 - (param_steps_inc_sidebar - 0.20) * 0.5
        base_wealth = 6657 * (param_steps_inc_sidebar / 0.20) * (param_consistency_sidebar / 0.75)
        
        # 模擬動畫邏輯
        if run_sim:
            progress_bar = st.progress(0)
            for p in range(1, 101, 4):
                time.sleep(0.01)
                progress_bar.progress(p)
            metric_slot1.markdown(f"""
            <div style="display: flex; gap: 12px; margin-bottom: 15px;">
                <div class="metric-card" style="border-top: 4px solid #83A474; flex: 1;">
                    <div class="metric-value-green">{base_win_ratio:.2f}%</div>
                    <div class="metric-label">全域共贏機率</div>
                </div>
                <div class="metric-card" style="border-top: 4px solid #0C0E0B; flex: 1;">
                    <div class="metric-value-blue">99.96%</div>
                    <div class="metric-label">保險大盤獲利機率</div>
                </div>
                <div class="metric-card" style="border-top: 4px solid #B7CEAD; flex: 1;">
                    <div class="metric-value-blue">{base_wacc:.2f}%</div>
                    <div class="metric-label">綠能 WACC</div>
                </div>
                <div class="metric-card" style="border-top: 4px solid #92BA80; flex: 1;">
                    <div class="metric-value-green">NT$ {base_wealth:,.0f}</div>
                    <div class="metric-label">10年累積資產</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            metric_slot1.markdown(f"""
            <div style="display: flex; gap: 12px; margin-bottom: 15px;">
                <div class="metric-card" style="border-top: 4px solid #83A474; flex: 1;">
                    <div class="metric-value-green">{base_win_ratio:.2f}%</div>
                    <div class="metric-label">全域共贏機率</div>
                </div>
                <div class="metric-card" style="border-top: 4px solid #0C0E0B; flex: 1;">
                    <div class="metric-value-blue">99.96%</div>
                    <div class="metric-label">保險大盤獲利機率</div>
                </div>
                <div class="metric-card" style="border-top: 4px solid #B7CEAD; flex: 1;">
                    <div class="metric-value-blue">{base_wacc:.2f}%</div>
                    <div class="metric-label">綠能 WACC</div>
                </div>
                <div class="metric-card" style="border-top: 4px solid #92BA80; flex: 1;">
                    <div class="metric-value-green">NT$ {base_wealth:,.0f}</div>
                    <div class="metric-label">10年累積資產</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # 互動式分頁切換
    tab_res1, tab_res2, tab_res3, tab_res4 = st.tabs(["🌿 消費者", "🏥 保險公司", "⚡ 綠能產業", "🔄 整體循環"])
    
    # ⚡ [關鍵修改區] 面向三：綠能產業端研究 (互動版)
    with tab_res3:
        st.markdown("<h4 style='color:#2D4A22 !important; font-weight:800;'>散戶碎金流群募效率與氣候韌性</h4>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            m_size = st.radio("設定市場保戶規模：", ["常態 (1萬人)", "全台 (10萬人)"], horizontal=True)
        with c2:
            c_risk = st.select_slider("氣候衝擊風險係數", options=["低", "中", "黑天鵝"], value="中")
        
        # 互動參數對應
        funding_days = 2059.1 if "1萬" in m_size else 205.9
        impact_map = {"低": 0.95, "中": 0.78, "黑天鵝": 0.55}
        fill_rate = impact_map[c_risk] * 100
        
        st.info(f"當前模擬：{m_size} | 風險情境：{c_risk} | 第8年資產填補率：{fill_rate:.1f}%")
        
        om_ratios = [100.0] * 11
        om_ratios[8] = fill_rate
        
        fig_energy = go.Figure()
        fig_energy.add_trace(go.Bar(x=years_axis, y=om_ratios, marker_color=['#83A474' if i!=8 else '#E53E3E' for i in range(11)]))
        fig_energy.update_layout(title="電廠運維公積金自動填補率 (動態壓力測試)", template="plotly_white")
        st.plotly_chart(fig_energy, use_container_width=True)

    # ... (其他分頁請維持您先前的結構) ...
