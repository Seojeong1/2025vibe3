import streamlit as st
import datetime
import re

# 시간 텍스트에서 시간 객체 추출 함수
def extract_time(text):
    patterns = [
        r"(\d{1,2})[:시](\d{1,2})",  # 10:30, 10시30분
        r"(\d{1,2})[:시]",           # 10: or 10시
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2)) if len(match.groups()) > 1 else 0
            try:
                return datetime.time(hour, minute)
            except:
                pass
    return datetime.time(0, 0)  # 기본값

# 체크리스트 UI 함수
def checklist_section(title, task_key):
    st.markdown(f"### {title}")

    if "data" not in st.session_state:
        st.session_state["data"] = {}
    if task_key not in st.session_state["data"]:
        st.session_state["data"][task_key] = []

    # 입력 폼
    with st.form(f"form_{task_key}", clear_on_submit=True):
        task_text = st.text_input("시간과 함께 작성: 예) 10:30 미팅", label_visibility="visible")
        submitted = st.form_submit_button("추가")
        if submitted and task_text:
            task_time = extract_time(task_text)
            st.session_state["data"][task_key].append({
                "text": task_text,
                "time": task_time,
                "done": False
            })

    # 시간순 정렬
    st.session_state["data"][task_key].sort(key=lambda x: x["time"])

    # 체크리스트 출력
    for i, task in enumerate(st.session_state["data"][task_key]):
        cols = st.columns([1, 5])
        task["done"] = cols[0].checkbox(task["time"].strftime("%H:%M"), value=task["done"], key=f"{task_key}_{i}")
        cols[1].markdown(f"- {'~~' + task['text'] + '~~' if task['done'] else task['text']}")

# --- 날짜 관련 기본 설정 ---
st.sidebar.title("📅 스터디 다이어리")
today = datetime.date.today()

year = st.sidebar.selectbox("연도 선택", list(range(today.year - 5, today.year + 6)), index=5)
month = st.sidebar.selectbox("월 선택", list(range(1, 13)), index=today.month - 1)

first_day = datetime.date(year, month, 1)
next_month = datetime.date(year + (month // 12), (month % 12) + 1, 1)
last_day = next_month - datetime.timedelta(days=1)

week_starts = [first_day + datetime.timedelta(days=i) for i in range((last_day - first_day).days + 1) if (first_day + datetime.timedelta(days=i)).weekday() == 0]
weeks = [f"{i+1}주차 ({start.strftime('%m/%d')})" for i, start in enumerate(week_starts)]
week_idx = st.sidebar.selectbox("주 선택", list(range(1, len(weeks)+1)), format_func=lambda x: weeks[x-1])

selected_date = st.sidebar.date_input("날짜 선택", today, min_value=first_day, max_value=last_day)
page = st.sidebar.radio("페이지 유형", ["주간 보기", "일간 보기"])

st.title("📝 스터디 다이어리")

# --- 렌더링 부분 ---
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
