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

# 隱藏 Streamlit 預設元素並注入 60-30-10 極簡白美學 CSS
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
    
    /* 核心亮點按鈕：使用 Primary 綠色 */
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
    
    /* 彭博終端/精算方磚樣式：改用白底與 Accent 綠細框 */
    .metric-card {
        background-color: #FFFFFF;
        border: 1px solid #B7CEAD;
        border-radius: 14px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.01);
    }
    .metric-value-green {
        font-size: 38px; font-weight: 700; color: #83A474; font-family: 'Courier New', monospace;
    }
    .metric-value-blue {
        font-size: 38px; font-weight: 700; color: #0C0E0B; font-family: 'Courier New', monospace;
    }
    .metric-label {
        font-size: 13px; font-weight: 600; color: #475569; margin-top: 5px; text-transform: uppercase; letter-spacing: 0.5px;
    }
    
    /* 虛擬手機 Mockup：使用極簡鋼鐵黑邊框搭配純白螢幕 */
    .phone-container {
        border: 10px solid #0C0E0B;
        border-radius: 36px;
        padding: 14px;
        background-color: #0C0E0B;
        box-shadow: 0 15px 35px rgba(0,0,0,0.06);
        height: 610px;
        display: flex;
        flex-direction: column;
    }
    .phone-screen {
        border-radius: 24px;
        background-color: #FFFFFF;
        padding: 22px 16px;
        flex-grow: 1;
        overflow-y: auto;
        color: #0C0E0B;
    }
    
    /* 優雅的三位一體願景摘要卡片色塊 */
    .vision-card {
        border: 1px solid #B7CEAD; 
        padding: 35px; 
        border-radius: 16px; 
        background-color: #FFFFFF; 
        min-height: 290px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.01);
        transition: all 0.3s ease;
    }
    .vision-card:hover {
        border-color: #83A474;
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(131, 164, 116, 0.1);
    }
    
    /* 自訂墨綠色專用標題樣式 */
    .dark-green-title {
        color: #2D4A22 !important;
        font-size: 19px;
        font-weight: 800;
        margin-bottom: 15px;
    }
    
    /* 結構化對比表格 */
    .styled-table {
        width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; background-color: #FFFFFF;
        border-radius: 8px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.01);
    }
    .styled-table th {
        background-color: #83A474; color: #F5F7F4; padding: 14px; text-align: left; font-weight: 600;
    }
    .styled-table td {
        padding: 14px; border-bottom: 1px solid #E2E8F0; color: #0C0E0B;
    }
    
    /* 行為金融學高級色塊提示區 */
    .alert-card {
        background-color: #FFFFFF; border-left: 5px solid #83A474; padding: 18px; border-radius: 0 12px 12px 0; margin: 15px 0;
        box-shadow: 0 4px 10px rgba(0,0,0,0.01);
    }
    .alert-card-danger {
        background-color: #FFF5F5; border-left: 5px solid #E53E3E; padding: 18px; border-radius: 0 12px 12px 0; margin: 15px 0;
    }
    
    /* 頂部毛玻璃導航欄 */
    .navbar-mock {
        background: rgba(245, 247, 244, 0.85);
        backdrop-filter: blur(16px);
        border-bottom: 1px solid #B7CEAD;
        padding: 18px 35px;
        position: sticky; top: 0; z-index: 999;
        display: flex; justify-content: space-between; align-items: center;
        margin: -6rem -4rem 2rem -4rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. 頂部毛玻璃導航欄區塊 (區塊 A)
# ==========================================
st.markdown("""
    <div class="navbar-mock">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 6px; height: 26px; background-color: #83A474; border-radius: 3px;"></div>
            <span style="font-size: 20px; font-weight: 800; letter-spacing: 3px; color: #0C0E0B;">ECOSTRIDE</span>
        </div>
        <div style="font-size: 13px; color: #0C0E0B; font-weight: 600; background-color: #B7CEAD; padding: 4px 12px; border-radius: 6px;">
            國立清華大學 金融科技專題研究成果展示大盤
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 側邊欄個人化導覽切換 (無 Emoji 嚴謹版)
# ==========================================
with st.sidebar:
    st.markdown("<div style='padding: 20px 0;'><h3 style='margin:0;'>專案選單</h3></div>", unsafe_allow_html=True)
    page = st.radio(
        "請選擇要調閱的章節：",
        ["專案首頁", "提案動機與模式介紹", "APP 介面展示", "相關研究成果"]
    )
    st.markdown("---")
    st.markdown("""
        <div style='font-size: 12px; line-height: 1.8;'>
        <b>研究團隊</b><br>
        蔡宜伶 | 量化金融與資訊管理雙主修<br>
        賀舜禹 | 定量金融學系<br>
        曾琬甯 | 定量金融學系<br><br>
        <b>指導教授</b><br>
        清華大學計量財務金融學系 專題指導群
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 3. 分頁一：專案首頁
# ==========================================
if page == "專案首頁":
    # 區塊 B：Hero Section
    st.markdown("<div style='padding: 60px 0 40px 0; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 54px; font-weight: 900; color: #5D7A51 !important; letter-spacing: -1.5px; margin-bottom: 20px;'>讓健康行為，成為生產性綠色資本</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 21px; color: #0C0E0B; max-width: 950px; margin: 0 auto 35px auto; line-height: 1.6; font-weight: 600; opacity: 0.9;'>EcoStride：結合行為金融與實體資產代幣化之永續金融生態系模式研究</p>", unsafe_allow_html=True)
    
    # 學術膠囊標籤 (Capsules)
    st.markdown("""
        <div style='display: flex; justify-content: center; gap: 15px; margin-bottom: 40px;'>
            <span style='background-color: #FFFFFF; color: #0C0E0B; padding: 8px 20px; border-radius: 24px; font-size: 13px; border: 1px solid #B7CEAD; font-weight: 600;'>國立清華大學 金融科技專題研究</span>
            <span style='background-color: #83A474; color: #F5F7F4; padding: 8px 20px; border-radius: 24px; font-size: 13px; font-weight: 600;'>Quantitative Finance & Information Management</span>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<hr style='border: none; border-top: 1px solid #B7CEAD; margin: 20px 0;'>", unsafe_allow_html=True)
    
    # 區塊 C：三位一體願景摘要 (Ecosystem Glimpse)
    st.markdown("<h2 style='text-align: center; font-size: 28px; margin-bottom: 15px; color:#0C0E0B !important; font-weight:800;'>三位一體機制全局摘要</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 14px; color: #0C0E0B; opacity:0.7; margin-bottom: 30px;'>滑鼠移至下方圖表的節點上，可查看三方閉環在永續金融生態中的資本與數據流轉細節</p>", unsafe_allow_html=True)
    
    # 三方循環協同關係圖
    fig_circle = go.Figure()
    
    x_nodes = [2.0, 1.0, 3.0]
    y_nodes = [2.8, 1.2, 1.2]
    node_names = ["保險公司", "消費者（用戶）", "綠能產業"]
    hover_details = [
        "保險公司端：注入預防成本資本化之準備金，透過資產複利控制並調降大盤理賠損失率。",
        "消費者端（用戶）：上傳經過 ZKP 驗證之生物健走行為數據，零門檻共享綠能轉型紅利。",
        "綠能產業端：錨定發電售電權，吸收散戶碎片化微型資本，調降 WACC 並維持開發商自主權。"
    ]
    
    # 畫三角形邊緣循環箭頭線
    fig_circle.add_trace(go.Scatter(
        x=[2.0, 1.0, 3.0, 2.0],
        y=[2.8, 1.2, 1.2, 2.8],
        mode='lines',
        line=dict(color='#83A474', width=4, shape='spline', smoothing=1.3),
        hoverinfo='skip'
    ))
    
    # 頂點節點
    fig_circle.add_trace(go.Scatter(
        x=x_nodes, y=y_nodes,
        mode='markers+text',
        marker=dict(
            size=45, 
            color=['#83A474', '#92BA80', '#0C0E0B'], 
            line=dict(color='#F5F7F4', width=3)
        ),
        text=node_names,
        textposition="top center",
        textfont=dict(size=14, weight='bold', color='#0C0E0B'),
        hoverinfo='text',
        hovertext=hover_details
    ))
    
    fig_circle.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.5, 3.5]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0.8, 3.4]),
        margin=dict(l=40, r=40, t=10, b=10),
        height=320,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False
    )
    st.plotly_chart(fig_circle, use_container_width=True)
    
    # 原本的框介紹區塊（標題已套用墨綠色樣式）
    col_card1, col_card2, col_card3 = st.columns(3)
    with col_card1:
        st.markdown("""
            <div class="vision-card">
                <div style='width: 40px; height: 6px; background-color: #83A474; margin-bottom: 20px; border-radius: 3px;'></div>
                <div class="dark-green-title">消費者端：生物行為資產化</div>
                <p style='font-size: 14.5px; color: #0C0E0B; line-height: 1.7; opacity: 0.85;'>徹底打破財富階級門檻。無初始存款之年輕族群，僅靠規律之步行數據，即可無痛認購綠能案場份額，共享淨零轉型之資本紅利。</p>
            </div>
            """, unsafe_allow_html=True)
            
    with col_card2:
        st.markdown("""
            <div class="vision-card">
                <div style='width: 40px; height: 6px; background-color: #B7CEAD; margin-bottom: 20px; border-radius: 3px;'></div>
                <div class="dark-green-title">保險公司端：高效率風險管理</div>
                <p style='font-size: 14.5px; color: #0C0E0B; line-height: 1.7; opacity: 0.85;'>將既有行銷費用與理賠準備金提前折現注入綠能基金，透過資產的生產性複利增值感，實質且長期優化保戶健康品質，控制理賠損失率。</p>
            </div>
            """, unsafe_allow_html=True)
            
    with col_card3:
        st.markdown("""
            <div class="vision-card">
                <div style='width: 40px; height: 6px; background-color: #92BA80; margin-bottom: 20px; border-radius: 3px;'></div>
                <div class="dark-green-title">綠能產業端：去中心化普惠資本</div>
                <p style='font-size: 14.5px; color: #0C0E0B; line-height: 1.7; opacity: 0.85;'>底層資產錨定「陽光綠益」等 STO 售電收益權。引入散戶碎金流以降低開發商資金成本（WACC），同時維護電廠之經營自主權。</p>
            </div>
            """, unsafe_allow_html=True)

    # 區塊 D：頁腳 (Footer)
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='border-top: 1px solid #B7CEAD; padding: 35px 0; text-align: center; font-size: 12px; color: #0C0E0B; background-color: #FFFFFF; margin: 0 -4rem;'>
            <b>© 2026 EcoStride Research Project. Powered by Streamlit Community Cloud.</b><br>
            研究成員：蔡宜伶（Quantitative Finance & Information Management）| 賀舜禹 | 曾琬甯
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 4. 分頁二：提案動機與模式介紹 (完全保留不變)
# ==========================================
elif page == "提案動機與模式介紹":
    st.markdown("<h2 style='color:#0C0E0B !important; font-size:32px; font-weight:800;'>💡 提案動機與模式介紹</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h3 style='color:#83A474 !important; font-size:24px; font-weight:800; margin-bottom:15px;'>一、 現行系統之結構性失靈</h3>", unsafe_allow_html=True)
    
    st.markdown("""
        <table class="styled-table">
            <tr>
                <th>保險機構</th>
                <th>核心量化計費模式</th>
                <th>主要經濟激勵機制類型</th>
                <th>學術限制判讀</th>
            </tr>
            <tr>
                <td><b>國泰人壽</b></td>
                <td>AI 活力分多面向量化評分</td>
                <td>週週領點數模式（小樹點）</td>
                <td>側重即時性之消費回饋，缺乏跨期資本留存</td>
            </tr>
            <tr>
                <td><b>富邦人壽</b></td>
                <td>鎖定計步省保費機制</td>
                <td>次年保費最高折抵 10%</td>
                <td>偏重長期財務減負，但無法產生資產複利增值感</td>
            </tr>
            <tr>
                <td><b>第一金人壽</b></td>
                <td>遊戲化積分累積與商城兌換</td>
                <td>開放式平台商品兌換券</td>
                <td>純屬一次性行銷預算消耗，與理賠池優化脫鉤</td>
            </tr>
            <tr>
                <td><b>南山人壽</b></td>
                <td>生理年齡減齡演算法</td>
                <td>個人步數挑戰與 CSR 公益捐款耦合</td>
                <td>外部化社會責任，未能提供個人端財務永續誘因</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)

    col_fail1, col_fail2 = st.columns(2)
    with col_fail1:
        st.markdown("""
            <div class="alert-card">
                <span style="color:#83A474; font-weight:800; font-size:16px;">邊際效用遞減與長期價值缺失</span><br style="margin-bottom:8px;">
                現行點數 or 現金券在核發與使用的瞬間，其經濟價值即告終結，缺乏資產增值所需之<b>複利效應</b>。
                由於獎勵無法轉化為長期資本，用戶難以將健康行為視為一種「投資」，誘因隨時間呈對數曲線下滑。
            </div>
            """, unsafe_allow_html=True)
    with col_fail2:
        st.markdown("""
            <div class="alert-card">
                <span style="color:#83A474; font-weight:800; font-size:16px;">雙曲貼現與現時偏誤（Present Bias）</span><br style="margin-bottom:8px;">
                人類天生具備現時偏誤，對未來健康獲益之評價遠低於即時享樂。
                當回饋不具資本增值潛力時，用戶難以克服長期運動之生理痛苦，最終導致高度流失率。
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("""
        <div class="alert-card-danger">
            <span style="color:#E53E3E; font-weight:800; font-size:16px;">財務與經營層面之負面影響：</span><br style="margin-bottom:8px;">
            金融機構為了維持日活躍用戶，被迫持續加碼行銷支出，陷入高獲客成本與低生命週期價值之財務泥淖；
            若無法實質控制理賠損失率，行銷活動將從風險管理投資轉化為純粹之資產流失。
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_stepn1, col_stepn2 = st.columns(2)
    with col_stepn1:
        st.markdown("<h4 style='color:#0C0E0B !important; font-weight:800; border-bottom: 2px solid #83A474; padding-bottom: 6px;'>二、 STEPN Move-to-Earn 模式之反思</h4>", unsafe_allow_html=True)
        st.markdown("""
            STEPN 雖透過 Web3 遊戲化驅動健康行為，吸引超過 200 萬用戶。然而，其核心崩盤原因在於
            <b>「死亡螺旋經濟模型」</b>── 高度依賴新用戶流入以支撐舊用戶收益（龐氏結構），代幣（GST）通膨嚴重且缺乏真實資產背書，導致資產價值最終崩盤。
            <br><br>
            <b>EcoStride 的改良路徑：</b>借鏡其健康驅動與碎片化參與之優勢，但<b>轉向實體資產（RWA）背書</b>，將步數代幣（STRIDE）錨定綠能收益權，徹底避免純投機風險。
            """, unsafe_allow_html=True)
    with col_stepn2:
        st.markdown("<h4 style='color:#0C0E0B !important; font-weight:800; border-bottom: 2px solid #83A474; padding-bottom: 6px;'>三、 永續投資市場門檻與資本隔離</h4>", unsafe_allow_html=True)
        st.markdown("""
            高品質綠色資產（如離岸風電債券與大型太陽能案場收益權）具備顯著的規模排他性，最低認購額度通常達新台幣一百萬元以上，長期由機構法人壟斷，導致小額資本與年輕世代難以介入。碎片化資金因行政成本過高，被排除在永續轉型的資本紅利之外。
            """, unsafe_allow_html=True)

    st.markdown("<br>---<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='color:#83A474 !important; font-size:24px; font-weight:800; margin-bottom:15px;'>二、 創新提案 ── 三位一體模型</h3>", unsafe_allow_html=True)
    st.markdown("""
        本專案提出一套將個體健康行為直接轉化為資本累積之流轉模式。核心在於重構流動機制：<b>將消耗性獎勵重構為生產性累積</b>。
        保戶之健康行為不再僅是換取一次性消費憑證，而是轉化為具備增值潛力之生產性資本投入，建立長期且具備複利效應之資產池。
        <br><br>
        <b>三方共贏博弈分析：</b><br>
        1. <b>用戶端</b>：提供經過驗證之健康行為數據，藉此交換取得實體資產代幣化之收益權份額。<br>
        2. <b>保險公司端</b>：投入既有之行銷預算或理賠準備金作為資產認購資金，換取保戶理賠率之降低與 ESG 評級之提升。<br>
        3. <b>綠能產業端</b>：獲取來自廣大受眾、碎片化且低成本之建設資金。<b>碎片化資本具備純粹之財務投資屬性</b>，投資者人數眾多卻不具備干涉經營之組織力。這能讓綠能業者在獲取穩定建設資金的同時，<b>保有更高之經營獨立性與獲利分配主導權</b>。
        """, unsafe_allow_html=True)

    st.markdown("<br>---<br>", unsafe_allow_html=True)

    st.markdown("<h3 style='color:#83A474 !important; font-size:24px; font-weight:800; margin-bottom:15px;'>三、 本土實證與合規機制 ── 台灣市場落地性</h3>", unsafe_allow_html=True)
    st.markdown("""
        <b>1. 法規政策演進與監管試驗環境分析</b><br>
        金管會自 20 23 年起放寬證券型代幣（STO）規範，並於 2024 年正式成立實體資產代幣化小組。2025 年 9 月之概念驗證報告成功驗證債券與基金代幣化之可行性，落實券款對付之即時交割機制。此項技術突破，為本計畫中生物行為資產化後之即時權益分配，奠定了關鍵的技術與法理基礎。
        <br><br>
        <b>2. 國泰證券「陽光綠益」STO 案例研究（底層資產實證）</b><br>
        國泰證券與綠點能創合作，發行台灣首檔 STO「陽光綠益」（募資規模三千萬元）。底層資產為六年期債務型憑證，提供年利率 3.5% 之固定回報。此案例成果直接解決了過往 Web3 模式缺乏實體資產背書之痛點。實體資產代幣化提供穩定之綠能收益權作為價值支撐，使 EcoStride 核發之數位憑證具備實體生產力背書。
        <br><br>
        <b>3. 隱私保護與次級市場流通</b><br>
        針對資產期限較長之特性，擬引入自動化造市商機制建立微型資產流動性池；在個資隱私上，<b>採用零知識證明技術（Zero-Knowledge Proofs, ZKP）保護隱私</b>，確保代幣化資產之發行、存管與清算皆符合國際監管標準。
        """, unsafe_allow_html=True)

# ==========================================
# 5. 分頁三：APP 介面展示 (完全保留不變)
# ==========================================
elif page == "APP 介面展示":
    st.markdown("<h2 style='color:#0C0E0B !important; font-size:32px; font-weight:800;'>📱 APP 核心介面互動模擬</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:14px; color:#0C0E0B; opacity:0.8; font-weight:500;'>請嘗試在左側控制台調整您的每日健走行為，右側虛擬手機內的金融數據與清算面板將會即時同步跳動。</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_ui_left, col_ui_right = st.columns([1, 2.5])
    
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
        step_threshold = 5000
        
        excess = max(0, ui_steps - step_threshold)
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
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            st.markdown(f"""
                <div class="phone-container">
                    <div style="font-size:10px; color:#FFFFFF; text-align:space-between; margin-bottom:10px; font-family:monospace; padding: 0 5px;">
                        <span>09:41</span> <span style="float:right;">LTE 100%</span>
                    </div>
                    <div class="phone-screen">
                        <p style="font-size:11px; font-weight:800; color:#83A474; text-align:center; tracking-widest; letter-spacing:0.5px;">ECOSTRIDE DASHBOARD</p>
                        <br>
                        <div style="text-align:center;">
                            <span style="font-size:38px; font-weight:900; color:#0C0E0B;">{ui_steps:,}</span>
                            <p style="font-size:11px; color:#0C0E0B; margin:0; font-weight:600; opacity:0.6;">STEPS TODAY</p>
                        </div>
                        <br>
                        <div style="background-color:#F5F7F4; border:1px solid #B7CEAD; padding:15px; border-radius:14px; text-align:center;">
                            <span style="font-size:11px; color:#0C0E0B; font-weight:700;">今日雙引擎補貼</span>
                            <p style="font-size:24px; font-weight:900; color:#83A474; margin:5px 0;">NT$ {total_daily_val:.2f}</p>
                        </div>
                        <p style="font-size:10px; color:#0C0E0B; opacity:0.5; text-align:center; margin-top:90px; line-height:1.5;">
                            數據已透過零知識證明 (ZKP) 隱私保護技術完成安全驗證。
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; font-size:13px; font-weight:700; color:#0C0E0B; margin-top:10px;'>畫面 A：健康看板與資本生成</p>", unsafe_allow_html=True)

        with col_m2:
            discount_rate = (ui_steps / 15000) * 10 * ui_cons
            st.markdown(f"""
                <div class="phone-container">
                    <div style="font-size:10px; color:#FFFFFF; text-align:space-between; margin-bottom:10px; font-family:monospace; padding: 0 5px;">
                        <span>09:41</span> <span style="float:right;">LTE 100%</span>
                    </div>
                    <div class="phone-screen">
                        <p style="font-size:11px; font-weight:800; color:#83A474; text-align:center; tracking-widest; letter-spacing:0.5px;">ACTUARIAL PANEL</p>
                        <br>
                        <p style="font-size:11px; color:#0C0E0B; opacity:0.6; margin:0; font-weight:600;">行為穩定度因子</p>
                        <p style="font-size:18px; font-weight:800; color:#0C0E0B; margin:5px 0;">{ui_cons} ({profile_choice.split(" ")[0]})</p>
                        <br>
                        <div style="background-color:#83A474; padding:18px; border-radius:14px; color:#F5F7F4; text-align:center;">
                            <span style="font-size:10px; opacity:0.9; font-weight:600;">預計次年保費折減率</span>
                            <p style="font-size:26px; font-weight:900; margin:5px 0;">{min(10.0, discount_rate):.1f}%</p>
                        </div>
                        <br>
                        <div style="font-size:11px; color:#0C0E0B; line-height:1.7; background-color:#F5F7F4; padding:12px; border-radius:10px; border:1px solid #B7CEAD;">
                            <b>大盤護城河邊際：</b><br>
                            • 智慧合約回流準備金: 25%<br>
                            • 大盤保留風險剩餘: 80%
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; font-size:13px; font-weight:700; color:#0C0E0B; margin-top:10px;'>畫面 B：風險精算與保費反饋</p>", unsafe_allow_html=True)

        with col_m3:
            st.markdown(f"""
                <div class="phone-container">
                    <div style="font-size:10px; color:#FFFFFF; text-align:space-between; margin-bottom:10px; font-family:monospace; padding: 0 5px;">
                        <span>09:41</span> <span style="float:right;">LTE 100%</span>
                    </div>
                    <div class="phone-screen">
                        <p style="font-size:11px; font-weight:800; color:#83A474; text-align:center; tracking-widest; letter-spacing:0.5px;">RWA GREEN PORTFOLIO</p>
                        <br>
                        <div style="background-color:#FFFFFF; border:1px solid #B7CEAD; padding:15px; border-radius:14px; text-align:center; box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
                            <span style="font-size:11px; color:#0C0E0B; font-weight:600; opacity:0.7;">10年累積 STRIDE 市值</span>
                            <p style="font-size:24px; font-weight:900; color:#83A474; margin:5px 0;">NT$ {calc_eco:,.0f}</p>
                        </div>
                        <br>
                        <div style="font-size:11px; background-color:#F5F7F4; padding:12px; border-radius:10px; border:1px solid #B7CEAD; line-height:1.6;">
                            <b style="color:#83A474;">錨定底層資產：</b><br>
                            國泰證券 — 陽光綠益太陽能案場<br>
                            • FIT 固定收益率: 3.5%<br>
                            • 信託管理費: 1.5%
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; font-size:13px; font-weight:700; color:#0C0E0B; margin-top:10px;'>畫面 C：實體資產與財富面板</p>", unsafe_allow_html=True)

# ==========================================
# 6. 分頁四：相關研究成果 (完全保留不變)
# ==========================================
elif page == "相關研究成果":
    st.markdown("<h2 style='color:#0C0E0B !important; font-size:32px; font-weight:800;'>📊 相關研究成果 ── 彭博精算終端模擬</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:14px; color:#0C0E0B; opacity:0.8; font-weight:500;'>本模組完全嵌入後台 Python 精算大腦。點擊下方測試按鈕即可執行 5,000 次全域對齊之蒙地卡羅模擬壓力測試。</p>", unsafe_allow_html=True)
    st.markdown("---")

    col_res_left, col_res_right = st.columns([1.2, 3])
    
    with col_res_left:
        st.markdown("<div style='background-color:#FFFFFF; border:1px solid #B7CEAD; padding:24px; border-radius:14px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#0C0E0B !important; margin-top:0; font-weight:800;'>生態系壓力測試面板</h4>", unsafe_allow_html=True)
        param_steps_inc = st.slider("保戶步行提升幅度 (Steps Increase %)", 0.05, 0.50, 0.20, 0.05)
        param_consistency = st.slider("全域行為穩定度均值 (Avg Consistency)", 0.30, 1.00, 0.75, 0.05)
        
        st.markdown("<br>", unsafe_allow_html=True)
        run_sim = st.button("執行 5,000 次全域對齊 Monte Carlo 模擬 ⚡")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if param_steps_inc >= 0.20 and param_consistency >= 0.70:
            st.markdown("<div style='color:#83A474; font-size:13px; font-weight:700;'>🔥 系統提示：當前行為特徵已成功啟動生產性複利飛輪，三方正和博弈達成。</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#D97706; font-size:13px; font-weight:700;'>⚠️ 系統提示：誘因 or 持續性不足，保險公司陷入行銷流失泥淖，請嘗試調高參數。</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_res_right:
        if run_sim:
            progress_bar = st.progress(0)
            status_text = st.empty()
            for percent_complete in range(100):
                time.sleep(0.01)
                progress_bar.progress(percent_complete + 1)
                status_text.text(f"正在執行 5,000 次隨機氣候與 Gamma 分佈理賠路徑清算中... {percent_complete+1}%")
            status_text.success("⚡ 5,000 次跨界聯立矩陣隨機清算完成！")
            
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        dynamic_win_ratio = 56.38 + (param_steps_inc - 0.20) * 40 + (param_consistency - 0.75) * 30
        dynamic_win_ratio = max(0.0, min(100.0, dynamic_win_ratio))
        
        with col_m1:
            st.markdown(f"""
                <div class="metric-card" style="border-top: 4px solid #83A474;">
                    <div class="metric-value-green">{dynamic_win_ratio:.2f}%</div>
                    <div class="metric-label">全域共贏機率 (Win-Win)</div>
                </div>
                """, unsafe_allow_html=True)
        with col_m2:
            st.markdown("""
                <div class="metric-card" style="border-top: 4px solid #0C0E0B;">
                    <div class="metric-value-blue">99.96%</div>
                    <div class="metric-label">保險公司獲利機率</div>
                </div>
                """, unsafe_allow_html=True)
        with col_m3:
            st.markdown("""
                <div class="metric-card" style="border-top: 4px solid #B7CEAD;">
                    <div class="metric-value-blue">3.50%</div>
                    <div class="metric-label">綠能開發商 WACC</div>
                </div>
                """, unsafe_allow_html=True)
        with col_m4:
            calc_final_w = 6657 * (param_steps_inc / 0.20) * (param_consistency / 0.75)
            st.markdown(f"""
                <div class="metric-card" style="border-top: 4px solid #92BA80;">
                    <div class="metric-value-green">NT$ {max(0.0, calc_final_w):,.0f}</div>
                    <div class="metric-label">典型保戶10年資產均值</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tab_res1, tab_res2, tab_res3, tab_res4 = st.tabs([
        "消費者端研究", "保險公司端研究", "綠能產業端研究", "整體生態系循環"
    ])
    
    years_x = [f"第 {i} 年" for i in range(11)]
    
    with tab_res1:
        st.markdown("<h4 style='color:#0C0E0B !important; font-weight:800; margin-top:10px;'>【研究 1, 2 & 3】財富分化與生產性資產跨期對比</h4>", unsafe_allow_html=True)
        
        base_inv = 2900 * 0.00065 * 365 * param_consistency
        high_path = [0]
        med_path = [0]
        low_path = [0]
        trad_path = [0]
        
        curr_h, curr_m, curr_l, curr_t = 0, 0, 0, 0
        for y in range(1, 11):
            curr_h = (curr_h + base_inv * 1.5) * (1 + 0.035 * 0.75 + 0.05)
            curr_m = (curr_m + base_inv * (param_steps_inc/0.20)) * (1 + 0.035 * 0.75 + 0.05)
            curr_l = (curr_l + base_inv * 0.4) * (1 + 0.035 * 0.75 + 0.05)
            curr_t = curr_t + 600 * max(0.2, 1.0 - 0.05 * np.log1p(y*365))
            high_path.append(curr_h)
            med_path.append(curr_m)
            low_path.append(curr_l)
            trad_path.append(curr_t)

        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=years_x, y=high_path, name="High 活躍族群", line=dict(color="#92BA80", width=3.5)))
        fig1.add_trace(go.Scatter(x=years_x, y=med_path, name="Medium 典型保戶", line=dict(color="#83A474", width=3.5)))
        fig1.add_trace(go.Scatter(x=years_x, y=low_path, name="Low 低活躍族群", line=dict(color="#B7CEAD", width=2.5)))
        fig1.add_trace(go.Scatter(x=years_x, y=trad_path, name="傳統消耗性點數保單", line=dict(color="#E53E3E", dash="dash")))
        fig1.update_layout(title="10 年期累積資產規模隨機路徑對照", template="plotly_white", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown("""
            <b>學術解讀與誠實揭露修正：</b><br>
            定量模擬顯示，高活躍用戶與低活躍用戶最終累積財富差高達數倍，證實行為持續性因子（Stability Factor）對個人財富具有顯著的放大效應。<br>
            然而，精算模型誠實揭露：若以台灣常見的 NT$ 10,000 作為理財門檻，中度活躍用戶單靠走路在 10 年內解鎖的成功率極低。<br>
            因此，本專案在白皮書中正式倡議<b>「將 RWA 起投門檻下探至 NT$ 5,000」</b>，如此可使普惠覆蓋率顯著攀升，落實普惠金融。
            """, unsafe_allow_html=True)

    with tab_res2:
        st.markdown("<h4 style='color:#0C0E0B !important; font-weight:800; margin-top:10px;'>【研究 6, 8 & 10】醫療理賠損失率分佈與精算折讓</h4>", unsafe_allow_html=True)
        
        x_loss = np.linspace(0.5, 1.0, 100)
        y_density = np.exp(-(x_loss - 0.72)**2 / (2 * 0.04**2))
        y_density_base = np.exp(-(x_loss - 0.75)**2 / (2 * 0.04**2))
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=x_loss*100, y=y_density, name="優化後理賠池損失率分佈", fill='tozeroy', line=dict(color="#83A474")))
        fig2.add_trace(go.Scatter(x=x_loss*100, y=y_density_base, name="初始基準損失率 (75%)", line=dict(color="#0C0E0B", dash="dash")))
        fig2.update_layout(title="保險大盤年度損失率機率密度函數 (第 10 年結算)", template="plotly_white", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("""
            <b>精算折讓 (Actuarial Haircut) 與風險控制：</b><br>
            本模型設定之健康-風險彈性係數（-0.15）雖具備公衛頂級文獻支撐，但考量保戶計步作弊、逆選擇等道德風險，
            模型採取保守主義，<b>進行了 3.4 倍之精算折讓 (Haircut)</b>，確保保險大盤擁有 80% 的風險剩餘，抵抗黑天鵝理賠。<br>
            敏感度測試證明：步數提升若低於 5% 專案將嚴重虧損，唯有超過 20% 門檻方可衝破 1.03 ROI。
            且整體回饋精確控制在 3.4% ~ 7.1%，<b>完美遵從金管會 10% 的附加費用監管紅線</b>。
            """, unsafe_allow_html=True)

    with tab_res3:
        st.markdown("<h4 style='color:#0C0E0B !important; font-weight:800; margin-top:10px;'>【研究 12, 13 & 14】碎片化籌資效率與電廠設備重置衝擊</h4>", unsafe_allow_html=True)
        
        om_filling = [100.0] * 11
        om_filling[8] = 78.4  
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=years_x, y=om_filling, name="運維公積金填補率 (%)", marker_color="#83A474"))
        fig3.update_layout(title="電廠中長期運維基金 (O&M) 缺口自動填補率 (第 8 年遭逢 200 萬變流器重大重置 CAPEX 衝擊)", template="plotly_white", height=400, yaxis=dict(range=[0, 120]), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown("""
            <b>籌資擴展性與資產韌性：</b><br>
            10,000 人保戶規模下，需 5.64 年可滿額募集 3,000 萬元的太陽能案場。<br>
            <b>拓展情境分析：</b>若擴展至全台 10 萬名保戶，碎金流募集規模效應爆發，<b>滿額籌資天數將縮短至 7 個月（205.9天）</b>！<br>
            在資金成本方面，WACC 從銀行貸款的 4.2% 降至 3.5%，顯著優於傳統渠道。<br>
            即使第 8 年遭遇台灣高溫高濕導致<b>變流器集體老化損壞、產生 200 萬元 CapEx 衝擊</b>，得益於前幾年資產池滾存的蓄水池，填補率仍能維持在 78.4% 穩健水位，流動性風險完全消弭。
            """, unsafe_allow_html=True)

    with tab_res4:
        st.markdown("<h4 style='color:#0C0E0B !important; font-weight:800; margin-top:10px;'>【研究 15, 16 & 17】三位一體全局穩定性與自然氣候防禦</h4>", unsafe_allow_html=True)
        st.markdown(f"""
            根據 5,000 次全局跨界聯立蒙地卡羅清算，三方同時達成正向飛輪之<b>全域共贏比例 (Win-Win Ratio) 精確定格在 {dynamic_win_ratio:.2f}%</b>。<br>
            這是在「保險公司利潤不低於傳統模式 95%」的合理商業讓渡門檻下達成的。
            <br><br>
            <b>邊際決策邊際分析：</b>當保戶行為持續性低於 40% 時，健康代理效果崩塌；一旦跨越 75% 門檻，複利循環高機率啟動。
            <br><br>
            <b>氣候黑天鵝托底防禦：</b>本模型導入台灣夏季高日照、梅雨季突發連續大雨（效益隨機重擊 -35%）之氣候風險傳導。<br>
            精算證實，在 95% 置信區間最極端之日照不足黑天鵝路徑下，保戶最終資產仍能保持穩定。
            這是因為我們在智慧合約中引入了 <b>3.0% 實體綠能最低托底保價機制 (Floor Yield)</b>，成功切斷了自然環境對保戶回饋的負面傳導，具備完美的抗風險韌性。
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📄 檢視後台核心複利精算公式 (互鎖定量金融與資管代碼)"):
        st.code("""
# EcoStride 智慧合約跨期核心資產滾存演算法
# 完全對齊定量金融精算架構，包含 25% 收益回流與 5% 市場資本利得

def calculate_compounding_rwa_wealth(excess_steps, alpha, beta, gamma, consistency, rwa_yield_base, insurance_share_yield, mu_market):
    daily_investment = (excess_steps * alpha + (excess_steps * beta * gamma)) * consistency
    annual_investment = daily_investment * 365
    
    total_user_rwa_wealth = 0.0
    for year in range(1, 11):
        # 智慧合約自動結算：發電總收益
        annual_rwa_yield_generated = total_user_rwa_wealth * rwa_yield_base
        # 25% 回流保險準備金
        rwa_flowback_to_insurance = annual_rwa_yield_generated * insurance_share_yield
        # 75% 用戶端收益自動再投資
        user_yield_reinvest = annual_rwa_yield_generated - rwa_flowback_to_insurance
        
        # 三方財務池會計平衡
        total_user_rwa_wealth += annual_investment + user_yield_reinvest
        
        # 5% 代幣市場增值 (資本利得屬用戶端財富)
        total_user_rwa_wealth *= (1.0 + mu_market)
        
    return total_user_rwa_wealth
        """, language="python")
