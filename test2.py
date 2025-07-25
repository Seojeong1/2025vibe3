import streamlit as st
from streamlit_folium import st_folium
import folium
from folium import LatLngPopup

# 페이지 설정
st.set_page_config(page_title="지도 선택 북마크", layout="wide")
st.title("📍 지도에서 직접 선택하는 나만의 북마크")

# 카테고리 목록
CATEGORIES = ["음식점 🍽️", "카페 ☕", "공원 🌳", "여행지 🗺️", "기타 ⭐"]

# 세션 상태 초기화
if "markers" not in st.session_state:
    st.session_state.markers = []

# 세션에 위치 임시 저장
if "selected_location" not in st.session_state:
    st.session_state.selected_location = None

# 사이드바 필터
st.sidebar.header("📂 카테고리 필터")
selected_category = st.sidebar.selectbox("카테고리 선택", ["전체 보기"] + CATEGORIES)

# 지도 생성
default_location = [37.5665, 126.9780]
m = folium.Map(location=default_location, zoom_start=12)

# 클릭 시 위도/경도 출력
m.add_child(LatLngPopup())

# 기존 마커들 추가 (필터링 반영)
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

# st_folium을 통해 지도 클릭 이벤트 수신
map_data = st_folium(m, width=900, height=600)

# 클릭된 좌표가 있으면 저장
if map_data and map_data.get("last_clicked"):
    st.session_state.selected_location = map_data["last_clicked"]

# 위치 선택되었을 때 폼 표시
if st.session_state.selected_location:
    st.markdown("### 📌 선택한 위치 정보:")
    st.info(f"위도: {st.session_state.selected_location['lat']}, 경도: {st.session_state.selected_location['lng']}")

    with st.form("add_marker_form"):
        place = st.text_input("장소 이름", "")
        description = st.text_area("설명", "")
        category = st.selectbox("카테고리", CATEGORIES)
        emoji = st.text_input("이모지 (예: ☕, 🍽️, 🏖️)", "")
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
            st.session_state.selected_location = None  # 초기화

# 북마크 목록 출력
with st.expander("📌 북마크 목록 보기"):
    if filtered:
        for i, marker in enumerate(filtered, 1):
            st.markdown(f"**{i}. {marker['emoji']} {marker['place']}**  \n{marker['category']} - `{marker['lat']}, {marker['lon']}`")
            st.caption(marker["description"])
    else:
        st.info("해당 카테고리에 대한 북마크가 없습니다.")
