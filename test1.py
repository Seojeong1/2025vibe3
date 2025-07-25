import streamlit as st
import datetime
import calendar
import re
import json
import os

# ===== 데이터 저장/불러오기 =====
DATA_FILE = "calendar_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ===== 시간 텍스트에서 추출 =====
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

# ===== 체크리스트 표시 =====
def checklist_section(title, task_key):
    st.markdown(f"#### {title}")
    if task_key not in st.session_state.data:
        st.session_state.data[task_key] = []

    with st.form(f"form_{task_key}", clear_on_submit=True):
        task_text = st.text_input("시간과 함께 작성 (예: 10:30 수학 복습)")
        submitted = st.form_submit_button("추가")
        if submitted and task_text:
            task_time = extract_time(task_text)
            st.session_state.data[task_key].append({
                "text": task_text,
                "time": task_time.strftime("%H:%M"),
                "done": False
            })
            save_data(st.session_state.data)

    # 시간순 정렬
    st.session_state.data[task_key].sort(key=lambda x: x["time"])

    for i, task in enumerate(st.session_state.data[task_key]):
        cols = st.columns([1, 5])
        done = cols[0].checkbox(task["time"], value=task["done"], key=f"{task_key}_{i}")
        task["done"] = done
        cols[1].markdown(f"- {'~~' + task['text'] + '~~' if done else task['text']}")
    save_data(st.session_state.data)

# ===== 앱 시작 =====
if "data" not in st.session_state:
    st.session_state.data = load_data()
if "selected_date" not in st.session_state:
    st.session_state.selected_date = None
if "selected_week" not in st.session_state:
    st.session_state.selected_week = None

# ===== UI 구성 =====
st.title("📅 스터디 다이어리 - 월간 캘린더 저장형")

today = datetime.date.today()
year = st.sidebar.selectbox("연도", list(range(today.year - 3, today.year + 4)), index=3)
month = st.sidebar.selectbox("월", list(range(1, 13)), index=today.month - 1)

month_calendar = calendar.Calendar(firstweekday=0).monthdatescalendar(year, month)
days_of_week = ['월', '화', '수', '목', '금', '토', '일', 'Weekly']

# ===== 달력 헤더 =====
cols = st.columns(8)
for i, day in enumerate(days_of_week):
    cols[i].markdown(f"**{day}**")

# ===== 달력 그리기 =====
for week in month_calendar:
    cols = st.columns(8)
    week_key = f"{week[0]}_week"

    for i in range(7):
        date = week[i]
        style = "color:lightgray;" if date.month != month else ""
        plan_key = f"{date}_plan"
        todo_key = f"{date}_todo"
        preview_lines = []

        if plan_key in st.session_state.data:
            preview_lines += [f"📌 {item['text']}" for item in st.session_state.data[plan_key]]
        if todo_key in st.session_state.data:
            preview_lines += [f"✅ {item['text']}" for item in st.session_state.data[todo_key]]

        if cols[i].button(f"{date.day}", key=f"date_{date}"):
            st.session_state.selected_date = date
            st.session_state.selected_week = None

        preview_text = "<br>".join(preview_lines)
        cols[i].markdown(f"<div style='font-size:12px; {style}'>{preview_text}</div>", unsafe_allow_html=True)

    # ===== Weekly 칸 =====
    if cols[7].button(" ", key=f"weekbtn_{week_key}"):
        st.session_state.selected_week = week_key
        st.session_state.selected_date = None

    # Weekly 미리보기 (⬇️칸 하단에 표시)
    weekly_preview = ""
    if week_key in st.session_state.data:
        weekly_preview = "<br>".join([f"• {item['text']}" for item in st.session_state.data[week_key]])
    cols[7].markdown(f"<div style='font-size:12px; padding-top:5px'>{weekly_preview}</div>", unsafe_allow_html=True)

# ===== 선택된 일정 표시 =====
st.markdown("---")
if st.session_state.selected_date:
    st.subheader(f"📆 {st.session_state.selected_date.strftime('%Y년 %m월 %d일')} 일정")
    checklist_section("📌 일정", f"{st.session_state.selected_date}_plan")
    checklist_section("✅ 할 일", f"{st.session_state.selected_date}_todo")
elif st.session_state.selected_week:
    st.subheader(f"🗓️ {st.session_state.selected_week.split('_')[0]} 주간 할 일")
    checklist_section("📝 주간 할 일", st.session_state.selected_week)
else:
    st.info("달력에서 날짜 또는 주간(Weekly)을 선택하세요.")
