import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="인구 피라미드", layout="wide")
st.title("🏛 서울특별시 인구 피라미드 (2025년 6월 기준)")

uploaded_file = st.file_uploader("남녀 구분 인구 CSV 업로드", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    try:
        # 서울특별시 전체 데이터
        df_seoul = df[df["행정구역"].str.contains("서울특별시")].iloc[0]

        # 남녀 연령별 열
        male_cols = [col for col in df.columns if "남_" in col and "세" in col]
        female_cols = [col for col in df.columns if "여_" in col and "세" in col]
        age_labels = [col.split("_")[-1] for col in male_cols]

        # 값 전처리
        male_values = df_seoul[male_cols].replace(",", "", regex=True)
        female_values = df_seoul[female_cols].replace(",", "", regex=True)

        male_values = pd.to_numeric(male_values, errors='coerce').fillna(0).astype(int)
        female_values = pd.to_numeric(female_values, errors='coerce').fillna(0).astype(int)

        # 피라미드용 음수 변환
        male_values = -male_values

        # 인구 피라미드 그리기
        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=age_labels,
            x=male_values,
            name="남성",
            orientation='h',
            marker_color='blue'
        ))

        fig.add_trace(go.Bar(
            y=age_labels,
            x=female_values,
            name="여성",
            orientation='h',
            marker_color='deeppink'
        ))

        fig.update_layout(
            title="서울특별시 연령별 인구 피라미드 (남녀 구분)",
            xaxis=dict(title="인구 수", tickformat=",", tickvals=[-200000, -100000, 0, 100000, 200000],
                       ticktext=["200K", "100K", "0", "100K", "200K"]),
            yaxis=dict(title="연령"),
            barmode='overlay',
            bargap=0.1,
            template='plotly_white'
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❗ 오류 발생: {e}")

else:
    st.info("좌측에서 남녀구분 인구 CSV 파일을 업로드하세요.")
