import streamlit as st
import datetime
import calendar
import re

# --- 시간 추출 함수 ---
def extract_time(text):
    patterns = [r"(\d{1,2})[:시](\d{1,2})", r"(\d{1,2})[:시]"]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2)) if len(match.groups()) > 1 else 0
            try:
                return datetime.time(hour, minute)
            except:
                pass
    return datetime.time(0, 0)

# --- 체크리스트 저장/표시 함수 ---
def checklist_section(title, task_key):
    st.markdown(f"#### {title}")

    if "data" not in st.session_state:
        st.session_state["data"] = {}
    if task_key not in st.session_state["data"]:
        st.session_state["data"][task_key] = []

    with st.form(f"form_{task_key}", clear_on_submit=True):
        task_text = st.text_input("시간과 함께 작성 (예: 10:30 수학 복습)")
        submitted = st.form_submit_button("추가")
        if submitted and task_text:
            task_time = extract_time(task_text)
            st.session_state["data"][task_key].append({
                "text": task_text,
                "time": task_time,
                "done": False
            })

    st.session_state["data"][task_key].sort(key=lambda x: x["time"])

    for i, task in enumerate(st.session_state["data"][task_key]):
        cols = st.columns([1, 5])
        task["done"] = cols[0].checkbox(task["time"].strftime("%H:%M"), value=task["done"], key=f"{task_key}_{i}")
        cols[1].markdown(f"- {'~~' + task['text'] + '~~' if task['done'] else task['text']}")

# --- 날짜 선택 ---
st.title("📅 스터디 다이어리 - 월간 보기")

today = datetime.date.today()
year = st.sidebar.selectbox("연도", list(range(today.year - 3, today.year + 4)), index=3)
month = st.sidebar.selectbox("월", list(range(1, 13)), index=today.month - 1)
selected_date = st.session_state.get("selected_date", today)

# 달력 구성
month_calendar = calendar.Calendar().monthdatescalendar(year, month)
days_of_week = ['월', '화', '수', '목', '금', '토', '일']

st.markdown(f"### 📆 {year}년 {month}월")

# 달력 표 형식으로 출력
for week in month_calendar:
    cols = st.columns(7)
    for i, date in enumerate(week):
        # 현재 월이 아니면 흐리게
        style = "color:lightgray;" if date.month != month else ""
        key = f"{date}_plan"
        preview = ""
        if "data" in st.session_state and key in st.session_state["data"]:
            # 일정 미리보기 (최대 1~2개)
            preview_items = st.session_state["data"][key][:2]
            preview = "<br>".join([f"• {item['text'][:10]}" for item in preview_items])

        if cols[i].button(f"{date.day}", key=str(date)):
            st.session_state["selected_date"] = date
            selected_date = date

        # 일정 미리보기 텍스트
        cols[i].markdown(f"<div style='font-size:12px; {style}'>{preview}</div>", unsafe_allow_html=True)

st.markdown("---")
st.header(f"🗓️ {selected_date.strftime('%Y년 %m월 %d일')} 일정")
checklist_section("📌 일정", f"{selected_date}_plan")
checklist_section("✅ 할 일", f"{selected_date}_todo")

