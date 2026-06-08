import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# ==========================================
# 0. 全局環境配置與指定五色高質感 CSS 注入
# ==========================================
st.set_page_config(
    page_title="EcoStride | 永續金融生態系研究",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化點擊狀態，用於控制首頁卡片背景色
if 'active_node' not in st.session_state:
    st.session_state.active_node = "none"

# 隱藏 Streamlit 預設元素並注入 60-30-10 極簡美學 CSS + 豪華動態交互組件
st.markdown("""
    <style>
    /* 全局背景色與文字色 */
    .stApp {
        background-color: #F5F7F4;
        color: #0C0E0B;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    
    /* 側邊欄改用二次色與細線框分隔 */
    .stSidebar {
        background-color: #B7CEAD !important;
        border-right: 1px solid #83A474 !important;
    }
    
    /* 🎯 頂部毛玻璃導航欄 */
    .navbar-mock {
        background: rgba(245, 247, 244, 0.85);
        backdrop-filter: blur(16px);
        border-bottom: 1px solid #B7CEAD;
        padding: 18px 35px;
        position: sticky; top: 0; z-index: 999;
        display: flex; justify-content: space-between; align-items: center;
        margin: -4.5rem -4rem 2rem -4rem;
    }

    /* 🎯 標籤頁字體放大與選中色塊切換 */
    div[data-testid="stTabs"] button {
        font-size: 18px !important;
        font-weight: 600 !important;
        color: #0C0E0B !important;
        padding: 10px 24px !important;
        border-radius: 8px 8px 0 0 !important;
        background-color: #E6EAE5 !important;
        margin-right: 6px !important;
        border: 1px solid #B7CEAD !important;
        border-bottom: none !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
        background-color: #B7CEAD !important;
        color: #2D4A22 !important;
        font-weight: 800 !important;
        border-top: 3px solid #83A474 !important;
    }
    .stSidebar div[data-testid="stTabs"] [role="tablist"] {
        flex-direction: column !important;
        gap: 6px !important;
    }

    /* 🎯 首頁機制摘要卡片樣式 */
    .vision-card {
        border: 1px solid #B7CEAD; 
        padding: 35px; 
        border-radius: 16px; 
        background-color: #FFFFFF; 
        min-height: 290px;
        transition: all 0.4s ease;
    }
    .vision-card-active {
        background-color: #B7CEAD !important; /* 點選時底色變更 */
        border: 2px solid #83A474 !important;
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(131, 164, 116, 0.2);
    }
    .dark-green-title {
        color: #2D4A22 !important;
        font-size: 19px;
        font-weight: 800;
        margin-bottom: 15px;
    }
    
    /* 🎯 豪華金流動畫 SVG Container */
    .trinity-container {
        display: flex; justify-content: center; align-items: center;
        padding: 20px 0; margin-bottom: 20px; position: relative;
    }
    .money-particle {
        fill: #83A474;
        animation: flow 3s infinite linear;
    }
    @keyframes flow {
        from { offset-distance: 0%; }
        to { offset-distance: 100%; }
    }
    
    /* 放大 Hover 時的浮標文字 (使用 HTML title 屬性的原生樣式難以更改，故採用自定義 Tooltip 模擬) */
    .node-btn {
        cursor: pointer; transition: all 0.3s ease;
    }
    .node-btn:hover {
        transform: scale(1.1); filter: brightness(1.2);
    }
    
    /* 🎯 彭博終端字體指定為 Inter 粗體 */
    .metric-value-green, .metric-value-blue {
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
    }
    
    /* 結構化對比表格 */
    .styled-table {
        width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; background-color: #FFFFFF;
        border-radius: 8px; overflow: hidden;
    }
    .styled-table th { background-color: #83A474; color: #F5F7F4; padding: 14px; text-align: left; }
    .styled-table td { padding: 14px; border-bottom: 1px solid #E2E8F0; color: #0C0E0B; }
    
    /* 行為金融學高級色塊提示區 */
    .alert-card {
        background-color: #FFFFFF; border-left: 5px solid #83A474; padding: 18px; border-radius: 0 12px 12px 0; margin: 15px 0;
    }
    .alert-card-danger {
        background-color: #FFF5F5; border-left: 5px solid #E53E3E; padding: 18px; border-radius: 0 12px 12px 0; margin: 15px 0;
    }

    /* 虛擬手機 Mockup */
    .phone-container {
        border: 10px solid #0C0E0B; border-radius: 36px; padding: 14px; background-color: #0C0E0B; height: 610px; display: flex; flex-direction: column;
    }
    .phone-screen { border-radius: 24px; background-color: #FFFFFF; padding: 22px 16px; flex-grow: 1; overflow-y: auto; color: #0C0E0B; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. 頂部導航欄文字更新
# ==========================================
st.markdown("""
    <div class="navbar-mock">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 6px; height: 26px; background-color: #83A474; border-radius: 3px;"></div>
            <span style="font-size: 20px; font-weight: 800; letter-spacing: 3px; color: #0C0E0B;">ECOSTRIDE</span>
        </div>
        <div style="font-size: 13px; color: #0C0E0B; font-weight: 600; background-color: #B7CEAD; padding: 4px 12px; border-radius: 6px;">
            國立清華大學 金融科技專題研究成果
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 側邊欄 Tabs 導覽選單
# ==========================================
with st.sidebar:
    st.markdown("<div style='padding: 20px 0 10px 0;'><h3 style='margin:0; font-size: 20px;'>專案選單</h3></div>", unsafe_allow_html=True)
    tab_m1, tab_m2, tab_m3, tab_m4 = st.tabs(["🏠 專案首頁", "💡 提案動機", "📱 APP 展示", "📈 研究成果"])
    
    with tab_m1: page = "專案首頁"
    with tab_m2: page = "提案動機與模式介紹"
    with tab_m3: page = "APP 介面展示"
    with tab_m4: page = "相關研究成果"
    
    st.markdown("---")
    st.markdown("""
        <div style='font-size: 12px; line-height: 1.8;'>
        <b style='font-size:14px; color:#2D4A22;'>研究團隊</b><br>
        蔡宜伶 | 計量財務金融學系<br>
        賀舜禹 | 計量財務金融學系<br>
        曾琬甯 | 計量財務金融學系<br><br>
        <b style='font-size:14px; color:#2D4A22;'>指導教授</b><br>
        韓傳祥 教授
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 3. 分頁一：專案首頁 (升級循環動畫與交互控制)
# ==========================================
if page == "專案首頁":
    st.markdown("<div style='padding: 60px 0 40px 0; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 54px; font-weight: 900; color: #5D7A51 !important; letter-spacing: -1.5px; margin-bottom: 20px;'>讓健康行為，成為生產性綠色資本</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 21px; color: #0C0E0B; max-width: 950px; margin: 0 auto 35px auto; line-height: 1.6; font-weight: 600; opacity: 0.9;'>EcoStride：結合行為金融與實體資產代幣化之永續金融生態系模式研究</p>", unsafe_allow_html
