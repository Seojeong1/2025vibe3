import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="남녀 연령별 인구 비교", layout="wide")
st.title("👫 서울특별시 연령별 인구 현황 (남녀 구분)")

uploaded_file = st.file_uploader("남녀 구분 CSV 업로드", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='cp949')
    except:
        df = pd.read_csv(uploaded_file, encoding='utf-8')

    try:
        # ⛳ 디버깅용 샘플 출력
        st.write("📌 데이터프레임 미리보기")
        st.dataframe(df.head(3))

        # 서울특별시 전체 데이터 찾기 (ex. '서울특별시  (1100000000)')
        df_seoul = df[df["행정구역"].str.contains("서울특별시")].iloc[0]

        # 열 필터링
        male_cols = [col for col in df.columns if "남_" in col and "세" in col]
        female_cols = [col for col in df.columns if "여_" in col and "세" in col]
        age_labels = [col.split("_")[-1] for col in male_cols]

        # 값 전처리 (쉼표 제거 → 숫자)
        male_values = df_seoul[male_cols].replace(",", "", regex=True)
        female_values = df_seoul[female_cols].replace(",", "", regex=True)

        male_values = pd.to_numeric(male_values, errors='coerce').fillna(0).astype(int)
        female_values = pd.to_numeric(female_values, errors='coerce').fillna(0).astype(int)

        # 시각화
        fig = go.Figure()
        fig.add_trace(go.Bar(x=age_labels, y=male_values, name="남성", marker_color='blue'))
        fig.add_trace(go.Bar(x=age_labels, y=female_values, name="여성", marker_color='deeppink'))

        fig.update_layout(
            title="서울특별시 남녀 연령별 인구 비교",
            xaxis_title="연령",
            yaxis_title="인구 수",
            barmode='group',
            xaxis_tickangle=-45,
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

        # 데이터 확인
        with st.expander("📋 원시 데이터 확인"):
            st.dataframe(pd.DataFrame({
                "연령": age_labels,
                "남성": male_values.values,
                "여성": female_values.values
            }))

    except Exception as e:
        st.error(f"❗ 오류 발생: {e}")

else:
    st.info("좌측에서 CSV 파일을 업로드하세요.")
