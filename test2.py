import streamlit as st
from streamlit_folium import st_folium
import folium

# 페이지 설정
st.set_page_config(page_title="나만의 북마크 지도", layout="wide")

st.title("📍 나만의 북마크 지도 만들기")

# 세션 상태에 마커 저장
if "markers" not in st.session_state:
    st.session_state.markers = []

# 기본 지도 중심 좌표 (서울)
default_lat = 37.5665
default_lon = 126.9780

# 사이드바 또는 입력 폼
with st.form("bookmark_form"):
    st.subheader("📝 북마크 추가")
    place = st.text_input("장소 이름", "")
    description = st.text_area("설명", "")
    lat = st.number_input("위도", value=default_lat, format="%.6f")
    lon = st.number_input("경도", value=default_lon, format="%.6f")
    submitted = st.form_submit_button("추가하기")

    if submitted:
        if place.strip() == "":
            st.warning("❗ 장소 이름은 필수입니다.")
        else:
            st.session_state.markers.append({
                "place": place,
                "description": description,
                "lat": lat,
                "lon": lon
            })
            st.success(f"✅ '{place}' 북마크가 추가되었습니다!")

# 지도 생성
m = folium.Map(location=[default_lat, default_lon], zoom_start=12)

# 마커 추가
for marker in st.session_state.markers:
    folium.Marker(
        location=[marker["lat"], marker["lon"]],
        popup=f"<b>{marker['place']}</b><br>{marker['description']}",
        tooltip=marker["place"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 출력
st_data = st_folium(m, width=900, height=600)

# 북마크 목록
with st.expander("📌 북마크 목록 보기"):
    if st.session_state.markers:
        for i, marker in enumerate(st.session_state.markers, 1):
            st.markdown(f"**{i}. {marker['place']}**  \n📍 위도: `{marker['lat']}`, 경도: `{marker['lon']}`")
            st.caption(marker['description'])
    else:
        st.info("아직 북마크가 없습니다. 위에서 추가해보세요!")
