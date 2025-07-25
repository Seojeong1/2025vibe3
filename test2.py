import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import LatLngPopup
from geopy.geocoders import Nominatim

# 페이지 설정
st.set_page_config(page_title="장소 검색 + 지도 클릭 북마크", layout="wide")
st.title("📍 장소명 검색 & 지도 클릭으로 북마크 추가")

# 카테고리 정의
CATEGORIES = ["음식점 🍽️", "카페 ☕", "공원 🌳", "여행지 🗺️", "기타 ⭐"]

# 지오코더
geolocator = Nominatim(user_agent="bookmark_map", timeout=10)

# 세션 상태 초기화
if "markers" not in st.session_state:
    st.session_state.markers = []
if "selected_location" not in st.session_state:
    st.session_state.selected_location = None

# 카테고리 필터
st.sidebar.header("📂 카테고리 필터")
selected_category = st.sidebar.selectbox("카테고리 보기", ["전체 보기"] + CATEGORIES)

# 장소 이름 검색
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 장소명으로 위치 찾기")
address_input = st.sidebar.text_input("장소명 또는 주소 입력 (예: 봉선동 포스코아파트, 고사리)")
if st.sidebar.button("📌 위치 찾기"):
    if address_input.strip():
        try:
            location = geolocator.geocode(address_input)
            if location:
                st.session_state.selected_location = {
                    "lat": location.latitude,
                    "lng": location.longitude
                }
                st.success(f"✅ '{address_input}'의 위치를 지도에 표시했습니다!")
            else:
                st.error("❌ 위치를 찾을 수 없습니다. 다른 표현으로 입력해 보세요.")
        except Exception as e:
            st.error(f"❌ 위치 검색 중 오류 발생: {e}")

# 지도 중심 위치
map_center = st.session_state.selected_location or {"lat": 37.5665, "lng": 126.9780}
m = folium.Map(location=[map_center["lat"], map_center["lng"]], zoom_start=13)
m.add_child(LatLngPopup())

# 필터링된 마커 추가
filtered = (
    st.session_state.markers
    if selected_category == "전체 보기"
    else [m for m in st.session_state.markers if m["category"] == selected_category]
)

for marker in filtered:
    folium.Marker(
        location=[marker["lat"], marker["lon"]],
        popup=f"<b>{marker['emoji']} {marker['place']}</b><br>{marker['description']}<br><i>{marker['category']}</i>",
        tooltip=marker["place"],
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 표시 및 클릭 감지
map_data = st_folium(m, width=900, height=600)

if map_data and map_data.get("last_clicked"):
    st.session_state.selected_location = map_data["last_clicked"]

# 북마크 추가 폼
if st.session_state.selected_location:
    st.markdown("### 📌 선택된 위치")
    st.info(f"위도: {st.session_state.selected_location['lat']}, 경도: {st.session_state.selected_location['lng']}")

    with st.form("add_marker_form"):
        place = st.text_input("장소 이름", "")
        description = st.text_area("설명", "")
        category = st.selectbox("카테고리", CATEGORIES)
        emoji = st.text_input("이모지 (예: 🍕, 🏖️, 🏥)", "")
        submit = st.form_submit_button("북마크 추가하기")

        if submit:
            st.session_state.markers.append({
                "place": place,
                "description": description,
                "category": category,
                "emoji": emoji,
                "lat": st.session_state.selected_location["lat"],
                "lon": st.session_state.selected_location["lng"]
            })
            st.success("✅ 북마크가 추가되었습니다!")
            st.session_state.selected_location = None

# 북마크 목록
with st.expander("📌 북마크 목록 보기"):
    if filtered:
        for i, marker in enumerate(filtered, 1):
            st.markdown(f"**{i}. {marker['emoji']} {marker['place']}**  \n{marker['category']} - `{marker['lat']}, {marker['lon']}`")
            st.caption(marker["description"])
    else:
        st.info("해당 카테고리에 대한 북마크가 없습니다.")
