import streamlit as st
import datetime

# --- 사이드바에서 연도, 월, 주, 일 선택 ---
st.sidebar.title("📅 스터디 다이어리")
today = datetime.date.today()

# 연도 선택
year = st.sidebar.selectbox("연도 선택", list(range(today.year - 5, today.year + 6)), index=5)

# 월 선택
month = st.sidebar.selectbox("월 선택", list(range(1, 13)), index=today.month - 1)

# 첫째 날과 마지막 날
first_day = datetime.date(year, month, 1)
next_month = datetime.date(year + (month // 12), (month % 12) + 1, 1)
last_day = next_month - datetime.timedelta(days=1)

# 주 리스트 생성 (월요일 기준)
week_starts = [first_day + datetime.timedelta(days=i) for i in range((last_day - first_day).days + 1) if (first_day + datetime.timedelta(days=i)).weekday() == 0]
weeks = [f"{i+1}주차 ({start.strftime('%m/%d')})" for i, start in enumerate(week_starts)]
week_idx = st.sidebar.selectbox("주 선택", list(range(1, len(weeks)+1)), format_func=lambda x: weeks[x-1])

# 날짜 선택
selected_date = st.sidebar.date_input("날짜 선택", today, min_value=first_day, max_value=last_day)

# 페이지 구분
page = st.sidebar.radio("페이지 유형", ["주간 보기", "일간 보기"])

st.title("📝 스터디 다이어리")

# --- 체크리스트 기능 ---
def checklist_section(title, task_key):
    st.markdown(f"### {title}")

    if "data" not in st.session_state:
        st.session_state["data"] = {}
    if task_key not in st.session_state["data"]:
        st.session_state["data"][task_key] = []

    # 입력 폼
    with st.form(f"form_{task_key}", clear_on_submit=True):
        col1, col2 = st.columns([1, 4])
        with col1:
            time = st.time_input("시간", value=datetime.time(0, 0), label_visibility="collapsed")
        with col2:
            task_text = st.text_input("내용 입력", label_visibility="collapsed")
        submitted = st.form_submit_button("추가")
        if submitted and task_text:
            st.session_state["data"][task_key].append({"text": task_text, "time": time, "done": False})

    # 시간순 정렬
    st.session_state["data"][task_key].sort(key=lambda x: x["time"])

    # 표시
    for i, task in enumerate(st.session_state["data"][task_key]):
        cols = st.columns([1, 5])
        task["done"] = cols[0].checkbox(task["time"].strftime("%H:%M"), value=task["done"], key=f"{task_key}_{i}")
        cols[1].markdown(f"- {'~~' + task['text'] + '~~' if task['done'] else task['text']}")

# --- 페이지 렌더링 ---
if page == "주간 보기":
    st.header(f"📅 {year}년 {month}월 {week_idx}주차")
    st.markdown("---")
    checklist_section("📌 일정", f"{year}_{month}_week{week_idx}_plan")
    st.markdown("---")
    checklist_section("✅ 할 일", f"{year}_{month}_week{week_idx}_todo")

elif page == "일간 보기":
    st.header(f"🗓 {selected_date.strftime('%Y-%m-%d')}")
    st.markdown("---")
    checklist_section("📌 일정", f"{selected_date}_plan")
    st.markdown("---")
    checklist_section("✅ 할 일", f"{selected_date}_todo")
