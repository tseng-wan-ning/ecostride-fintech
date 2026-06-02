import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 1. 頁面基本配置 ---
st.set_page_config(
    page_title="EcoStride | 永續金融生態系",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. 自定義 CSS (提升精緻度) ---
st.markdown("""
    <style>
    /* 全局深色科技感 */
    .stApp { background-color: #0e1117; color: #ffffff; }
    
    /* 自定義卡片樣式 */
    .feature-card {
        background-color: #161b22;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #30363d;
        height: 100%;
    }
    
    /* 標題與字體 */
    h1, h2, h3 { color: #10b981 !important; font-family: 'Noto Sans TC', sans-serif; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 12px; border: 1px solid #30363d; }
    
    /* 手機 Mockup 樣式 */
    .phone-screen {
        background-color: #000000;
        border: 8px solid #30363d;
        border-radius: 30px;
        padding: 20px;
        height: 550px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 側邊欄導覽 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2964/2964514.png", width=80)
    st.title("EcoStride 導覽")
    st.markdown("---")
    page = st.radio(
        "選單切換",
        ["🏠 專案首頁", "💡 提案動機與模式", "📱 APP 介面展示", "📊 相關研究成果"]
    )
    st.markdown("---")
    st.write("組員：蔡宜伶、賀舜禹、曾琬甯")

# --- 4. 分頁邏輯 ---

# ==========================================
# 分頁一：專案首頁
# ==========================================
if page == "🏠 專案首頁":
    st.title("🌿 EcoStride")
    st.subheader("結合行為金融與實體資產代幣化之永續金融生態系模式研究")
    
    st.markdown("---")
    
    col_hero1, col_hero2 = st.columns([2, 1])
    with col_hero1:
        st.markdown("""
        ### **讓健康行為，成為你的綠色資產**
        這是一個針對傳統外溢保單痛點所設計的新型金融模式。我們將保戶的健康步行數據透過區塊鏈技術，
        直接對接實體綠能案場的收益權 (RWA)，解決了獎勵效用遞減的問題，同時實踐普惠金融。
        
        **核心三元素：**
        1. **行為金融學**：解決雙曲貼現導致的運動惰性。
        2. **RWA 代幣化**：將實體售電收益轉化為數位資產。
        3. **永續金融**：創造保戶、保險公司、綠能業者三方共贏。
        """)
        if st.button("了解更多動機 ➔"):
            st.info("請點選左側選單的『提案動機與模式』")
    
    with col_hero2:
        st.image("https://img.icons8.com/clouds/500/natural-user-interface.png")

# ==========================================
# 分頁二：提案動機與模式
# ==========================================
elif page == "💡 提案動機與模式":
    st.title("💡 為什麼我們要做 EcoStride？")
    
    tab1, tab2 = st.tabs(["核心痛點分析", "生態系機制介紹"])
    
    with tab1:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.error("📉 **外溢保單激勵失效**")
            st.write("傳統咖啡券獎勵具備『一次性效用』。根據行為金融學，保戶對遠期回饋感到疲勞，導致誘因強度快速遞減。")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.warning("⚠️ **Web3 龐氏教訓**")
            st.write("STEPN 等 M2E 模式缺乏實體資產 (RWA) 背書。EcoStride 錨定實體綠能售電收益，確保資產內在價值。")
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="feature-card">', unsafe_allow_html=True)
            st.success("💰 **高品質資產隔離**")
            st.write("高品質綠能資產門檻高 (NT$ 100萬+)。我們透過碎片化技術，讓年輕世代僅靠步行即可參與綠能紅利。")
            st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.header("🔄 三位一體價值流動模型")
        st.markdown("""
        本專案建立了一個用戶、保險公司與綠能產業間的閉環流動模型：
        
        1. **用戶端**：提供經驗證之健康數據，交換實體資產代幣化 (RWA) 收益權，實現複利累積。
        2. **保險公司端**：投入理賠準備金折現資金作為種子金，優化保戶健康品質，降低理賠損失率。
        3. **綠能產業端**：提供具備現金流之再生能源資產，獲取去中心化、低成本之建設資金。
        """)
        st.image("https://raw.githubusercontent.com/Yiling-Tsai/Fintech-Project/main/eco_loop.png", caption="EcoStride 運作機制示意圖")

# ==========================================
# 分頁三：APP 介面展示
# ==========================================
elif page == "📱 APP 介面展示":
    st.title("📱 EcoStride 使用者界面展示")
    st.write("我們將繁瑣的金融精算轉化為直觀的「資產成長」視覺反饋。")
    
    ui_col1, ui_col2, ui_col3 = st.columns(3)
    
    with ui_col1:
        st.markdown("""
        <div class="phone-screen">
            <p style="color:#10b981; font-weight:bold; text-align:center;">User Dashboard</p>
            <h1 style="text-align:center; font-size:40px;">7,500</h1>
            <p style="text-align:center; font-size:12px; color:gray;">TODAY'S STEPS</p>
            <hr>
            <div style="background:#161b22; padding:15px; border-radius:10px;">
                <p style="font-size:10px; color:#10b981;">今日預計補貼</p>
                <p style="font-size:20px; font-weight:bold;">NT$ 1.625</p>
            </div>
            <p style="font-size:10px; color:gray; margin-top:20px;">已達成每日目標 150%</p>
        </div>
        """, unsafe_allow_html=True)
        st.caption("畫面 A：每日步行與資本生成看板")

    with ui_col2:
        st.markdown("""
        <div class="phone-screen">
            <p style="color:#3b82f6; font-weight:bold; text-align:center;">Actuarial Panel</p>
            <div style="margin-top:40px;">
                <p style="font-size:10px; color:gray;">行為穩定度 (Consistency)</p>
                <h3 style="color:white !important;">0.7 (中活躍)</h3>
            </div>
            <div style="margin-top:20px; background:#1e293b; padding:15px; border-radius:10px;">
                <p style="font-size:10px; color:#3b82f6;">預計明年保費減免</p>
                <p style="font-size:24px; font-weight:bold;">5.2%</p>
            </div>
            <p style="font-size:10px; color:gray; margin-top:100px;">*數據由零知識證明 (ZKP) 保護驗證</p>
        </div>
        """, unsafe_allow_html=True)
        st.caption("畫面 B：風險精算與保費反饋介面")

    with ui_col3:
        st.markdown("""
        <div class="phone-screen">
            <p style="color:#f59e0b; font-weight:bold; text-align:center;">RWA Portfolio</p>
            <div style="background:#451a03; padding:15px; border-radius:10px; margin-top:30px;">
                <p style="font-size:10px; color:#fbbf24;">當前累積 STRIDE 資產</p>
                <p style="font-size:22px; font-weight:bold;">NT$ 15,721</p>
            </div>
            <div style="margin-top:20px; font-size:12px;">
                <p>● 案場 A (陽光綠益): 發電中</p>
                <p>● 當期收益率: 3.5%</p>
                <p>● 資本利得預估: 5.0%</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("畫面 C：實體資產與累積財富面板")

# ==========================================
# 分頁四：相關研究成果
# ==========================================
elif page == "📊 相關研究成果":
    st.title("📊 相關研究成果與模擬")
    st.write("本模擬重現了我們專題研究中的核心精算邏輯。")

    # --- 模擬參數調整 (由同學的 Python 邏輯支持) ---
    with st.expander("🛠️ 調整模擬參數", expanded=True):
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            steps_input = st.slider("保戶每日平均步數", 5000, 15000, 7500, 500)
        with col_p2:
            cons_input = st.slider("行為持續性因子 (Consistency)", 0.3, 1.0, 0.7, 0.1)

    # --- 同學提供的精算模擬核心引擎 ---
    def simulate_path(steps, consistency):
        # 參數對齊企劃書
        alpha = 0.00065
        beta = 0.0001
        gamma = 0.20
        yield_base = 0.035
        capital_gain = 0.05
        insurance_share = 0.25
        
        years = 10
        eco_wealth = [0]
        legacy_wealth = [0]
        curr_eco = 0
        curr_legacy = 0
        
        for y in range(1, years + 1):
            excess_steps = max(0, steps - 5000)
            # 引擎 A + B 資本流入
            daily_inv = (excess_steps * alpha + (excess_steps * beta * gamma)) * consistency
            annual_inv = daily_inv * 365
            
            # RWA 複利滾存：(資產 + 投入) * (1 + 淨收益 + 資本利得)
            curr_eco = (curr_eco + annual_inv) * (1 + (yield_base * (1 - insurance_share)) + capital_gain)
            
            # 傳統方案：線性累計點數 (考量 5% 疲勞感衰減)
            fatigue = max(0.2, 1.0 - 0.05 * np.log1p(y * 365))
            curr_legacy += (excess_steps * 0.0005 * 365) * fatigue
            
            eco_wealth.append(curr_eco)
            legacy_wealth.append(curr_legacy)
            
        return eco_wealth, legacy_wealth

    eco_res, leg_res = simulate_path(steps_input, cons_input)

    # 指標面板
    m1, m2, m3 = st.columns(3)
    m1.metric("10年累積資產 (EcoStride)", f"NT$ {eco_res[-1]:,.0f}")
    m2.metric("傳統點數累計價值", f"NT$ {leg_res[-1]:,.0f}")
    m3.metric("資產增值效益", f"{((eco_res[-1]/max(1,leg_res[-1]))-1)*100:.1f}%", delta="生產性累積")

    # 圖表呈現
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(11)), y=eco_res, name="EcoStride (生產性複利)", line=dict(color="#10b981", width=4)))
    fig.add_trace(go.Scatter(x=list(range(11)), y=leg_res, name="傳統保單 (消耗性點數)", line=dict(color="#64748b", dash='dash')))
    fig.update_layout(title="10年期財富累積預測對比圖", template="plotly_dark", height=500, legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("📚 關鍵研究論證 (學術依據)")
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.write("""
        **1. 理賠損失率 (Loss Ratio) 降幅：**
        經 10,000 次 Monte Carlo 模擬，保戶步數提升 20% 情況下，理賠節省足以完全覆蓋投資成本，
        **保險公司獲利機率高達 99.96%**。
        
        **2. WACC 融資優勢：**
        相較於傳統銀行融資 WACC 4.2%，透過 EcoStride 吸收之資金成本僅 **3.5%**。
        """)
    with col_r2:
        st.write("""
        **3. 法規紅線遵從：**
        回饋總成本控制在保費的 **3.4% ~ 7.1%**，完美符合金管會 10% 之附加費用規範。
        
        **4. 普惠金融門檻：**
        透過碎片化技術，將原本百萬級的綠能投資門檻下探至零資本起點，
        讓中活躍用戶在 10 年內無痛累積逾 **NT$ 6,000** 之綠色資產。
        """)
    st.link_button("📄 檢視完整 Python 研究程式碼 (Google Colab)", "https://colab.research.google.com/drive/1FVdXkrON5mwvZ6HyVOujPzr07CSHQ-3e")
