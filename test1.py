import streamlit as st
import json
import os

DATA_FILE = "todo_data.json"

# 파일 불러오기
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# 파일 저장
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# 초기 데이터
if "todos" not in st.session_state:
    st.session_state.todos = load_data()
if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = None  # index of item being edited

st.title("📝 나만의 메모장 TODO")

# 새 할 일 추가
with st.form("new_todo", clear_on_submit=True):
    new_text = st.text_input("새 할 일 입력", "")
    submitted = st.form_submit_button("추가")
    if submitted and new_text:
        st.session_state.todos.append({"text": new_text, "done": False})
        save_data(st.session_state.todos)

# 할 일 목록 표시
for idx, item in enumerate(st.session_state.todos):
    cols = st.columns([1, 5, 1, 1, 1])
    item["done"] = cols[0].checkbox("", value=item["done"], key=f"done_{idx}")

    # 수정 모드일 경우
    if st.session_state.edit_mode == idx:
        new_text = cols[1].text_input("수정", value=item["text"], key=f"edit_{idx}")
        if cols[2].button("💾", key=f"save_{idx}"):
            item["text"] = new_text
            st.session_state.edit_mode = None
            save_data(st.session_state.todos)
        if cols[3].button("❌", key=f"cancel_{idx}"):
            st.session_state.edit_mode = None
    else:
        # 일반 표시
        style = "text-decoration: line-through;" if item["done"] else ""
        cols[1].markdown(f"<div style='{style}'>{item['text']}</div>", unsafe_allow_html=True)
        if cols[2].button("✏️", key=f"edit_btn_{idx}"):
            st.session_state.edit_mode = idx
        if cols[3].button("🗑️", key=f"delete_{idx}"):
            st.session_state.todos.pop(idx)
            save_data(st.session_state.todos)
            st.rerun()

    # 위치 이동
    up = cols[4].button("🔼", key=f"up_{idx}") if idx > 0 else None
    down = cols[4].button("🔽", key=f"down_{idx}") if idx < len(st.session_state.todos) - 1 else None

    if up:
        st.session_state.todos[idx - 1], st.session_state.todos[idx] = st.session_state.todos[idx], st.session_state.todos[idx - 1]
        save_data(st.session_state.todos)
        st.rerun()
    elif down:
        st.session_state.todos[idx + 1], st.session_state.todos[idx] = st.session_state.todos[idx], st.session_state.todos[idx + 1]
        save_data(st.session_state.todos)
        st.rerun()
