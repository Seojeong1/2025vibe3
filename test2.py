import streamlit as st
from streamlit_folium import st_folium
import folium
from geopy.geocoders import Nominatim

# 페이지 설정
st.set_page_config(page_title="이모지 북마크 지도", layout="wide")
st.title("📍 나만의 이모지 북마크 지도 만들기")

# 지오코더 초기화
geolocator = Nominatim(user_agent="emoji_bookmark_map")

# 세션 상태 초기화
if "markers" not in st.session_state:
    st.session_state.markers = []

# 기본 위치 (서울)
default_lat = 37.5665
default_lon = 126.9780

# 입력 폼
with st.form("bookmark_form"):
    st.subheader("📝 북마크 추가")

    place = st.text_input("장소 이름", "")
    address = st.text_input("주소", "")
    description = st.text_area("설명", "")

    # ✅ 카테고리 및 이모지 입력
    category = st.selectbox("카테고리", ["음식점 🍽️", "카페 ☕", "공원 🌳", "여행지 🗺️", "기타 ⭐"])
    emoji = st.text_input("이모지 (예: 🎡, 🏠, 🍕)", "")

    submitted = st.form_submit_button("추가하기")

    if submitted:
        if place.strip() == "" or address.strip() == "":
            st.warning("❗ 장소 이름과 주소를 모두 입력해 주세요.")
        else:
            try:
                location = geolocator.geocode(address)
                if location:
                    st.session_state.markers.append({
                        "place": place,
                        "address": address,
                        "description": description,
                        "category": category,
                        "emoji": emoji,
                        "lat": location.latitude,
                        "lon": location.longitude
                    })
                    st.success(f"✅ '{place}' 북마크가 추가되었습니다!")
                else:
                    st.error("❌ 주소를 찾을 수 없습니다. 정확한 주소를 입력해 주세요.")
            except Exception as e:
                st.error(f"❌ 오류 발생: {e}")

# 지도 중심 위치
if st.session_state.markers:
    last = st.session_state.markers[-1]
    map_center = [last["lat"], last["lon"]]
else:
    map_center = [default_lat, default_lon]

# 지도 생성
m = folium.Map(location=map_center, zoom_start=12)

# 마커 추가
for marker in st.session_state.markers:
    popup_html = f"""
    <b>{marker['emoji']} {marker['place']}</b><br>
    <i>{marker['category']}</i><br>
    {marker['description']}<br>
    <small>{marker['address']}</small>
    """
    folium.Marker(
        location=[marker["lat"], marker["lon"]],
        popup=popup_html,
        tooltip=f"{marker['emoji']} {marker['place']}",
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 출력
st_data = st_folium(m, width=900, height=600)

# 목록 출력
with st.expander("📌 북마크 목록 보기"):
    if st.session_state.markers:
        for i, marker in enumerate(st.session_state.markers, 1):
            st.markdown(f"**{i}. {marker['emoji']} {marker['place']}**  \n{marker['category']} - `{marker['lat']}, {marker['lon']}`")
            st.caption(marker["description"])
    else:
        st.info("북마크가 아직 없습니다.")
