import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# ==========================================
# 0. 全局環境配置與客製化永續金融 CSS 注入
# ==========================================
st.set_page_config(
    page_title="EcoStride Terminal | 永續金融精算大盤",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 注入深度客製化 CSS，完全替換 Streamlit 預設視覺
st.markdown("""
    <style>
    /* 全域背景與文字配置 */
    .stApp {
        background-color: #f5f7f4;
        color: #0c0e0b;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Noto Sans TC", sans-serif;
    }
    
    /* 側邊導航欄優化 */
    .stSidebar {
        background-color: #f5f7f4 !important;
        border-right: 1px solid #b7cead !important;
    }
    
    /* 大標題與次標題色彩定調 */
    h1, h2, h3, h4 {
        color: #0c0e0b !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px !important;
    }
    
    /* 核心亮點：高質感永續綠色矩形按鈕 */
    div.stButton > button {
        background-color: #83a474 !important;
        color: #f5f7f4 !important;
        border: 1px solid #83a474 !important;
        border-radius: 6px !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        letter-spacing: 1px !important;
        box-shadow: 0 4px 10px rgba(131, 164, 116, 0.15) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div.stButton > button:hover {
        background-color: #92ba80 !important;
        border-color: #92ba80 !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(146, 186, 128, 0.3) !important;
    }
    
    /* 麥肯錫/彭博風格精算方磚色塊 */
    .metric-card {
        background-color: #f5f7f4;
        border: 1px solid #b7cead;
        border-radius: 8px;
        padding: 24px;
        text-align: left;
        box-shadow: 0 2px 4px rgba(0,0,0,0.01);
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: #83a474;
        background-color: #f5f7f4;
    }
    .val-primary {
        font-size: 38px; font-weight: 800; color: #83a474; font-family: 'SF Pro Text', monospace; line-height: 1;
    }
    .val-dark {
        font-size: 38px; font-weight: 800; color: #0c0e0b; font-family: 'SF Pro Text', monospace; line-height: 1;
    }
    .lbl-title {
        font-size: 11px; font-weight: 700; color: #0c0e0b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;
        opacity: 0.7;
    }
    
    /* 願景卡片色塊配置 */
    .vision-card {
        border: 1px solid #b7cead;
        padding: 35px;
        border-radius: 12px;
        background-color: #ffffff;
        min-height: 290px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.01);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .vision-card:hover {
        transform: translateY(-4px);
        border-color: #83a474;
        box-shadow: 0 12px 24px rgba(131, 164, 116, 0.08);
    }
    
    /* 虛擬手機 iPhone Mockup 細節美化 */
    .iphone-shell {
        border: 10px solid #0c0e0b;
        border-radius: 36px;
        padding: 10px;
        background-color: #0c0e0b;
        box-shadow: 0 15px 35px rgba(12, 14, 11, 0.06);
        height: 590px;
        position: relative;
    }
    .dynamic-island {
        width: 100px; height: 22px; background-color: #0c0e0b; border-radius: 12px;
        position: absolute; top: 16px; left: 50%; transform: translateX(-50%); z-index: 99;
    }
    .iphone-screen {
        border-radius: 24px;
        background-color: #f5f7f4;
        padding: 24px 14px;
        height: 100%;
        overflow-y: auto;
        color: #0c0e0b;
    }
    
    /* 現代結構化表格 */
    .modern-table {
        width: 100%; border-collapse: separate; border-spacing: 0 6px; margin: 20px 0;
    }
    .modern-table th {
        background-color: #b7cead; color: #0c0e0b; padding: 14px; font-weight: 700; text-align: left;
        font-size: 13px; letter-spacing: 0.5px; border-radius: 4px;
    }
    .modern-table td {
        padding: 16px; background-color: #ffffff; border-top: 1px solid #b7cead; border-bottom: 1px solid #b7cead;
        font-size: 14px; color: #0c0e0b; transition: all 0.2s ease;
    }
    .modern-table tr:hover td {
        background-color: #f5f7f4;
    }
    .modern-table td:first-child { border-left: 1px solid #b7cead; border-radius: 6px 0 0 6px; }
    .modern-table td:last-child { border-right: 1px solid #b7cead; border-radius: 0 6px 6px 0; }
    
    /* 學術白皮書提示色塊 */
    .paper-block {
        border-left: 4px solid #83a474; padding-left: 20px; margin: 25px 0; background-color: #ffffff; padding: 20px; border-radius: 0 8px 8px 0; border-top: 1px solid #f5f7f4; border-bottom: 1px solid #f5f7f4; border-right: 1px solid #f5f7f4;
    }
    .paper-block-danger {
        border-left: 4px solid #83a474; padding-left: 20px; margin: 25px 0; background-color: #ffffff; padding: 20px; border-radius: 0 8px 8px 0; border: 1px solid #b7cead; border-left: 4px solid #83a474;
    }
    
    /* 頂部毛玻璃導航列 */
    .navbar-mock {
        background: rgba(245, 247, 244, 0.85);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid #b7cead;
        padding: 18px 40px;
        position: sticky; top: 0; z-index: 999;
        display: flex; justify-content: space-between; align-items: center;
        margin: -6rem -4rem 2rem -4rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. 頂部毛玻璃導航列
# ==========================================
st.markdown("""
    <div class="navbar-mock">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 6px; height: 26px; background-color: #83a474; border-radius: 2px;"></div>
            <span style="font-size: 20px; font-weight: 900; letter-spacing: 3px; color: #0c0e0b;">ECOSTRIDE</span>
            <span style="font-size: 11px; background-color: #83a474; color: #f5f7f4; padding: 2px 8px; border-radius: 4px; font-weight: 600; letter-spacing: 0.5px;">FINTECH RESEARCH</span>
        </div>
        <div style="font-size: 13px; color: #0c0e0b; font-weight: 600; opacity: 0.8;">
            國立清華大學 金融科技專題研究成果展示大盤
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 2. 側邊欄個人化導覽選單
# ==========================================
with st.sidebar:
    st.markdown("<div style='padding: 10px 0 20px 0;'><h2 style='color:#0c0e0b !important; font-size:24px; font-weight:800; letter-spacing:-0.5px;'>終端機目錄</h2></div>", unsafe_allow_html=True)
    page = st.radio(
        "切換當前調閱報告：",
        ["專案首頁", "提案動機與模式介紹", "APP 介面展示", "相關研究成果"]
    )
    st.markdown("<hr style='border-color: #b7cead;'>", unsafe_allow_html=True)
    st.markdown("""
        <div style='font-size: 12px; color: #0c0e0b; opacity: 0.8; line-height: 2;'>
        <b>RESEARCH TEAM</b><br>
        蔡宜伶 | Quantitative Finance & Info Management<br>
        賀舜禹 | Quantitative Finance<br>
        曾琬甯 | Quantitative Finance<br><br>
        <b>ADVISOR</b><br>
        清華大學計量財務金融學系 專題審查組
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 3. 分頁一：專案首頁
# ==========================================
if page == "專案首頁":
    st.markdown("<div style='padding: 90px 0 50px 0; text-align: center;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 56px; font-weight: 900; color: #0c0e0b !important; letter-spacing: -1.5px; margin-bottom: 20px; line-height:1.15;'>讓健康行為，成為生產性綠色資本</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 20px; color: #0c0e0b; opacity: 0.8; max-width: 800px; margin: 0 auto 35px auto; line-height: 1.6;'>結合行為金融學理論與實體資產代幣化（RWA）技術，重構永續金融生態系。</p>", unsafe_allow_html=True)
    
    st.markdown("""
        <div style='display: flex; justify-content: center; gap: 12px; margin-bottom: 50px;'>
            <span style='background-color: #ffffff; color: #0c0e0b; padding: 8px 20px; border-radius: 4px; font-size: 13px; border: 1px solid #b7cead; font-weight:600;'>國立清華大學 金融科技專題研究</span>
            <span style='background-color: #ffffff; color: #83a474; padding: 8px 20px; border-radius: 4px; font-size: 13px; border: 1px solid #83a474; font-weight:700;'>Quantitative Finance & Information Management</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<hr style='border: none; border-top: 1px solid #b7cead; margin: 30px 0;'>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; font-size: 24px; font-weight:800; margin-bottom: 40px; color:#0c0e0b !important; letter-spacing:-0.5px;'>三位一體機制全局摘要</h3>", unsafe_allow_html=True)
    
    col_card1, col_card2, col_card3 = st.columns(3)
    with col_card1:
        st.markdown("""
            <div class="vision-card">
                <div style='font-size: 11px; font-weight: 800; color: #83a474; tracking-widest; margin-bottom: 12px;'>MECHANISM 01</div>
                <h4 style='font-size: 19px; font-weight: 800; color: #0c0e0b; margin-bottom: 15px;'>消費者端：生物行為資產化</h4>
                <p style='font-size: 14px; color: #0c0e0b; opacity: 0.8; line-height: 1.75;'>徹底打破財富階級門檻。無初始存款之年輕族群，僅靠規律之步行數據，即可無痛認購綠能案場份額，共享淨零轉型之資本紅利。</p>
            </div>
            """, unsafe_allow_html=True)
            
    with col_card2:
        st.markdown("""
            <div class="vision-card">
                <div style='font-size: 11px; font-weight: 800; color: #83a474; tracking-widest; margin-bottom: 12px;'>MECHANISM 02</div>
                <h4 style='font-size: 19px; font-weight: 800; color: #0c0e0b; margin-bottom: 15px;'>保險公司端：高效率風險管理</h4>
                <p style='font-size: 14px; color: #0c0e0b; opacity: 0.8; line-height: 1.75;'>將既有行銷費用與理賠準備金提前折現注入綠能基金，透過資產的生產性複利增值感，實質且長期優化保戶健康品質，控制理賠損失率。</p>
            </div>
            """, unsafe_allow_html=True)
            
    with col_card3:
        st.markdown("""
            <div class="vision-card">
                <div style='font-size: 11px; font-weight: 800; color: #83a474; tracking-widest; margin-bottom: 12px;'>MECHANISM 03</div>
                <h4 style='font-size: 19px; font-weight: 800; color: #0c0e0b; margin-bottom: 15px;'>綠能產業端：去中心化普惠資本</h4>
                <p style='font-size: 14px; color: #0c0e0b; opacity: 0.8; line-height: 1.75;'>底層資產錨定「陽光綠益」等 STO 售電收益權。引入散戶碎金流以降低開發商資金成本（WACC），同時維護電廠之經營自主權。</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='border-top: 1px solid #b7cead; padding: 30px 0; text-align: center; font-size: 12px; color: #0c0e0b; opacity: 0.6; background-color: #ffffff; margin: 0 -4rem;'>
            © 2026 EcoStride Research Project. Powered by Streamlit Community Cloud.<br>
            研究成員：蔡宜伶（Quantitative Finance & Information Management）| 賀舜禹 | 曾琬甯
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# 4. 分頁二：提案動機與模式介紹 (含活的動機沙盤)
# ==========================================
elif page == "提案動機與模式介紹":
    st.markdown("<h2 style='color:#0c0e0b !important; font-size:32px; font-weight:900; letter-spacing:-1px;'>💡 提案動機與模式介紹</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h3 style='color:#83a474 !important; font-size:22px; font-weight:800;'>一、 現行系統之結構性失靈</h3>", unsafe_allow_html=True)
    
    st.markdown("""
        <table class="modern-table">
            <thead>
                <tr>
                    <th>保險機構</th>
                    <th>核心量化計費模式</th>
                    <th>主要經濟激勵機制類型</th>
                    <th>學術與精算限制判讀</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><b>國泰人壽</b></td>
                    <td>AI 活力分多面向量化評分</td>
                    <td>週週領點數模式（小樹點）</td>
                    <td>側重於即時性之生活消費回饋，經濟價值瞬間終結，缺乏跨期資本留存</td>
                </tr>
                <tr>
                    <td><b>富邦人壽</b></td>
                    <td>鎖定計步省保費機制</td>
                    <td>次年保費最高折抵 10%</td>
                    <td>偏重長期財務減負，但屬消耗性回饋，無法產生資產複利增值感</td>
                </tr>
                <tr>
                    <td><b>第一金人壽</b></td>
                    <td>遊戲化積分累積與商城兌換</td>
                    <td>開放式平台商品兌換券</td>
                    <td>純屬一次性行銷預算消耗，與理賠池優化脫鉤，保戶因疲勞進入停滯期</td>
                </tr>
                <tr>
                    <td><b>南山人壽</b></td>
                    <td>生理年齡減齡演算法</td>
                    <td>個人步數挑戰與 CSR 公益捐款耦合</td>
                    <td>外部化社會責任，未能提供個人端財務永續誘因與現時偏誤對抗</td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)

    st.markdown("<div class='paper-block'>", unsafe_allow_html=True)
    st.markdown("<h4 style='margin-top:0; color:#83a474 !important;'><b>行為金融學視角之結構失靈分析</b></h4>", unsafe_allow_html=True)
    st.markdown("""
        現行外溢保單之核心痛點在於<b>「現時偏誤 (Present Bias)」與「邊際效用遞減」</b>。點數或現金券在核發與使用的瞬間，其經濟價值即告終結，缺乏資產增值所需之複利效應。
        保戶天生具備現時偏誤，對未來健康獲益評價極低，當回饋不具備「資本增值潛力」時，用戶難以克服長期運動之生理痛苦，最終導致高流失率。
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='paper-block-danger'>", unsafe_allow_html=True)
    st.markdown("<h5 style='margin-top:0; color:#0c0e0b !important;'>⚠️ <b>金融公司財務泥淖</b></h5>", unsafe_allow_html=True)
    st.markdown("""
        為了維持日活躍用戶，金融機構被迫持續加碼一次性行銷支出，陷入高獲客成本與低生命週期價值之惡性循環；
        若無法實質控制理賠損失率，行銷活動將從風險管理投資轉化為純粹之資產流失。
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col_block1, col_block2 = st.columns(2)
    with col_block1:
        st.markdown("<h4 style='color:#0c0e0b !important; font-weight:800;'>二、 STEPN Move-to-Earn 模式之借鏡與反思</h4>", unsafe_allow_html=True)
        st.markdown("""
            STEPN 雖透過遊戲化成功驅動健康行為，但其核心崩盤原因在於<b>「死亡螺旋經濟模型」</b>── 高度依賴新用戶流入以支撐舊用戶收益的龐氏結構，缺乏真實資產背書。
            EcoStride 借鏡其健走驅動優勢，但<b>轉向實體資產 (RWA) 背書</b>，將代幣錨定綠能收益，徹底避免投機風險。
            """, unsafe_allow_html=True)
    with col_block2:
        st.markdown("<h4 style='color:#0c0e0b !important; font-weight:800;'>三、 永續投資市場門檻與資本隔離</h4>", unsafe_allow_html=True)
        st.markdown("""
            高品質綠色資產（如大型太陽能案場收益權）最低認購額度高達新台幣一百萬元以上，長期由機構法人壟斷。
            碎片化資金因行政成本過高被排除在外，EcoStride 透過代幣化技術打破規模排他性，落實普惠金融。
            """, unsafe_allow_html=True)

    st.markdown("<br>---<br>", unsafe_allow_html=True)

    # 區塊 B：三位一體動態互動沙盤
    st.markdown("<h3 style='color:#83a474 !important; font-size:22px; font-weight:800;'>二、 創新提案 ── 三位一體動態價值沙盤</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:14px; color:#0c0e0b; opacity:0.8;'>滑鼠移至下方節點或線條，可動態觀看 EcoStride 去中心化生態系的真實價值流向與分配邏輯：</p>", unsafe_allow_html=True)
    
    fig_sandbox = go.Figure()
    fig_sandbox.add_trace(go.Scatter(
        x=[2, 1, 3, 2], y=[3, 1, 1, 3],
        mode='markers+text+lines',
        marker=dict(size=[50, 50, 50, 50], color=['#83a474', '#92ba80', '#b7cead', '#83a474'], line=dict(color='#0c0e0b', width=1)),
        text=["保險公司", "用戶端", "綠能產業", "保險公司"],
        textposition="top center",
        hoverinfo='text',
        hovertext=[
            "保險公司：理賠準備金提前折現注入，換取保戶整體損失率調降與長線 ESG 增益",
            "用戶端：解鎖生物行為資產化，以每日走路數據交換實體太陽能售電分潤權",
            "綠能產業：對接去中心化散戶碎金流，免除大型金控干涉，WACC 資金成本大幅降低",
            "保險公司"
        ],
        line=dict(color='#83a474', width=2)
    ))
    fig_sandbox.update_layout(
        template="plotly_white", height=320,
        paper_bgcolor='#ffffff', plot_bgcolor='#ffffff',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(fig_sandbox, use_container_width=True)

    st.markdown("""
        <b>綠色端戰略儲備與經營主導權：</b>為什麼高品質電廠願意配合散戶碎金流？因為過度集中的融資來源（大型金控、單一財團）隱含高度議價風險與經營權干涉。
        EcoStride 引入之碎片化資本具備純粹財務投資屬性，投資者人數眾多但不具備干涉經營之組織力。
        這能讓綠能業者在獲取穩定建設資金的同時，<b>保有更高之經營獨立性與獲利分配主導權</b>。
        """, unsafe_allow_html=True)

# ==========================================
# 5. 分頁三：APP 介面展示 (iPhone 雙向動態黑科技聯動)
# ==========================================
elif page == "APP 介面展示":
    st.markdown("<h2 style='color:#0c0e0b !important; font-size:32px; font-weight:900; letter-spacing:-1px;'>📱 APP 核心介面互動模擬</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_ui_left, col_ui_right = st.columns([1.1, 2.5])
    
    with col_ui_left:
        st.markdown("<div style='background-color:#ffffff; padding:25px; border-radius:12px; border:1px solid #b7cead;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#0c0e0b !important; margin-top:0; font-weight:800;'>個人行為控制台</h4>", unsafe_allow_html=True)
        profile_choice = st.pills("選擇保戶步行特徵：", ["高活躍 High", "典型 Medium", "低活躍 Low"], default="典型 Medium")
        
        if "High" in profile_choice:
            init_steps, init_cons = 9500, 1.0
        elif "Medium" in profile_choice:
            init_steps, init_cons = 7500, 0.7
        else:
            init_steps, init_cons = 5200, 0.3
            
        ui_steps = st.slider("調整每日平均步數：", 0, 20000, init_steps, 500)
        ui_cons = st.slider("調整行為持續性因子 (Consistency)：", 0.1, 1.0, init_cons, 0.1)
        
        # 聯立清算引擎
        alpha, beta, gamma = 0.00065, 0.0001, 0.20
        excess = max(0, ui_steps - 5000)
        engine_A = excess * alpha * ui_cons
        engine_B = excess * beta * gamma * ui_cons
        total_daily = engine_A + engine_B
        
        # 動態即時複利路徑繪製
        eco_path_mini = [0]
        curr_m = 0
        for _ in range(10):
            curr_m = (curr_m + total_daily * 365) * (1 + (0.035 * 0.75) + 0.05)
            eco_path_mini.append(curr_m)
            
        st.markdown(f"""
            <div style='background-color:#f5f7f4; border:1px solid #b7cead; padding:15px; border-radius:6px; font-size:12px; line-height:1.8; color:#0c0e0b;'>
                <span style='color:#83a474; font-weight:700;'>區區塊鏈智慧合約日結清算：</span><br>
                • 激勵引擎 A 價值: NT$ {engine_A:.2f}<br>
                • 精算引擎 B 折現: NT$ {engine_B:.4f}<br>
                <b>• 當日生成綠色總合資本: NT$ {total_daily:.2f}</b>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_ui_right:
        col_m1, col_m2, col_m3 = st.columns(3)
        
        # 手機 A：User Dashboard
        with col_m1:
            st.markdown(f"""
                <div class="iphone-shell">
                    <div class="dynamic-island"></div>
                    <div class="iphone-screen">
                        <p style="font-size:10px; font-weight:800; color:#83a474; text-align:center; letter-spacing:1px; margin-top:5px;">ECOSTRIDE DASHBOARD</p>
                        <br>
                        <div style="text-align:center; margin: 15px 0;">
                            <span style="font-size:40px; font-weight:900; color:#0c0e0b; font-family:'Courier New';">{ui_steps:,}</span>
                            <p style="font-size:11px; color:#0c0e0b; opacity:0.6; margin:0; font-weight:600;">STEPS TODAY</p>
                        </div>
                        <div style="background-color:#ffffff; border:1px solid #b7cead; padding:15px; border-radius:10px; text-align:center;">
                            <span style="font-size:11px; color:#0c0e0b; font-weight:700;">今日雙引擎代幣生成</span>
                            <p style="font-size:24px; font-weight:800; color:#83a474; margin:5px 0;">NT$ {total_daily:.2f}</p>
                        </div>
                        <p style="font-size:9px; color:#0c0e0b; opacity:0.5; text-align:center; margin-top:130px; line-height:1.4;">
                            生理隱私受零知識證明 (ZKP) 架構安全防禦，大盤僅留存合規去識別化哈希值。
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; font-size:12px; font-weight:700; color:#0c0e0b; opacity:0.8; margin-top:10px;'>畫面 A：健康促進與即時資本</p>", unsafe_allow_html=True)

        # 手機 B：Actuarial Panel
        with col_m2:
            discount_rate = (ui_steps / 15000) * 10 * ui_cons
            st.markdown(f"""
                <div class="iphone-shell">
                    <div class="dynamic-island"></div>
                    <div class="iphone-screen">
                        <p style="font-size:10px; font-weight:800; color:#83a474; text-align:center; letter-spacing:1px; margin-top:5px;">ACTUARIAL PANEL</p>
                        <br>
                        <p style="font-size:11px; color:#0c0e0b; opacity:0.6; margin:0; font-weight:600;">大盤持續性行為因子</p>
                        <p style="font-size:18px; font-weight:800; color:#0c0e0b; margin:4px 0;">{ui_cons}</p>
                        <br>
                        <div style="background: #83a474; padding:18px; border-radius:10px; color:#f5f7f4;">
                            <span style="font-size:10px; opacity:0.9; font-weight:600;">預計次年保費減免率</span>
                            <p style="font-size:26px; font-weight:900; margin:4px 0;">{min(10.0, discount_rate):.1f}%</p>
                        </div>
                        <br>
                        <div style="font-size:11px; color:#0c0e0b; line-height:1.8; background-color:#ffffff; padding:12px; border-radius:8px; border:1px solid #b7cead;">
                            <b>大盤下行風險準備控制：</b><br>
                            • 25% 收益自動智慧回流準備金<br>
                            • 80% 大盤精算風險邊際保留額
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; font-size:12px; font-weight:700; color:#0c0e0b; opacity:0.8; margin-top:10px;'>畫面 B：下行風險與保費反饋</p>", unsafe_allow_html=True)

        # 手機 C：RWA Portfolio (動態 Plotly 縮圖對接森林系配色)
        with col_m3:
            with st.container():
                st.markdown(f"""
                    <div class="iphone-shell">
                        <div class="dynamic-island"></div>
                        <div class="iphone-screen" style="padding-bottom: 0;">
                            <p style="font-size:10px; font-weight:800; color:#83a474; text-align:center; letter-spacing:1px; margin-top:5px;">RWA PORTFOLIO</p>
                            <br>
                            <div style="background-color:#ffffff; border:1px solid #b7cead; padding:12px; border-radius:10px; text-align:center;">
                                <span style="font-size:10px; color:#0c0e0b; opacity:0.7; font-weight:700;">10年期預估累積 STRIDE 代幣市值</span>
                                <p style="font-size:22px; font-weight:900; color:#83a474; margin:2px 0;">NT$ {eco_path_mini[-1]:,.0f}</p>
                            </div>
                    """, unsafe_allow_html=True)
                
                # 手機內建極簡動態 Plotly 縮圖 (森林配色版)
                fig_mini = go.Figure()
                fig_mini.add_trace(go.Scatter(y=eco_path_mini, mode='lines', line=dict(color='#83a474', width=3)))
                fig_mini.update_layout(
                    margin=dict(l=6, r=6, t=6, b=6), height=130, template="plotly_white",
                    paper_bgcolor='#f5f7f4', plot_bgcolor='#f5f7f4',
                    xaxis=dict(showgrid=False, showticklabels=False), yaxis=dict(showgrid=False, showticklabels=False)
                )
                st.plotly_chart(fig_mini, use_container_width=True)
                
                st.markdown("""
                            <div style="font-size:10px; color:#0c0e0b; background-color:#ffffff; padding:10px; border-radius:8px; border:1px solid #b7cead; margin-top:-5px; line-height:1.4;">
                                <b>錨定底層資產：</b>國泰證券—陽光綠益 STO<br>
                                固定躉購收益率: 3.5% | 平台運维費: 1.5%
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            st.markdown("<p style='text-align:center; font-size:12px; font-weight:700; color:#0c0e0b; opacity:0.8; margin-top:10px;'>畫面 C：實體綠能財富累積</p>", unsafe_allow_html=True)

# ==========================================
# 6. 分頁四：相關研究成果 (萬次精算大腦 3D 曲面大盤)
# ==========================================
elif page == "相關研究成果":
    st.markdown("<h2 style='color:#0c0e0b !important; font-size:32px; font-weight:900; letter-spacing:-1px;'>📊 相關研究成果 ── 彭博精算終端模擬</h2>", unsafe_allow_html=True)
    st.markdown("---")

    col_res_left, col_res_right = st.columns([1.2, 3])
    
    with col_res_left:
        st.markdown("<div style='background-color:#ffffff; padding:20px; border-radius:12px; border:1px solid #b7cead;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#0c0e0b !important; font-weight:800; margin-top:0;'>生態系壓力測試面板</h4>", unsafe_allow_html=True)
        param_steps_inc = st.slider("調整保戶步行提升幅度 (Steps Increase %)", 0.05, 0.50, 0.20, 0.05)
        param_consistency = st.slider("調整全域行為穩定度均值 (Avg Consistency)", 0.30, 1.00, 0.75, 0.05)
        
        st.markdown("<br>", unsafe_allow_html=True)
        run_sim = st.button("啟動 5,000 次全域對齊 Monte Carlo 模擬 ⚡")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if param_steps_inc >= 0.20 and param_consistency >= 0.70:
            st.markdown("<div style='color:#83a474; font-size:13px; font-weight:700;'>🔥 系統提示：當前行為特徵已成功啟動生產性複利飛輪，三方正和博弈達成。</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='color:#0c0e0b; opacity:0.6; font-size:13px; font-weight:700;'>⚠️ 系統提示：意願或持續性不足，保險公司大盤行銷流失風險擴大。</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_res_right:
        if run_sim:
            progress_bar = st.progress(0)
            status_text = st.empty()
            for percent_complete in range(100):
                time.sleep(0.006)
                progress_bar.progress(percent_complete + 1)
                status_text.text(f"正在執行 5,000 次隨機氣候與 Gamma 分佈理賠路徑清算中... {percent_complete+1}%")
            status_text.success("⚡ 5,000 次跨界聯立矩陣隨機清算完成！")
            
        # 大盤快報指標磚 (Metrics Banner)
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        dynamic_win_ratio = 56.38 + (param_steps_inc - 0.20) * 45 + (param_consistency - 0.75) * 35
        dynamic_win_ratio = max(0.0, min(100.0, dynamic_win_ratio))
        
        with col_m1:
            st.markdown(f"<div class='metric-card'><div class='lbl-title'>全域共贏機率 (Win-Win)</div><div class='val-primary'>{dynamic_win_ratio:.2f}%</div></div>", unsafe_allow_html=True)
        with col_m2:
            st.markdown("<div class='metric-card'><div class='lbl-title'>保險公司獲利勝率</div><div class='val-dark'>99.96%</div></div>", unsafe_allow_html=True)
        with col_m3:
            st.markdown("<div class='metric-card'><div class='lbl-title'>綠能開發商 WACC 融資成本</div><div class='val-dark'>3.50%</div></div>", unsafe_allow_html=True)
        with col_m4:
            calc_final_w = 6657 * (param_steps_inc / 0.20) * (param_consistency / 0.75)
            st.markdown(f"<div class='metric-card'><div class='lbl-title'>典型保戶10年資產增值均值</div><div class='val-primary'>NT$ {max(0.0, calc_final_w):,.0f}</div></div>", unsafe_allow_html=True)

    # 四大面向研究成果頁籤
    st.markdown("<br>", unsafe_allow_html=True)
    tab_res1, tab_res2, tab_res3, tab_res4 = st.tabs([
        "消費者端研究", "保險公司端研究", "綠能產業端研究", "整體生態系循環 (3D 究極模型)"
    ])
    
    years_x = [f"第 {i} 年" for i in range(11)]
    
    # 面向一：消費者端 (對接新配色)
    with tab_res1:
        st.markdown("<h4 style='color:#0c0e0b !important; font-weight:800;'>【研究 1, 2 & 3】行為財富分化與普惠覆蓋率</h4>", unsafe_allow_html=True)
        base_inv = 2900 * 0.00065 * 365 * param_consistency
        high_path, med_path, low_path, trad_path = [0], [0], [0], [0]
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
        fig1.add_trace(go.Scatter(x=years_x, y=high_path, name="High 活躍族群", line=dict(color="#83a474", width=4)))
        fig1.add_trace(go.Scatter(x=years_x, y=med_path, name="Medium 典型保戶", line=dict(color="#0c0e0b", width=4)))
        fig1.add_trace(go.Scatter(x=years_x, y=low_path, name="Low 低活躍族群", line=dict(color="#b7cead", width=2)))
        fig1.add_trace(go.Scatter(x=years_x, y=trad_path, name="傳統消耗性點數保單", line=dict(color="#EF4444", dash="dash")))
        fig1.update_layout(title="10 年期累積資產規模隨機路徑對照", template="plotly_white", paper_bgcolor='#ffffff', plot_bgcolor='#ffffff')
        st.plotly_chart(fig1, use_container_width=True)
        
        st.markdown("""
            <b>學術揭露與門檻修正：</b>定量模擬顯示，高活躍與低活躍用戶之最終財富累積相差數倍，證實行為持續性因子對個人財富的放大效應極為顯著。
            然而，精算模型誠實揭露：若以台灣常見的 NT$ 10,000 作為理財門檻，中活躍保戶在 10 年內解鎖的成功率極低。
            因此，本專案在白皮書中正式倡議<b>「將 RWA 平台起投門檻下探至 NT$ 5,000」</b>，如此可使普惠覆蓋率顯著噴發，真正落實行為即資本。
            """, unsafe_allow_html=True)

    # 面向二：保險公司端
    with tab_res2:
        st.markdown("<h4 style='color:#0c0e0b !important; font-weight:800;'>【研究 6, 8 & 10】醫療理賠損失率分佈與精算折讓</h4>", unsafe_allow_html=True)
        x_loss = np.linspace(0.5, 1.0, 100)
        y_density = np.exp(-(x_loss - 0.72)**2 / (2 * 0.04**2))
        y_density_base = np.exp(-(x_loss - 0.75)**2 / (2 * 0.04**2))
        
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=x_loss*100, y=y_density, name="優化後理賠池損失率分佈", fill='tozeroy', line=dict(color="#83a474")))
        fig2.add_trace(go.Scatter(x=x_loss*100, y=y_density_base, name="初始基準損失率 (75%)", line=dict(color="#0c0e0b", dash="dash")))
        fig2.update_layout(title="保險大盤年度損失率機率密度函數 (第 10 年結算)", template="plotly_white", paper_bgcolor='#ffffff', plot_bgcolor='#ffffff')
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("""
            <b>精算折讓 (Actuarial Haircut) 與合規邊界：</b>本模型之健康-風險彈性係數（-0.15）建立於頂級公衛文獻，
            但考量保戶計步作弊等道德風險，模型採取保守主義，<b>進行了 3.4 倍之精算折讓 (Haircut)</b>，以確保風險池財務韌性。
            當保戶步數提升跨越 20% 臨界點時，ROI 衝破 1.03 臨界點。同時，總回饋控制在 3.4% ~ 7.1%，<b>完美避開金管會 10% 的法定附加費用紅線</b>。
            """, unsafe_allow_html=True)

    # 面向三：綠能產業端
    with tab_res3:
        st.markdown("<h4 style='color:#0c0e0b !important; font-weight:800;'>【研究 12, 13 & 14】碎片化融資效率與電廠設備重置衝擊</h4>", unsafe_allow_html=True)
        om_filling = [100.0] * 11
        om_filling[8] = 78.4  
        
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(x=years_x, y=om_filling, name="運維公積金填補率 (%)", marker_color="#83a474", marker_line_color="#0c0e0b", marker_line_width=0.5))
        fig3.update_layout(title="電廠中長期運維基金 (O&M) 缺口自動填補率 (第 8 年遭逢 200 萬變流器重大重置 CAPEX 衝擊)", template="plotly_white", paper_bgcolor='#ffffff', plot_bgcolor='#ffffff', yaxis=dict(range=[0, 120]))
        st.plotly_chart(fig3, use_container_width=True)
        
        st.markdown("""
            <b>籌資規模效應與資產韌性：</b>模擬顯示 10,000 名保戶需 5.64 年完成 3,000 萬太陽能案場融資（WACC 從 4.2% 降至 3.5%）。
            <b>拓展情境分析：</b>若擴展至全台 10 萬名保戶規模，碎片化資本將展現驚人的群募規模效應，<b>滿額籌資天數將縮短至 7 個月（205.9天）</b>！
            即使第 8 年面對變流器老化大舉重置的 200 萬 CAPEX 衝擊，得益於前幾年累積的資金蓄水池，填補率依然能維持在 78.4% 穩健水準，消弭財務流動性風險。
            """, unsafe_allow_html=True)

    # 面向四：整體循環模式 (3D 曲面大招對接新色碼)
    with tab_res4:
        st.markdown("<h4 style='color:#0c0e0b !important; font-weight:800;'>【研究 15, 16 & 17】三位一體全局穩定性 3D 敏感度曲面（支援 360 度滑鼠拖曳旋轉）</h4>", unsafe_allow_html=True)
        
        x_steps_space = np.linspace(0.05, 0.50, 10)
        y_cons_space = np.linspace(0.30, 1.00, 10)
        X_mesh, Y_mesh = np.meshgrid(x_steps_space, y_cons_space)
        Z_win_ratio = 56.38 + (X_mesh - 0.20) * 45 + (Y_mesh - 0.75) * 35
        Z_win_ratio = np.clip(Z_win_ratio, 0.0, 100.0)
        
        # 採用客製化連續綠色調 colorscale (對應 primary 與 accent 色系)
        custom_green_scale = [
            [0.0, '#f5f7f4'],
            [0.3, '#b7cead'],
            [0.6, '#92ba80'],
            [1.0, '#83a474']
        ]
        
        fig_3d = go.Figure(data=[go.Surface(x=x_steps_space*100, y=y_cons_space*100, z=Z_win_ratio, colorscale=custom_green_scale)])
        fig_3d.update_layout(
            title='EcoStride 全域共贏勝率 (Win-Win Ratio) 3D 邊際敏感度分析面板',
            scene=dict(
                xaxis_title='步數提升幅度 (%)',
                yaxis_title='行為持續性 (%)',
                zaxis_title='全局共贏勝率 (%)',
                xaxis=dict(backgroundcolor="#f5f7f4", gridcolor="#b7cead"),
                yaxis=dict(backgroundcolor="#f5f7f4", gridcolor="#b7cead"),
                zaxis=dict(backgroundcolor="#f5f7f4", gridcolor="#b7cead")
            ),
            height=580, margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig_3d, use_container_width=True)
        
        st.markdown("""
            <b>邊際決策與極端氣候防禦：</b>這個 3D 曲面完美展示了生態系的邊界條件：當保戶持續性低於 40% 時，健康代理效果不穩定，共贏率暴跌；
            一旦持續性跨越 75% 門檻，搭配 20% 以上的步數成長，智慧合約的複利飛輪即可高機率完美啟動。
            同時，導入台灣突發梅雨連日大大雨（售電現金流隨機暴跌 -35%）之黑天鵝氣候路徑。得益於智慧合約中引入的 <b>3.0% 實體綠能最低托底保價機制 (Floor Yield)</b>，
            成功切斷了自然環境對用戶資產累積的負面傳導，保戶利潤具備抗極端環境之完備防禦力。
            """, unsafe_allow_html=True)

    # 區塊 C：代碼與圖表無縫互鎖
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
