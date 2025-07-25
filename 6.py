# 유전적 위험 점수 계산
df["FTO_위험점수"] = (df["FTO_빈도"] * risk_factor_fto).round(2)
df["TCF7L2_위험점수"] = (df["TCF7L2_빈도"] * risk_factor_tcf).round(2)

# 예측 비만/당뇨 수치 생성
df["예상_비만률(%)"] = (df["기본_비만률"] * df["FTO_위험점수"]).round(2)
df["예상_당뇨병률(%)"] = (df["기본_당뇨병률"] * df["TCF7L2_위험점수"]).round(2)

# 세계 평균과 비교
mean_obesity = df["예상_비만률(%)"].mean()
mean_diabetes = df["예상_당뇨병률(%)"].mean()

df["비만_평균초과여부"] = df["예상_비만률(%)"].apply(lambda x: "⬆ 초과" if x > mean_obesity else "⬇ 이하")
df["당뇨_평균초과여부"] = df["예상_당뇨병률(%)"].apply(lambda x: "⬆ 초과" if x > mean_diabetes else "⬇ 이하")

# 위험 등급
def 위험등급(score):
    if score > 35: return "🔴 High"
    elif score > 20: return "🟠 Medium"
    else: return "🟢 Low"

df["비만_등급"] = df["예상_비만률(%)"].apply(위험등급)
df["당뇨_등급"] = df["예상_당뇨병률(%)"].apply(위험등급)

# 확장 테이블 출력
st.subheader("📌 확장된 국가별 유전형 기반 질병 예측 테이블")
st.dataframe(df[[
    "국가", "FTO_위험점수", "TCF7L2_위험점수",
    "예상_비만률(%)", "비만_등급", "비만_평균초과여부",
    "예상_당뇨병률(%)", "당뇨_등급", "당뇨_평균초과여부"
]])
