# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 데이터 정의
data = {
    "국가": ["South Korea", "USA", "Germany", "India", "Nigeria", "Japan", "Brazil", "China"],
    "FTO_빈도": [0.12, 0.45, 0.42, 0.31, 0.05, 0.11, 0.32, 0.13],
    "TCF7L2_빈도": [0.28, 0.38, 0.35, 0.39, 0.41, 0.30, 0.34, 0.29],
    "기본_비만률": [5.3, 36.2, 22.3, 4.0, 8.9, 4.3, 22.1, 6.2],
    "기본_당뇨병률": [8.2, 10.5, 9.5, 8.9, 4.5, 7.4, 10.1, 9.1],
}
df = pd.DataFrame(data)

# Streamlit UI
st.set_page_config(page_title="질병 예측 시뮬레이션", layout="wide")
st.title("🧬 유전형 기반 국가별 질병 위험 시뮬레이션")

st.markdown("당신이 보유한 유전자를 선택하면, 국가별 비만률/당뇨병률 예측 결과를 시뮬레이션합니다.")

# 유전형 입력
col1, col2 = st.columns(2)
with col1:
    user_fto = st.selectbox("FTO 유전자 (비만 관련)", ["비보유", "보유"])
with col2:
    user_tcf = st.selectbox("TCF7L2 유전자 (당뇨병 관련)", ["비보유", "보유"])

# 위험계수
risk_factor_fto = 1.67 if user_fto == "보유" else 1.0
risk_factor_tcf = 1.45 if user_tcf == "보유" else 1.0

# 시뮬레이션 계산
df["예상_비만률(%)"] = (df["기본_비만률"] * (risk_factor_fto * df["FTO_빈도"] + (1 - df["FTO_빈도"]))).round(2)
df["예상_당뇨병률(%)"] = (df["기본_당뇨병률"] * (risk_factor_tcf * df["TCF7L2_빈도"] + (1 - df["TCF7L2_빈도"]))).round(2)

# 결과 출력
st.subheader("📊 국가별 예측 결과")
st.dataframe(df[["국가", "예상_비만률(%)", "예상_당뇨병률(%)"]].sort_values("예상_비만률(%)", ascending=False))

# 시각화
st.subheader("🌍 예측 결과 시각화")

tab1, tab2 = st.tabs(["비만률 예측 맵", "당뇨병률 예측 맵"])

with tab1:
    fig1 = px.bar(df.sort_values("예상_비만률(%)", ascending=False),
                  x="국가", y="예상_비만률(%)", color="예상_비만률(%)",
                  title="국가별 예상 비만률", labels={"예상_비만률(%)": "예상 비만률 (%)"})
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.bar(df.sort_values("예상_당뇨병률(%)", ascending=False),
                  x="국가", y="예상_당뇨병률(%)", color="예상_당뇨병률(%)",
                  title="국가별 예상 당뇨병률", labels={"예상_당뇨병률(%)": "예상 당뇨병률 (%)"})
    st.plotly_chart(fig2, use_container_width=True)

