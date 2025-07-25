
# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 데이터 준비
data = {
    "국가": ["South Korea", "USA", "Germany", "India", "Nigeria", "Japan", "Brazil", "China"],
    "지역": ["East Asia", "North America", "Europe", "South Asia", "Africa", "East Asia", "South America", "East Asia"],
    "FTO_빈도": [0.12, 0.45, 0.42, 0.31, 0.05, 0.11, 0.32, 0.13],
    "TCF7L2_빈도": [0.28, 0.38, 0.35, 0.39, 0.41, 0.30, 0.34, 0.29],
    "비만률(%)": [5.3, 36.2, 22.3, 4.0, 8.9, 4.3, 22.1, 6.2],
    "당뇨병률(%)": [8.2, 10.5, 9.5, 8.9, 4.5, 7.4, 10.1, 9.1],
    "고혈압률(%)": [28.0, 33.0, 30.2, 25.1, 23.4, 27.5, 32.8, 29.7]
}
df = pd.DataFrame(data)

st.set_page_config(page_title="유전자-질병 국가 통계 분석", layout="wide")
st.title("🌍 국가별 유전자 빈도와 질병 유병률 분석")

# --- 1. 국가 선택 및 정보 표시 ---
st.header("📌 국가 정보 확인")
selected_country = st.selectbox("국가를 선택하세요", df["국가"])
info = df[df["국가"] == selected_country].iloc[0]

st.markdown(f"""
**지역**: {info['지역']}  
**FTO 유전자 빈도**: {info['FTO_빈도']}  
**TCF7L2 유전자 빈도**: {info['TCF7L2_빈도']}  
**비만률**: {info['비만률(%)']}%  
**당뇨병률**: {info['당뇨병률(%)']}%  
**고혈압률**: {info['고혈압률(%)']}%
""")

# --- 2. 시각화 섹션 ---
st.header("📊 유전자 빈도 vs 질병 유병률 시각화")

col1, col2 = st.columns(2)

with col1:
    fig1 = px.scatter(df, x="FTO_빈도", y="비만률(%)", text="국가",
                      title="FTO 빈도 vs 비만률",
                      labels={"FTO_빈도": "FTO 유전자 빈도", "비만률(%)": "비만률(%)"})
    fig1.update_traces(textposition='top center')
    st.plotly_chart(fig1, use_container_width=True)

    corr_fto = np.corrcoef(df["FTO_빈도"], df["비만률(%)"])[0, 1]
    st.info(f"**상관계수(FTO vs 비만률)**: {corr_fto:.2f}")

with col2:
    fig2 = px.scatter(df, x="TCF7L2_빈도", y="당뇨병률(%)", text="국가",
                      title="TCF7L2 빈도 vs 당뇨병률",
                      labels={"TCF7L2_빈도": "TCF7L2 유전자 빈도", "당뇨병률(%)": "당뇨병률(%)"})
    fig2.update_traces(textposition='top center')
    st.plotly_chart(fig2, use_container_width=True)

    corr_tcf = np.corrcoef(df["TCF7L2_빈도"], df["당뇨병률(%)"])[0, 1]
    st.info(f"**상관계수(TCF7L2 vs 당뇨병률)**: {corr_tcf:.2f}")
