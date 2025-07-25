import streamlit as st
from streamlit_folium import st_folium
import folium
from geopy.geocoders import Nominatim

# 페이지 설정
st.set_page_config(page_title="카테고리 필터 북마크 지도", layout="wide")
st.title("📍 이모지 & 카테고리 북마크 지도")

# 지오코더
geolocator = Nominatim(user_agent="category_bookmark_app")

# 세션 상태 초기화
if "markers" not in st.session_state:
    st.session_state.markers = []

# 카테고리 목록
CATEGORIES = ["음식점 🍽️", "카페 ☕", "공원 🌳", "여행지 🗺️", "기타 ⭐"]

# 📌 사이드바: 카테고리 필터
st.sidebar.header("📂 카테고리 필터")
selected_category = st.sidebar.selectbox(
    "어떤 카테고리의 북마크를 보고 싶나요?",
    ["전체 보기"] + CATEGORIES
)

# 기본 지도 위치
default_lat = 37.5665
default_lon = 126.9780

# 🌟 북마크 추가 폼
with st.form("bookmark_form"):
    st.subheader("📝 북마크 추가")

    place = st.text_input("장소 이름", "")
    address = st.text_input("주소", "")
    description = st.text_area("설명", "")
    category = st.selectbox("카테고리", CATEGORIES)
    emoji = st.text_input("이모지 (예: 🍕, ☕, 🌳)", "")

    submitted = st.form_submit_button("추가하기")

    if submitted:
        if not place.strip() or not address.strip():
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

# 💡 필터링된 북마크만 가져오기
if selected_category == "전체 보기":
    filtered_markers = st.session_state.markers
else:
    filtered_markers = [m for m in st.session_state.markers if m["category"] == selected_category]

# 지도 중심 위치 설정
if filtered_markers:
    center_lat = filtered_markers[-1]["lat"]
    center_lon = filtered_markers[-1]["lon"]
else:
    center_lat, center_lon = default_lat, default_lon

# 지도 생성
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# 지도에 마커 추가
for marker in filtered_markers:
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

# 📋 북마크 목록
with st.expander("📌 북마크 목록 보기"):
    if filtered_markers:
        for i, marker in enumerate(filtered_markers, 1):
            st.markdown(f"**{i}. {marker['emoji']} {marker['place']}**  \n{marker['category']} - `{marker['lat']}, {marker['lon']}`")
            st.caption(marker["description"])
    else:
        st.info("해당 카테고리에 대한 북마크가 없습니다.")

