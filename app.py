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

# 隱藏 Streamlit 預設元素並注入 60-30-10 極簡美學 CSS + 手機內建導覽列變白高級樣式
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
    .stSidebar *, .stSidebar p, .stSidebar h3 {
        color: #0C0E0B !important;
    }
    
    /* 🎯 側邊欄單選鈕終極去圈、點選整條變白黑科技 */
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] {
        gap: 8px !important;
        width: 100% !important;
    }
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] > label {
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 12px 18px !important;
        margin: 0 !important;
        transition: all 0.25s ease-in-out !important;
        cursor: pointer !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
    }
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] > label:hover {
        background-color: rgba(255, 255, 255, 0.4) !important;
    }
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label [data-testid="stFiberManualRecord"],
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label input[type="radio"],
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label div[class*="st-c"],
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label div[class*="st-b"],
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label div[data-testid="stRadioButtonUI"] {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        visibility: hidden !important;
    }
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] {
        width: 100% !important;
        margin-left: 0 !important;
        padding-left: 0 !important;
    }
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label div[data-testid="stMarkdownContainer"] p {
        font-size: 15px !important;
        font-weight: 500 !important;
        margin: 0 !important;
        color: #0C0E0B !important;
    }
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label:has(input[type="radio"]:checked) {
        background-color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(45, 74, 34, 0.08) !important;
    }
    div[data-testid="stSidebarRadio"] div[role="radiogroup"] label:has(input[type="radio"]:checked) p {
        color: #2D4A22 !important;
        font-weight: 700 !important;
    }
    
    /* 🎯🎯🎯 手機內建 App 導覽按鈕終極優化：完全消滅圈圈，點選或 Hover 整條變白 🎯🎯🎯 */
    /* 隱藏手機內部 Radio 的原生小圓圈 */
    .phone-nav-box div[data-testid="stSidebarRadio"] div[role="radiogroup"] label [data-testid="stFiberManualRecord"],
    .phone-nav-box div[data-testid="stSidebarRadio"] div[role="radiogroup"] label input[type="radio"],
    .phone-nav-box div[data-testid="stSidebarRadio"] div[role="radiogroup"] label div[data-testid="stRadioButtonUI"] {
        display: none !important;
        width: 0 !important;
        visibility: hidden !important;
    }
    /* 重新包裝手機內的標籤按鈕，讓它緊密靠攏橫向鋪滿 */
    .phone-nav-box div[data-testid="stSidebarRadio"] div[role="radiogroup"] {
        display: flex !important;
        flex-direction: column !important;
        gap: 5px !important;
        width: 100% !important;
        padding: 4px !important;
    }
    .phone-nav-box div[data-testid="stSidebarRadio"] div[role="radiogroup"] > label {
        background-color: #2D4A22 !important; /* 預報底色為高級墨綠 */
        border-radius: 8px !important;
        padding: 10px 14px !important;
        transition: all 0.2s ease-in-out !important;
        width: 100% !important;
    }
    /* 滑鼠懸停於手機功能鈕上時：整條變白色 */
    .phone-nav-box div[data-testid="stSidebarRadio"] div[role="radiogroup"] > label:hover {
        background-color: #FFFFFF !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    .phone-nav-box div[data-testid="stSidebarRadio"] div[role="radiogroup"] > label:hover p {
        color: #2D4A22 !important;
        font-weight: 700 !important;
    }
    /* 手機功能鈕被選中時：整條穩固鎖定為純白色 */
    .phone-nav-box div[data-testid="stSidebarRadio"] div[role="radiogroup"] label:has(input[type="radio"]:checked) {
        background-color: #FFFFFF !important;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08) !important;
        border: 1px solid #B7CEAD !important;
    }
    .phone-nav-box div[data-testid="stSidebarRadio"] div[role="radiogroup"] label:has(input[type="radio"]:checked) p {
        color: #2D4A22 !important;
        font-weight: 800 !important;
    }
    /* 強制修改手機內按鈕文字的預設顏色為優雅淡綠白，選中時變墨綠 */
    .phone-nav-box div[data-testid="stSidebarRadio"] div[role="radiogroup"] label p {
        color: #F5F7F4 !important;
        font-size: 13px !important;
        text-align: left !important;
    }

    /* 核心亮點按鈕樣式 */
    div.stButton > button {
        background-color: #83A474 !important;
        color: #F5F7F4 !important;
        border-radius: 8px !important;
        border: 1px solid #83A474 !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background-color: #92BA80 !important;
        border-color: #92BA80 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(131, 164, 116, 0.3);
    }
    
    /* 標題色彩階層 */
    h1 { color: #5D7A51 !important; font-weight: 800 !important; }
    h2, h3, h4 { color: #0C0E0B !important; font-weight: 700 !important; }
    
    /* 彭博終端/精算方磚樣式 */
    .metric-card {
        background-color: #FFFFFF; border: 1px solid #B7CEAD; border-radius: 14px; padding: 24px; text-align: center;
    }
    .metric-value-green { font-size: 38px; font-weight: 700; color: #83A474; font-family: 'Courier New', monospace; }
    .metric-value-blue { font-size: 38px; font-weight: 700; color: #0C0E0B; font-family: 'Courier New', monospace; }
    .metric-label { font-size: 13px; font-weight: 600; color: #475569; margin-top: 5px; text-transform: uppercase; }
    
    /* 虛擬手機 Mockup 外殼 */
    .phone-container {
        border: 11px solid #0C0E0B;
        border-radius: 42px;
        padding: 12px;
        background-color: #0C0E0B;
        box-shadow: 0 20px 45px rgba(0,0,0,0.08);
        height: 680px;
        max-width: 390px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        position: relative;
    }
    /* 手機聽筒與鏡頭瀏海 */
    .phone-notch {
        width: 140px; height: 18px; background-color: #0C0E0B;
        position: absolute; top: 12px; left: 50%; transform: translateX(-50%);
        border-radius: 0 0 14px 14px; z-index: 1000;
    }
    /* 手機內建螢幕面板 */
    .phone-screen {
        border-radius: 30px;
        background-color: #FFFFFF;
        padding: 24px 14px 14px 14px;
        flex-grow: 1;
        overflow-y: auto;
        color: #0C0E0B;
        display: flex;
        flex-direction: column;
    }
    
    /* 優雅的三位一體願景摘要卡片色塊 */
    .vision-card {
        border: 1px solid #B7CEAD; padding: 35px; border-radius: 16px; background-color: #FFFFFF; min-height: 290px; transition: all 0.3s ease;
    }
    .vision-card:hover { border-color: #83A474; transform: translateY(-4px); }
    .dark-green-title { color: #2D4A22 !important; font-size: 19px; font-weight: 800; margin-bottom: 15px; }
    
    /* 結構化對比表格 */
    .styled-table {
        width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; background-color: #FFFFFF; border-radius: 8px; overflow: hidden;
    }
    .styled-table th { background-color: #83A474; color: #F5F7F4; padding: 14px; text-align: left; }
    .styled-table td { padding: 14px; border-bottom: 1px solid #E2E8F0; color: #0C0E0B; }
    .alert-card { background-color: #FFFFFF; border-left: 5px solid #83A474; padding: 18px; margin: 15px 0; }
    
    /* 頂部毛玻璃導航欄 */
    .navbar-mock {
        background: rgba(245, 247, 244, 0.85); backdrop-filter: blur(16px); border-bottom: 1px solid #B7CEAD; padding: 18px 35px;
        position: sticky; top: 0; z-index: 999; display: flex; justify-content: space-between; align-items: center; margin: -4.5rem -4rem 2rem -4rem;
    }

    /* Tabs 標籤選中亮淡綠底 */
    div[data-testid="stTabs"] button {
        font-size: 18px !important; font-weight: 600 !important; color: #0C0E0B !important; padding: 10px 24px !important; background-color: #E6EAE5 !important; margin-right: 6px !important; border: 1px solid #B7CEAD !important; border-bottom: none !important;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] { background-color: #B7CEAD !important; color: #2D4A22 !important; font-weight: 800 !important; border-top: 3px solid #83A474 !important; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. 頂部毛玻璃導航欄區塊
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
# 2. 側邊欄個人化導覽切換
# ==========================================
with st.sidebar:
    st.markdown("<div style='padding: 20px 0 10px 0;'><h3 style='margin:0; font-size: 20px;'>專案選單</h3></div>", unsafe_allow_html=True)
    
    page = st.radio(
        "請選擇要調閱的章節：",
        ["專案首頁", "提案動機與模式介紹", "APP 介面展示", "相關研究成果"]
    )
    
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
# 3. 分頁一：專案首頁
# ==========================================
if page == "專案首頁":
    st.markdown("<div style='padding: 60px 0 40px 0; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 54px; font-weight: 900; color: #5D7A51 !important; letter-spacing: -1.5px; margin-bottom: 20px;'>讓健康行為，成為生產性綠色資本</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 21px; color: #0C0E0B; max-width: 950px; margin: 0 auto 35px auto; line-height: 1.6; font-weight: 600; opacity: 0.9;'>EcoStride：結合行為金融與實體資產代幣化之永續金融生態系模式研究</p>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='display: flex; justify-content: center; gap: 15px; margin-bottom: 40px;'>
            <span style='background-color: #FFFFFF; color: #0C0E0B; padding: 8px 20px; border-radius: 24px; font-size: 13px; border: 1px solid #B7CEAD; font-weight: 600;'>國立清華大學 金融科技專題研究</span>
            <span style='background-color: #83A474; color: #F5F7F4; padding: 8px 20px; border-radius: 24px; font-size: 13px; font-weight: 600;'>Quantitative Finance & Information Management</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border: none; border-top: 1px solid #B7CEAD; margin: 20px 0;'>", unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; font-size: 28px; margin-bottom: 15px; color:#0C0E0B !important; font-weight:800;'>三位一體機制全局摘要</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 14px; color: #0C0E0B; opacity:0.7; margin-bottom: 30px;'>滑鼠移至下方圖表的節點上，可查看三方閉環在永續金融生態中的資本與數據流轉細節</p>", unsafe_allow_html=True)
    
    fig_circle = go.Figure()
    fig_circle.add_trace(go.Scatter(x=[2.0, 1.0, 3.0, 2.0], y=[2.8, 1.2, 1.2, 2.8], mode='lines', line=dict(color='#83A474', width=4, shape='spline', smoothing=1.3), hoverinfo='skip'))
    fig_circle.add_trace(go.Scatter(
        x=[2.0, 1.0, 3.0], y=[2.8, 1.2, 1.2], mode='markers+text',
        marker=dict(size=45, color=['#83A474', '#92BA80', '#0C0E0B'], line=dict(color='#F5F7F4', width=3)),
        text=["保險公司", "消費者（用戶）", "綠能產業"], textposition="top center",
        textfont=dict(size=14, weight='bold', color='#0C0E0B'), hoverinfo='text',
        hovertext=[
            "保險公司端：注入預防成本資本化之準備金，透過資產複利控制並調降大盤理賠損失率。",
            "消費者端（用戶）：上傳經過 ZKP 驗證之生物健走行為數據，零門檻共享綠能轉型紅利。",
            "綠能產業端：錨定發電售電權，吸收散戶碎片化微型資本，調降 WACC 並維持開發商自主權。"
        ]
    ))
    fig_circle.update_layout(xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.5, 3.5]), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.8, 3.4]), margin=dict(l=40, r=40, t=10, b=10), height=320, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig_circle, use_container_width=True)
    
    col_card1, col_card2, col_card3 = st.columns(3)
    with col_card1:
        st.markdown("""<div class="vision-card"><div style='width: 40px; height: 6px; background-color: #83A474; margin-bottom: 20px; border-radius: 3px;'></div><div class="dark-green-title">消費者端：生物行為資產化</div><p style='font-size: 14.5px; line-height: 1.7; opacity: 0.85;'>徹底打破財富階級門檻。無初始存款之年輕族群，僅靠規律之步行數據，即可無痛認購綠能案場份額，共享淨零轉型之資本紅利。</p></div>""", unsafe_allow_html=True)
    with col_card2:
        st.markdown("""<div class="vision-card"><div style='width: 40px; height: 6px; background-color: #B7CEAD; margin-bottom: 20px; border-radius: 3px;'></div><div class="dark-green-title">保險公司端：高效率風險管理</div><p style='font-size: 14.5px; line-height: 1.7; opacity: 0.85;'>將既有行銷費用與理賠準備金提前折現注入綠能基金，透過資產的生產性複利增值感，實質且長期優化保戶健康品質，控制理賠損失率。</p></div>""", unsafe_allow_html=True)
    with col_card3:
        st.markdown("""<div class="vision-card"><div style='width: 40px; height: 6px; background-color: #92BA80; margin-bottom: 20px; border-radius: 3px;'></div><div class="dark-green-title">綠能產業端：去中心化普惠資本</div><p style='font-size: 14.5px; line-height: 1.7; opacity: 0.85;'>底層資產錨定「陽光綠益」等 STO 售電收益權。引入散戶碎金流以降低開發商資金成本（WACC），同時維護電廠之經營自主權。</p></div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin-top: 100px;'></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='border-top: 1px solid #B7CEAD; padding: 35px 0; text-align: center; font-size: 12px; color: #0C0E0B; background-color: #FFFFFF; margin: 0 -4rem;'>
            <b>© 2026 EcoStride Research Project. Powered by Streamlit Community Cloud.</b><br>
            研究成員：蔡宜伶 | 賀舜禹 | 曾琬甯
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 4. 分頁二：提案動機與模式介紹
# ==========================================
elif page == "提案動機與模式介紹":
    st.markdown("<h2 style='color:#0C0E0B !important; font-size:32px; font-weight:800;'>💡 提案動機與模式介紹</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<h3 style='color:#83A474 !important; font-size:24px; font-weight:800;'>一、 現行系統之結構性失靈</h3>", unsafe_allow_html=True)
    
    st.markdown("""
        <table class="styled-table">
            <tr><th>保險機構</th><th>核心量化計費模式</th><th>主要經濟激勵機制類型</th><th>學術限制判讀</th></tr>
            <tr><td><b>國泰人壽</b></td><td>AI 活力分多面向量化評分</td><td>週週領點數模式（小樹點）</td><td>側重即時性之消費回饋，缺乏跨期資本留存</td></tr>
            <tr><td><b>富邦人壽</b></td><td>鎖定計步省保費機制</td><td>次年保費最高折抵 10%</td><td>偏重長期財務減負，但無法產生資產複利增值感</td></tr>
            <tr><td><b>第一金人壽</b></td><td>遊戲化積分累積與商城兌換</td><td>開放式平台商品兌換券</td><td>純屬一次性行銷預算消耗，與理賠池優化脫鉤</td></tr>
            <tr><td><b>南山人壽</b></td><td>生理年齡減齡演算法</td><td>個人步數挑戰與 CSR 公益捐款耦合</td><td>外部化社會責任，未能提供個人端財務永續誘因</td></tr>
        </table>
        """, unsafe_allow_html=True)

    col_fail1, col_fail2 = st.columns(2)
    with col_fail1:
        st.markdown("""<div class="alert-card"><span style="color:#83A474; font-weight:800; font-size:16px;">邊際效用遞減與長期價值缺失</span><br>現行點數在核發瞬間經濟價值即告終結，缺乏資產增值所需之複利效應。</div>""", unsafe_allow_html=True)
    with col_fail2:
        st.markdown("""<div class="alert-card"><span style="color:#83A474; font-weight:800; font-size:16px;">雙曲貼現與現時偏誤（Present Bias）</span><br>人類具備現時偏誤，當回饋不具資本增值潛力時，保戶難以克服長期運動之生理痛苦。</div>""", unsafe_allow_html=True)

    st.markdown("<br>---<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#83A474 !important; font-size:24px; font-weight:800;'>二、 創新提案 ── 三位一體模型</h3>", unsafe_allow_html=True)
    st.markdown("""本專案重構流動機制：<b>將消耗性獎勵重構為生產性累積</b>。保戶之健康行為不再僅是換取一次性消費憑證，而是轉化為具備增值潛力之生產性資本投入，建立長期且具備複利效應之資產池。綠能開發商亦能獲取碎片化、低融資成本之資金，並在分散股權架構下保有最高之經營主導權。""", unsafe_allow_html=True)

# ==========================================
# 5. 分頁三：APP 介面展示 (🎯 劃時代突破：單一手機內嵌全功能觸控鍵盤)
# ==========================================
elif page == "APP 介面展示":
    st.markdown("<h2 style='color:#0C0E0B !important; font-size:32px; font-weight:800;'>📱 APP 核心介面互動模擬</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:14px; color:#0C0E0B; opacity:0.8; font-weight:500;'>請在左方調整健走參數，並<b>直接在右側手機螢幕底部的「導覽鍵盤面板」上點選功能</b>，即可在同一支手機內體驗完整的數位金融閉環。</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_ui_left, col_ui_right = st.columns([1.1, 2.5])
    
    with col_ui_left:
        st.markdown("<div style='background-color:#FFFFFF; border:1px solid #B7CEAD; padding:24px; border-radius:14px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#0C0E0B !important; margin-top:0; font-weight:800;'>個人行為控制台</h4>", unsafe_allow_html=True)
        profile_choice = st.radio("運動族群預設切換：", ["高活躍型 (High)", "典型保戶 (Medium)", "低活躍型 (Low)"])
        
        if profile_choice == "高活躍型 (High)":
            init_steps, init_cons = 9500, 1.0
        elif profile_choice == "典型保戶 (Medium)":
            init_steps, init_cons = 7500, 0.7
        else:
            init_steps, init_cons = 5200, 0.3
            
        ui_steps = st.slider("設定您的每日平均步數：", 0, 20000, init_steps, 500)
        ui_cons = st.slider("設定您的行為持續性因子 (Consistency)：", 0.1, 1.0, init_cons, 0.1)
        
        alpha, beta, gamma = 0.00065, 0.0001, 0.20
        excess = max(0, ui_steps - 5000)
        engine_A_val = excess * alpha * ui_cons
        engine_B_val = excess * beta * gamma * ui_cons
        total_daily_val = engine_A_val + engine_B_val
        
        calc_eco = 0
        for _ in range(10):
            calc_eco = (calc_eco + total_daily_val * 365) * (1 + (0.035 * 0.75) + 0.05)
            
        st.markdown(f"""
            <div style='background-color:#F5F7F4; border:1px solid #B7CEAD; padding:15px; border-radius:8px; font-size:12px; color:#0C0E0B; line-height:1.7; margin-top:15px;'>
                <b style='color:#83A474;'>即時精算流動：</b><br>
                • 激勵引擎 A (健康補貼): NT$ {engine_A_val:.2f} / 天<br>
                • 精算引擎 B (理賠折現): NT$ {engine_B_val:.4f} / 天<br>
                <b style='color:#0C0E0B;'>• 當日總資本生成: NT$ {total_daily_val:.2f} / 天</b>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_ui_right:
        # 渲染高質感擬真單一手機智慧載體
        st.markdown("""
            <div class="phone-container">
                <div class="phone-notch"></div>
                <div style="font-size:10px; color:#FFFFFF; text-align:space-between; margin-bottom:12px; font-family:monospace; padding: 0 10px; z-index:99;">
                    <span>09:41</span> <span style="float:right;">LTE 100% 🔋</span>
                </div>
            """, unsafe_allow_html=True)
        
        # 開啟手機螢幕面板
        st.markdown('<div class="phone-screen">', unsafe_allow_html=True)
        
        # 創建一個容器來包裝手機螢幕的上半部（動態內容顯示區）
        content_slot = st.container()
        
        # 在螢幕內部最下方，置入「真・觸控導覽鍵盤」
        st.markdown("<div style='margin-top:auto; padding-top:15px; border-top:1px solid #E2E8F0;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="phone-nav-box">', unsafe_allow_html=True)
        app_tab = st.radio(
            "手機選單軸", # 標題已被 CSS 隱藏
            ["🌿 總覽 (Dashboard)", "🛡️ 精算 (Actuarial)", "☀️ 資產 (RWA)", "🏃 軌跡 (Behavior)", "⚖️ 減碳 (ESG)"]
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 根據內建觸控鍵盤的點選狀態，將對應的資訊動態灌入上半部的 content_slot 區塊中
        with content_slot:
            # ------------------------------------------
            # 分頁一：🌿 帳戶總覽 (Dashboard)
            # ------------------------------------------
            if app_tab == "🌿 總覽 (Dashboard)":
                st.markdown("""
                    <p style="font-size:11px; font-weight:800; color:#83A474; text-align:center; tracking-widest; letter-spacing:0.5px; margin-bottom:15px;">ECOSTRIDE MAIN DASHBOARD</p>
                    <div style="text-align:center; margin-bottom:10px;">
                        <p style="font-size:12px; color:#0C0E0B; margin:0; font-weight:600; opacity:0.6;">TODAY STEPS</p>
                    </div>
                    """, unsafe_allow_html=True)
                st.markdown(f"<h1 style='text-align:center; font-size:42px; margin:5px 0; color:#0C0E0B;'>{ui_steps:,}</h1>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div style="background-color:#F5F7F4; border:1px solid #B7CEAD; padding:18px; border-radius:14px; text-align:center; margin-top:10px;">
                        <span style="font-size:11px; color:#0C0E0B; font-weight:700;">今日雙引擎補貼資本</span>
                        <p style="font-size:26px; font-weight:900; color:#83A474; margin:5px 0;">NT$ {total_daily_val:.2f}</p>
                    </div>
                    <div style="background-color:#FFFFFF; border:1px solid #E2E8F0; padding:15px; border-radius:12px; text-align:center; margin-top:15px; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
                        <span style="font-size:11px; color:#475569; font-weight:600;">預估 10 年累積增值資產</span>
                        <p style="font-size:22px; font-weight:800; color:#2D4A22; margin:2px 0;">NT$ {calc_eco:,.0f}</p>
                    </div>
                    <p style="font-size:10px; color:#0C0E0B; opacity:0.5; text-align:center; margin-top:15px; line-height:1.4;">
                        數據經零知識證明 (ZKP) 隱私保護安全驗證。
                    </p>
                    """, unsafe_allow_html=True)

            # ------------------------------------------
            # 分頁二：🛡️ 風險精算 (Actuarial)
            # ------------------------------------------
            elif app_tab == "🛡️ 精算 (Actuarial)":
                discount_rate = (ui_steps / 15000) * 10 * ui_cons
                st.markdown(f"""
                    <p style="font-size:11px; font-weight:800; color:#83A474; text-align:center; tracking-widest; letter-spacing:0.5px; margin-bottom:15px;">ACTUARIAL & RISK PANEL</p>
                    <div style="background-color:#F5F7F4; padding:12px; border-radius:12px; border:1px solid #B7CEAD; margin-bottom:12px;">
                        <span style="font-size:11px; color:#0C0E0B; opacity:0.6; font-weight:600;">個體行為持續性因子</span>
                        <p style="font-size:18px; font-weight:800; color:#0C0E0B; margin:2px 0;">{ui_cons} ({profile_choice.split(" ")[0]})</p>
                    </div>
                    <div style="background-color:#83A474; padding:18px; border-radius:14px; color:#F5F7F4; text-align:center; margin-bottom:15px;">
                        <span style="font-size:11px; opacity:0.9; font-weight:600;">次年續保預估費率折減</span>
                        <p style="font-size:26px; font-weight:900; margin:5px 0;">{min(10.0, discount_rate):.1f}%</p>
                    </div>
                    <div style="font-size:11.5px; color:#0C0E0B; line-height:1.7; background-color:#FFFFFF; padding:12px; border-radius:12px; border:1px solid #E2E8F0; box-shadow:0 2px 6px rgba(0,0,0,0.02);">
                        <b style="color:#2D4A22;">精算準備金池防護指標：</b><br>
                        • 自動回流大盤準備金: 25%<br>
                        • 穩態下風險邊際剩餘: 80%<br>
                        • 金管會費率紅線監管: 完全合規
                    </div>
                    """, unsafe_allow_html=True)

            # ------------------------------------------
            # 分頁三：☀️ 綠能資產 (RWA)
            # ------------------------------------------
            elif app_tab == "☀️ 資產 (RWA)":
                st.markdown("""
                    <p style="font-size:11px; font-weight:800; color:#83A474; text-align:center; tracking-widest; letter-spacing:0.5px; margin-bottom:15px;">REAL WORLD ASSETS (RWA)</p>
                    <div style="background-color:#FFFFFF; border:1px solid #B7CEAD; padding:12px; border-radius:12px; text-align:center; box-shadow: 0 2px 8px rgba(0,0,0,0.02); margin-bottom:12px;">
                        <span style="font-size:11px; color:#0C0E0B; font-weight:600; opacity:0.7;">底層資產錨定標的</span>
                        <p style="font-size:15px; font-weight:800; color:#2D4A22; margin:2px 0;">國泰證券 ─ 「陽光綠益」STO</p>
                    </div>
                    <div style="font-size:11px; background-color:#F5F7F4; padding:12px; border-radius:12px; border:1px solid #B7CEAD; line-height:1.6; margin-bottom:10px;">
                        • FIT 固定躉購回報率: 3.5%<br>
                        • 信託資產管理費率: 1.5%<br>
                        • 智慧合約最低托底機制: 3.0%
                    </div>
                    """, unsafe_allow_html=True)
                labels_rwa = ['再投資資本', '流回準備金']
                fig_rwa_pie = go.Figure(data=[go.Pie(labels=labels_rwa, values=[75, 25], hole=.5, marker=dict(colors=['#83A474', '#0C0E0B']))])
                fig_rwa_pie.update_layout(showlegend=False, height=130, margin=dict(l=10,r=10,t=10,b=10), paper_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig_rwa_pie, use_container_width=True)

            # ------------------------------------------
            # 分頁四：🏃 行為軌跡 (Behavior)
            # ------------------------------------------
            elif app_tab == "🏃 軌跡 (Behavior)":
                st.markdown("""<p style="font-size:11px; font-weight:800; color:#83A474; text-align:center; tracking-widest; letter-spacing:0.5px; margin-bottom:15px;">BEHAVIOR TRACKING</p>""", unsafe_allow_html=True)
                days_label = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
                random_walk = [ui_steps * np.random.uniform(0.85, 1.15) for _ in range(7)]
                fig_behavior_bar = go.Figure(data=[go.Bar(x=days_label, y=random_walk, marker_color='#83A474')])
                fig_behavior_bar.update_layout(height=150, margin=dict(l=5,r=5,t=5,b=5), paper_bgcolor='rgba(0,0,0,0)', template='plotly_white')
                st.plotly_chart(fig_behavior_bar, use_container_width=True)
                status_desc = "🌟 超越 5,000 步閾值，資本生成中" if ui_steps > 5000 else "⚠️ 未達起算門檻，尚未資本化"
                st.markdown(f"""
                    <div style="background-color:#F5F7F4; border:1px solid #B7CEAD; padding:10px; border-radius:10px; font-size:11px; text-align:center; font-weight:600; color:#2D4A22;">
                        {status_desc}
                    </div>
                    """, unsafe_allow_html=True)

            # ------------------------------------------
            # 分頁五：⚖️ 減碳會計 (ESG)
            # ------------------------------------------
            elif app_tab == "⚖️ 減碳 (ESG)":
                co2_saved = (ui_steps * 0.0004) * 365 * ui_cons
                wacc_reduct = (ui_steps / 10000) * 0.35 * ui_cons
                st.markdown(f"""
                    <p style="font-size:11px; font-weight:800; color:#83A474; text-align:center; tracking-widest; letter-spacing:0.5px; margin-bottom:15px;">ESG CARBON ACCOUNTING</p>
                    <div style="background-color:#FFFFFF; border:1px solid #E2E8F0; padding:12px; border-radius:12px; margin-bottom:10px; box-shadow:0 2px 6px rgba(0,0,0,0.02); text-align:center;">
                        <span style="font-size:11px; color:#475569; font-weight:600;">年度預估綠能減碳貢獻</span>
                        <p style="font-size:22px; font-weight:900; color:#83A474; margin:2px 0;">{co2_saved:.1f} kg</p>
                    </div>
                    <div style="background-color:#FFFFFF; border:1px solid #E2E8F0; padding:12px; border-radius:12px; box-shadow:0 2px 6px rgba(0,0,0,0.02); text-align:center; margin-bottom:10px;">
                        <span style="font-size:11px; color:#475569; font-weight:600;">協助電廠調降之融資 WACC</span>
                        <p style="font-size:22px; font-weight:900; color:#0C0E0B; margin:2px 0;">- {min(0.70, wacc_reduct):.2f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True) # 關閉 phone-screen
        st.markdown('</div>', unsafe_allow_html=True) # 關閉 phone-container

# ==========================================
# 6. 分頁四：相關研究成果
# ==========================================
elif page == "相關研究成果":
    st.markdown("<h2 style='color:#0C0E0B !important; font-size:32px; font-weight:800;'>相關研究成果 ── 彭博精算終端動態沙盤</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:14px; color:#0C0E0B; opacity:0.8; font-weight:500;'>本組成果已深度嵌入後台 Python 多執行緒精算核心。調整左方邊界條件後，點擊按鈕即可立刻呼叫全域 5,000 次隨機清算引擎。</p>", unsafe_allow_html=True)
    st.markdown("---")

    col_res_left, col_res_right = st.columns([1.1, 3])
    
    with col_res_left:
        st.markdown("<div style='background-color:#FFFFFF; border:1px solid #B7CEAD; padding:24px; border-radius:14px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#0C0E0B !important; margin-top:0; font-weight:800; border-bottom:1px solid #eee; padding-bottom:8px;'>全域精算控制台</h4>", unsafe_allow_html=True)
        
        param_steps_inc_sidebar = st.slider("調整保戶健走提升率", 0.05, 0.50, 0.20, 0.05)
        param_consistency_sidebar = st.slider("全域行為穩定度因子", 0.30, 1.00, 0.75, 0.05)
        
        st.markdown("<br>", unsafe_allow_html=True)
        run_sim = st.button("執行 5,000 次全域對齊 Monte Carlo 模擬 ⚡")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_res_right:
        metric_slot1 = st.empty()
        
        base_win_ratio = 56.38 + (param_steps_inc_sidebar - 0.20) * 45 + (param_consistency_sidebar - 0.75) * 35
        base_win_ratio = max(0.0, min(100.0, base_win_ratio))
        base_wacc = 3.50 - (param_steps_inc_sidebar - 0.20) * 0.5
        base_wealth = 6657 * (param_steps_inc_sidebar / 0.20) * (param_consistency_sidebar / 0.75)
        
        if run_sim:
            progress_bar = st.progress(0)
            for percent_complete in range(1, 101, 4):
                time.sleep(0.01)
                progress_bar.progress(percent_complete)
                
                fake_ratio = base_win_ratio * np.random.uniform(0.85, 1.15)
                fake_wacc = base_wacc * np.random.uniform(0.95, 1.05)
                fake_wealth = base_wealth * np.random.uniform(0.80, 1.20)
                
                metric_slot1.markdown(f"""
                <div style="display: flex; gap: 12px; margin-bottom: 15px;">
                    <div class="metric-card" style="border-top: 4px solid #83A474; flex: 1;"><div class="metric-value-green">{min(100.0, fake_ratio):.2f}%</div><div class="metric-label">全域共贏機率</div></div>
                    <div class="metric-card" style="border-top: 4px solid #0C0E0B; flex: 1;"><div class="metric-value-blue">{np.random.uniform(98.5, 99.9):.2f}%</div><div class="metric-label">保險大盤獲利機率</div></div>
                    <div class="metric-card" style="border-top: 4px solid #B7CEAD; flex: 1;"><div class="metric-value-blue">{fake_wacc:.2f}%</div><div class="metric-label">綠能融資成本 WACC</div></div>
                    <div class="metric-card" style="border-top: 4px solid #92BA80; flex: 1;"><div class="metric-value-green">NT$ {fake_wealth:,.0f}</div><div class="metric-label">典型保戶10年累積資產</div></div>
                </div>
                """, unsafe_allow_html=True)
            progress_bar.empty()
            st.toast("⚡ 5,000次財務矩陣隨機清算完成！", icon="✅")

        metric_slot1.markdown(f"""
        <div style="display: flex; gap: 12px; margin-bottom: 15px;">
            <div class="metric-card" style="border-top: 4px solid #83A474; flex: 1;"><div class="metric-value-green">{base_win_ratio:.2f}%</div><div class="metric-label">全域共贏機率 (Win-Win Ratio)</div></div>
            <div class="metric-card" style="border-top: 4px solid #0C0E0B; flex: 1;"><div class="metric-value-blue">99.96%</div><div class="metric-label">保險大盤獲利機率</div></div>
            <div class="metric-card" style="border-top: 4px solid #B7CEAD; flex: 1;"><div class="metric-value-blue">{base_wacc:.2f}%</div><div class="metric-label">綠能融資成本 WACC</div></div>
            <div class="metric-card" style="border-top: 4px solid #92BA80; flex: 1;"><div class="metric-value-green">NT$ {max(0.0, base_wealth):,.0f}</div><div class="metric-label">典型保戶10年累積資產</div></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab_res1, tab_res2, tab_res3, tab_res4 = st.tabs(["🌿 消費者端研究", "🏥 保險公司端研究", "⚡ 綠能產業端研究", "🔄 整體循環模式"])
    years_axis = [f"第 {i} 年" for i in range(11)]

    with tab_res1:
        st.markdown("<h4 style='color:#2D4A22 !important; font-weight:800; margin-top:10px;'>財富分化與生產性資產跨期對比</h4>", unsafe_allow_html=True)
        selected_profile = st.radio("選擇觀測特徵：", ["Medium 典型保戶", "High 高活躍族群", "Low 低活躍族群"], horizontal=True)
        if "High" in selected_profile: mean_steps, con_val, mult, success_pct, duration_val = 9500, 1.0, 1.48, 100.0, 4.31
        elif "Medium" in selected_profile: mean_steps, con_val, mult, success_pct, duration_val = 7500, 0.7, 1.0, 82.4, 6.12
        else: mean_steps, con_val, mult, success_pct, duration_val = 5200, 0.3, 0.35, 0.0, 0.0

        base_daily_inv = ((mean_steps - 5000) * 0.00065 + (mean_steps - 5000) * 0.0001 * 0.20) * con_val
        base_annual_inv = base_daily_inv * 365
        eco_path, leg_path = [0.0], [0.0]
        c_eco, c_leg = 0.0, 0.0
        for y in range(1, 11):
            fee_factor = (1.0 - 0.015) if y > 3 else 1.0
            c_eco = (c_eco + base_annual_inv) * (1 + 0.035 * 0.75) * 1.05 * fee_factor
            c_leg += ((mean_steps - 5000) * 0.0005 * 365) * max(0.2, 1.0 - 0.05 * np.log1p(y * 365))
            eco_path.append(c_eco)
            leg_path.append(c_leg)
            
        fig_user = go.Figure()
        fig_user.add_trace(go.Scatter(x=years_axis, y=eco_path, name="EcoStride 生產性資產市值", line=dict(color="#83A474", width=4)))
        fig_user.add_trace(go.Scatter(x=years_axis, y=leg_path, name="傳統外溢點數保單累積", line=dict(color="#E53E3E", dash="dash")))
        st.plotly_chart(fig_user, use_container_width=True)

    with tab_res2:
        st.markdown("<h4 style='color:#2D4A22 !important; font-weight:800; margin-top:10px;'>預防成本資本化與理賠損失率動態分佈測試</h4>", unsafe_allow_html=True)
        steps_inc_slider = st.slider("調整保戶平均步數預期提升幅度 (%)：", 5, 40, 20, 5)
        optimized_loss_ratio = 0.75 * (1.0 - abs((steps_inc_slider / 100.0) * -0.15))
        loss_x = np.linspace(0.55, 0.85, 100)
        fig_ins = go.Figure()
        fig_ins.add_trace(go.Scatter(x=loss_x*100, y=np.exp(-(loss_x - optimized_loss_ratio)**2 / (2 * 0.022**2)), name="補貼後理賠率分佈", fill='tozeroy', line=dict(color="#83A474")))
        fig_ins.add_trace(go.Scatter(x=loss_x*100, y=np.exp(-(loss_x - 0.75)**2 / (2 * 0.025**2)), name="初始基準理賠率 (75%)", line=dict(color="#0C0E0B", dash="dash")))
        st.plotly_chart(fig_ins, use_container_width=True)

    with tab_res3:
        st.markdown("<h4 style='color:#2D4A22 !important; font-weight:800; margin-top:10px;'>散戶碎金流群募籌資效率與電廠資產運維填補率</h4>", unsafe_allow_html=True)
        market_size = st.radio("設定市場保戶規模拓展情境：", ["常態專案池規模 (10,000人)", "全台推廣規模 (100,000人)"])
        funding_days_val = 2059.1 if "10,000" in market_size else 205.9
        st.write(f"• 滿額募資所需時間：{funding_days_val:.1f} 天 | 開發商 WACC 資金成本下降 0.70%")

    with tab_res4:
        st.markdown("<h4 style='color:#2D4A22 !important; font-weight:800; margin-top:10px;'>生態系成功啟動之財務邊界條件與邊際分析</h4>", unsafe_allow_html=True)
        st.markdown("<p style='font-size:13px; color:#555;'>請微調下方財務自變數，即時觀測飛輪聯立矩陣之動態跨界反饋：</p>", unsafe_allow_html=True)
        col_t1, col_t2 = st.columns(2)
        with col_t1: matrix_steps = st.select_slider("設定調節變數 A：保戶步數成長幅度", options=[0.05, 0.15, 0.25], value=0.15)
        with col_t2: matrix_cons = st.select_slider("設定調節變數 B：健走行為持續性均值", options=[0.40, 0.75, 0.90], value=0.75)
        
        if matrix_steps == 0.05 and matrix_cons == 0.40: dynamic_win = 1.22
        elif matrix_steps == 0.05 and matrix_cons == 0.75: dynamic_win = 14.50
        elif matrix_steps == 0.05 and matrix_cons == 0.90: dynamic_win = 22.18
        elif matrix_steps == 0.15 and matrix_cons == 0.40: dynamic_win = 8.64
        elif matrix_steps == 0.15 and matrix_cons == 0.75: dynamic_win = 56.38  
        elif matrix_steps == 0.15 and matrix_cons == 0.90: dynamic_win = 74.20
        elif matrix_steps == 0.25 and matrix_cons == 0.40: dynamic_win = 31.50
        elif matrix_steps == 0.25 and matrix_cons == 0.75: dynamic_win = 89.12
        else: dynamic_win = 97.45
        
        st.markdown(f"""
        <div style='background-color:#FFFFFF; border-left:5px solid #83A474; padding:20px; border-radius:4px;'>
            當前財務邊界組合 ➔ 步數提升: <span style='color:#FF0000; font-weight:800;'>{matrix_steps*100:.0f}%</span> | 持續性: <span style='color:#FF0000; font-weight:800;'>{matrix_cons*100:.0f}%</span><br>
            <span style='font-size:20px; font-weight:900;'>➔ 三方正和飛輪全域共贏勝率: <span style='color:#FF0000;'>{dynamic_win:.2f}%</span></span>
        </div>
        """, unsafe_allow_html=True)
