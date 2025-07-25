import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="연령별 인구 시각화", layout="wide")

st.title("📊 서울특별시 연령별 인구 현황 (2025년 6월)")

# CSV 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드 (예: 2025년 연령별 인구 현황)", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    try:
        # 서울특별시 전체 데이터만 추출
        df_seoul = df[df["행정구역"].str.contains("서울특별시")].iloc[0]

        # 연령별 인구 컬럼만 추출
        age_columns = [col for col in df.columns if "계_" in col and "세" in col]
        age_labels = [col.split("_")[-1] for col in age_columns]

        # 문자열 숫자에서 쉼표 제거 후 정수형 변환
        age_values = df_seoul[age_columns].apply(lambda x: x.replace(",", "", regex=True)).astype(int).values.flatten()

        # 시각화용 데이터프레임 구성
        df_plot = pd.DataFrame({"연령": age_labels, "인구 수": age_values})

        # Plotly 시각화
        fig = px.bar(
            df_plot,
            x="연령",
            y="인구 수",
            title="서울특별시 연령별 인구 분포",
            labels={"연령": "연령", "인구 수": "인구 수"},
            template="plotly_white",
            color="인구 수"
        )
        fig.update_layout(xaxis_tickangle=-45)

        # 출력
        st.plotly_chart(fig, use_container_width=True)

        with st.expander("📋 연령별 인구 데이터 보기"):
            st.dataframe(df_plot, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ 데이터 처리 중 오류 발생: {e}")

else:
    st.info("좌측에서 연령별 인구 CSV 파일을 업로드하세요.")
