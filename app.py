import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# --- 頁面基本配置 ---
st.set_page_config(page_title="EcoStride | 永續金融生態系", layout="wide")

# --- 自定義 CSS (讓畫面更精緻) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #161b22; padding: 20px; border-radius: 15px; border: 1px solid #30363d; }
    h1, h2, h3 { color: #10b981 !important; font-family: 'Noto Sans TC', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# --- 側邊欄導覽 ---
with st.sidebar:
    st.title("🌿 EcoStride")
    st.markdown("---")
    menu = st.radio("功能選單", ["提案動機與機制", "使用者界面展示", "研究模擬成果"])
    st.markdown("---")
    st.info("專題成員：蔡宜伶、賀舜禹、曾琬甯")

# --- 分頁一：提案動機與機制 ---
if menu == "提案動機與機制":
    st.title("💡 提案動機與運作機制")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("🎯 痛點：激勵失效")
        st.write("傳統外溢保單的一次性獎勵（如咖啡券）具備明顯消耗性，難以產生資產複利感，保戶動力易隨時間遞減。")
    with col2:
        st.subheader("🛡️ 改良：RWA 背書")
        st.write("借鏡 STEPN 模式但切斷死亡螺旋。資產錨定太陽能售電收益權，確保代幣具備實體生產力支撐。")
    with col3:
        st.subheader("🌍 目標：普惠金融")
        st.write("打破綠能投資的高門檻。透過碎片化技術，讓年輕族群的「生物行為」直接轉化為長期資本。")

    st.markdown("---")
    st.header("🔄 三位一體循環模型")
    st.write("我們建立了一個由「用戶端、保險公司、綠能產業」組成的價值閉環：")
    st.markdown("""
    1. **用戶端**：提供健康步行數據 $\rightarrow$ 獲取 RWA 收益權份額。
    2. **保險公司**：投入理賠預防費用 $\rightarrow$ 降低整體風險池損失率。
    3. **綠能產業**：獲取碎片化低成本資金 $\rightarrow$ 支付固定售電回報。
    """)

# --- 分頁二：使用者界面展示 ---
elif menu == "使用者界面展示":
    st.title("📱 使用者界面展示 (UI/UX)")
    st.write("我們設計了三個核心功能介面，強化「行為即資產」的視覺回饋。")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### **1. 用戶儀表板**")
        st.image("https://img.icons8.com/clouds/500/walking.png", width=150)
        st.write("**核心：今日步數與補貼**")
        st.write("顯示即時步數、達成率，以及換算後的當日 RWA 投資補貼（NT$ 1.625/天）。")
    with c2:
        st.markdown("### **2. 精算風險面板**")
        st.image("https://img.icons8.com/clouds/500/safety-shield.png", width=150)
        st.write("**核心：穩定度與保費減免**")
        st.write("展示行為持續性因子 (Consistency) 與預期次年保費折減率。")
    with c3:
        st.markdown("### **3. RWA 透明數據庫**")
        st.image("https://img.icons8.com/clouds/500/solar-panel.png", width=150)
        st.write("**核心：案場透視**")
        st.write("展示底層太陽能案場即時發電收益與 3.5% 的固定回報率。")

# --- 分頁三：研究模擬成果 ---
elif menu == "研究模擬成果":
    st.title("📊 研究模擬成果：Monte Carlo 模擬")
    st.write("本頁面重現了我們在專題中使用的 Python 模擬引擎。")

    # 側邊調整參數
    with st.expander("🛠️ 調整模擬參數", expanded=True):
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            input_steps = st.slider("保戶每日平均步數", 5000, 15000, 7500, 500)
        with col_p2:
            input_cons = st.slider("行為持續性因子 (Consistency)", 0.3, 1.0, 0.7, 0.1)

    # 模擬運算邏輯 (引用同學的精算參數)
    def simulate_path(steps, consistency):
        alpha = 0.00065
        beta = 0.0001
        gamma = 0.20
        rwa_yield_base = 0.035
        mu_market = 0.05
        insurance_share = 0.25
        
        years = 10
        eco_wealth = [0]
        legacy_wealth = [0]
        curr_eco = 0
        curr_legacy = 0
        
        for y in range(1, years + 1):
            excess_steps = max(0, steps - 5000)
            # 引擎 A + B 資本注入
            annual_inv = (excess_steps * alpha + (excess_steps * beta * gamma)) * consistency * 365
            # RWA 複利滾存
            curr_eco = (curr_eco + annual_inv) * (1 + (rwa_yield_base * (1-insurance_share)) + mu_market)
            # 傳統點數累計 (考慮疲勞度)
            fatigue = max(0.2, 1.0 - 0.05 * np.log1p(y*365))
            curr_legacy += (excess_steps * 0.0005 * 365) * fatigue
            
            eco_wealth.append(curr_eco)
            legacy_wealth.append(curr_legacy)
        return eco_wealth, legacy_wealth

    eco_res, leg_res = simulate_path(input_steps, input_cons)

    # 數據指標展示
    m1, m2, m3 = st.columns(3)
    m1.metric("10年累積資產 (EcoStride)", f"NT$ {eco_res[-1]:,.0f}")
    m2.metric("傳統獎勵總價值", f"NT$ {leg_res[-1]:,.0f}")
    m3.metric("資產成長效益", f"{((eco_res[-1]/max(1,leg_res[-1]))-1)*100:.1f}%", delta="生產性累積")

    # 圖表展示
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(11)), y=eco_res, name="EcoStride (複利)", line=dict(color="#10b981", width=4)))
    fig.add_trace(go.Scatter(x=list(range(11)), y=leg_res, name="傳統方案 (線性)", line=dict(color="#64748b", dash='dash')))
    fig.update_layout(title="10年資產累積趨勢對照圖", template="plotly_dark", height=450)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ---
    ### 🛡️ 研究論證摘要
    1. **理賠節省效益**：經 10,000 次 Monte Carlo 模擬，保險公司獲利機率達 **99.96%**。
    2. **WACC 融資優勢**：綠能案場資金成本從 4.2% 降至 **3.5%**，顯著優於銀行貸款。
    3. **法規合規性**：獎勵成本佔保費比率控制在 **3.4% ~ 7.1%**，符合金管會 10% 紅線規範。
    """)
    st.link_button("📄 檢視完整 Google Colab 原始碼", "https://colab.research.google.com/drive/1FVdXkrON5mwvZ6HyVOujPzr07CSHQ-3e")
