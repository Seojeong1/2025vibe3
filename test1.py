import streamlit as st
import datetime
import calendar
import re

# 시간 추출 함수
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

# 체크리스트 표시 함수
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

# 기본 설정
st.title("📅 스터디 다이어리 - 월간 캘린더")
today = datetime.date.today()
year = st.sidebar.selectbox("연도", list(range(today.year - 3, today.year + 4)), index=3)
month = st.sidebar.selectbox("월", list(range(1, 13)), index=today.month - 1)
selected_date = st.session_state.get("selected_date", today)
selected_week = st.session_state.get("selected_week", None)

month_calendar = calendar.Calendar(firstweekday=0).monthdatescalendar(year, month)
days_of_week = ['월', '화', '수', '목', '금', '토', '일', 'Weekly']

# 요일 헤더
cols = st.columns(8)
for i, day in enumerate(days_of_week):
    cols[i].markdown(f"**{day}**")

# 달력 출력
for week in month_calendar:
    cols = st.columns(8)
    week_key = f"{week[0]}_week"
    weekly_todo_preview = ""
    if "data" in st.session_state and week_key in st.session_state["data"]:
        items = st.session_state["data"][week_key][:3]
        weekly_todo_preview = "<br>".join([f"• {item['text'][:15]}" for item in items])

    for i in range(7):
        date = week[i]
        style = "color:lightgray;" if date.month != month else ""
        plan_key = f"{date}_plan"
        todo_key = f"{date}_todo"
        preview_lines = []

        # 일정 미리보기
        if "data" in st.session_state and plan_key in st.session_state["data"]:
            plan_items = st.session_state["data"][plan_key][:1]
            preview_lines += [f"📌 {item['text'][:10]}" for item in plan_items]

        # 할 일 미리보기
        if "data" in st.session_state and todo_key in st.session_state["data"]:
            todo_items = st.session_state["data"][todo_key][:1]
            preview_lines += [f"✅ {item['text'][:10]}" for item in todo_items]

        # 날짜 버튼
        if cols[i].button(f"{date.day}", key=str(date)):
            st.session_state["selected_date"] = date
            selected_date = date
            selected_week = None

        # 미리보기 출력
        preview_text = "<br>".join(preview_lines)
        cols[i].markdown(f"<div style='font-size:12px; {style}'>{preview_text}</div>", unsafe_allow_html=True)

    # Weekly 칸 (글자 없이 미리보기만 출력, 버튼 없음)
    cols[7].markdown("<br>" * 1, unsafe_allow_html=True)
    cols[7].markdown(f"<div style='font-size:12px'>{weekly_todo_preview}</div>", unsafe_allow_html=True)

# 선택된 날짜 or 주간 표시
st.markdown("---")
if selected_date:
    st.header(f"🗓️ {selected_date.strftime('%Y년 %m월 %d일')} 일정")
    checklist_section("📌 일정", f"{selected_date}_plan")
    checklist_section("✅ 할 일", f"{selected_date}_todo")
elif selected_week:
    st.header(f"🗓️ {selected_week.split('_')[0]} 주간 할 일")
    checklist_section("📌 주간 할 일", f"{selected_week}")
