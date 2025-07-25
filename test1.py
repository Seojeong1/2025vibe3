import streamlit as st
import datetime
import calendar
import re

# 시간 텍스트 추출
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

# 체크리스트 출력
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

    # 시간순 정렬
    st.session_state["data"][task_key].sort(key=lambda x: x["time"])

    for i, task in enumerate(st.session_state["data"][task_key]):
        cols = st.columns([1, 5])
        task["done"] = cols[0].checkbox(
            task["time"].strftime("%H:%M"),
            value=task["done"],
            key=f"{task_key}_{i}"
        )
        cols[1].markdown(f"- {'~~' + task['text'] + '~~' if task['done'] else task['text']}")

# 📅 월 선택
st.title("📅 스터디 다이어리 - 월간 캘린더에서 직접 입력")

today = datetime.date.today()
year = st.sidebar.selectbox("연도", list(range(today.year - 3, today.year + 4)), index=3)
month = st.sidebar.selectbox("월", list(range(1, 13)), index=today.month - 1)

selected_date = st.session_state.get("selected_date", None)
selected_week = st.session_state.get("selected_week", None)

month_calendar = calendar.Calendar(firstweekday=0).monthdatescalendar(year, month)
days_of_week = ['월', '화', '수', '목', '금', '토', '일', 'Weekly']

# 🗓 요일 헤더
cols = st.columns(8)
for i, day in enumerate(days_of_week):
    cols[i].markdown(f"**{day}**")

# 🧾 달력 그리기
for week in month_calendar:
    cols = st.columns(8)
    week_key = f"{week[0]}_week"

    for i in range(7):
        date = week[i]
        style = "color:lightgray;" if date.month != month else ""
        plan_key = f"{date}_plan"
        todo_key = f"{date}_todo"
        preview_lines = []

        # 📌 일정 표시
        if "data" in st.session_state:
            if plan_key in st.session_state["data"]:
                preview_lines += [f"📌 {item['text']}" for item in st.session_state["data"][plan_key]]
            if todo_key in st.session_state["data"]:
                preview_lines += [f"✅ {item['text']}" for item in st.session_state["data"][todo_key]]

        if cols[i].button(f"{date.day}", key=f"date_{date}"):
            st.session_state["selected_date"] = date
            st.session_state["selected_week"] = None
            selected_date = date
            selected_week = None

        preview_text = "<br>".join(preview_lines)
        cols[i].markdown(f"<div style='font-size:12px; {style}'>{preview_text}</div>", unsafe_allow_html=True)

    # ➕ 주간 버튼 (텍스트 없는 클릭 영역)
    week_preview = ""
    if "data" in st.session_state and week_key in st.session_state["data"]:
        week_preview = "<br>".join([f"• {item['text']}" for item in st.session_state["data"][week_key]])

    if cols[7].button(" ", key=f"weekbtn_{week_key}"):
        st.session_state["selected_week"] = week_key
        st.session_state["selected_date"] = None
        selected_week = week_key
        selected_date = None

    cols[7].markdown(f"<div style='font-size:12px'>{week_preview}</div>", unsafe_allow_html=True)

# 📝 선택된 항목에 따른 입력 폼 표시
st.markdown("---")
if selected_date:
    st.subheader(f"📆 {selected_date.strftime('%Y년 %m월 %d일')} 일정")
    checklist_section("📌 일정", f"{selected_date}_plan")
    checklist_section("✅ 할 일", f"{selected_date}_todo")
elif selected_week:
    st.subheader(f"📅 {selected_week.split('_')[0]} 주간 할 일")
    checklist_section("📝 주간 할 일", f"{selected_week}")
else:
    st.info("왼쪽 달력에서 날짜 또는 주를 클릭해 주세요.")
