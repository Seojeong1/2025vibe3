def checklist_section(title, task_key):
    st.markdown(f"#### {title}")
    if task_key not in st.session_state.data:
        st.session_state.data[task_key] = []

    # 새 항목 추가
    with st.form(f"form_{task_key}", clear_on_submit=True):
        task_text = st.text_input("할 일 또는 일정을 입력 (시간 포함 가능)")
        submitted = st.form_submit_button("추가")
        if submitted and task_text:
            task_time = extract_time(task_text)
            st.session_state.data[task_key].append({
                "text": task_text,
                "time": task_time.strftime("%H:%M"),
                "done": False,
                "edit": False
            })
            save_data(st.session_state.data)

    # 시간순 정렬
    st.session_state.data[task_key].sort(key=lambda x: x["time"])

    # 항목 표시 및 편집 UI
    for i, task in enumerate(st.session_state.data[task_key]):
        cols = st.columns([1, 4, 1, 1])
        task["done"] = cols[0].checkbox("", value=task.get("done", False), key=f"{task_key}_{i}_done")

        if task.get("edit", False):
            new_text = cols[1].text_input("수정", value=task["text"], key=f"{task_key}_{i}_text")
            if cols[2].button("💾", key=f"{task_key}_{i}_save"):
                task["text"] = new_text
                task["time"] = extract_time(new_text).strftime("%H:%M")
                task["edit"] = False
                save_data(st.session_state.data)
            if cols[3].button("❌", key=f"{task_key}_{i}_cancel"):
                task["edit"] = False
        else:
            display_text = f"~~{task['text']}~~" if task["done"] else task["text"]
            cols[1].markdown(f"- {display_text}")
            if cols[2].button("✏️", key=f"{task_key}_{i}_edit"):
                task["edit"] = True
            if cols[3].button("🗑️", key=f"{task_key}_{i}_delete"):
                st.session_state.data[task_key].pop(i)
                save_data(st.session_state.data)
                st.rerun()

    # 수정된 내용 저장
    save_data(st.session_state.data)
