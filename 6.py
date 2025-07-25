import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -------------------
# 1. 데이터 정의
# -------------------
df = pd.DataFrame({
    "국가": ["South Korea", "USA", "Germany", "India", "Nigeria", "Japan", "Brazil", "China"],
    "FTO_빈도": [0.12, 0.45, 0.42, 0.31, 0.05, 0.11, 0.32, 0.13],
    "TCF7L2_빈도": [0.28, 0.38, 0.35, 0.39, 0.41, 0.30, 0.34, 0.29],
    "기본_비만률": [5.3, 36.2, 22.3, 4.0, 8.9, 4.3, 22.1, 6.2],
    "기본_당뇨병률": [8.2, 10.5, 9.5, 8.9, 4.5, 7.4, 10.1, 9.1]
})

# -------------------
# 2. Streamlit UI
# -------------------
st.set_page_config(page_title="유전형 기반 질병 리스크 맵", layout="wide")
st.title("🧬 유전형 기반 국가별 질병 위험 시뮬레이션")

st.markdown("당신이 보유한 유전자를 선택하면, 국가별 비만률과 당뇨병률을 예측할 수 있습니다.")

col1, col2 = st.columns(2)
with col1:
    user_fto = st.selectbox("FTO 유전자 보유 여부 (비만 관련)", ["비보유", "보유"])
with col2:
    user_tcf = st.selectbox("TCF7L2 유전자 보유 여부 (당뇨 관련)", ["비보유", "보유"])

# -------------------
# 3. 유전자 위험 가중치 설정
# -------------------
risk_factor_fto = 1.67 if user_fto == "보유" else 1.0
risk_factor_tcf = 1.45 if user_tcf == "보유" else 1.0

# -------------------
# 4. 계산: 위험 점수 & 예측
# -------------------
df["FTO_위험점수"] = (df["FTO_빈도"] * risk_factor_fto).round(2)
df["TCF7L2_위험점수"] = (df["TCF7L2_빈도"] * risk_factor_tcf).round(2)

df["예상_비만률(%)"] = (df["기본_비만률"] * df["FTO_위험점수"]).round(2)
df["예상_당뇨병률(%)"] = (df["기본_당뇨병률"] * df["TCF7L2_위험점수"]).round(2)

# -------------------
# 5. 위험 등급 및 평균 비교
# -------------------
mean_obesity = df["예상_비만률(%)"].mean()
mean_diabetes = df["예상_당뇨병률(%)"].mean()

df["비만_평균초과여부"] = df["예상_비만률(%)"].apply(lambda x: "⬆ 초과" if x > mean_obesity else "⬇ 이하")
df["당뇨_평균초과여부"] = df["예상_당뇨병률(%)"].apply(lambda x: "⬆ 초과" if x > mean_diabetes else "⬇ 이하")

def 위험등급(score):
    if score > 35: return "🔴 High"
    elif score > 20: return "🟠 Medium"
    else: return "🟢 Low"

df["비만_등급"] = df["예상_비만률(%)"].apply(위험등급)
df["당뇨_등급"] = df["예상_당뇨병률(%)"].apply(위험등급)

# -------------------
# 6. 결과 표 출력
# -------------------
st.subheader("📋 국가별 질병 위험 예측 결과")

st.dataframe(df[[
    "국가", "FTO_위험점수", "TCF7L2_위험점수",
    "예상_비만률(%)", "비만_등급", "비만_평균초과여부",
    "예상_당뇨병률(%)", "당뇨_등급", "당뇨_평균초과여부"
]])

# -------------------
# 7. 시각화
# -------------------
st.subheader("📊 국가별 질병 위험 시각화")

tab1, tab2 = st.tabs(["비만률 예측", "당뇨병률 예측"])

with tab1:
    fig1 = px.bar(df.sort_values("예상_비만률(%)", ascending=False),
                  x="국가", y="예상_비만률(%)", color="비만_등급",
                  title="국가별 예상 비만률", labels={"예상_비만률(%)": "예상 비만률 (%)"})
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    fig2 = px.bar(df.sort_values("예상_당뇨병률(%)", ascending=False),
                  x="국가", y="예상_당뇨병률(%)", color="당뇨_등급",
                  title="국가별 예상 당뇨병률", labels={"예상_당뇨병률(%)": "예상 당뇨병률 (%)"})
    st.plotly_chart(fig2, use_container_width=True)
