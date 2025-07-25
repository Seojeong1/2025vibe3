import streamlit as st
import random

st.set_page_config(page_title="가위바위보 게임", page_icon="✊✋✌️", layout="centered")

st.title("✊✋✌️ 가위바위보 게임")
st.write("당신은 무엇을 선택하시겠습니까?")

choices = ["가위", "바위", "보"]
user_choice = st.radio("당신의 선택:", choices, horizontal=True)

if st.button("대결!"):
    computer_choice = random.choice(choices)

    st.write(f"### 당신의 선택: {user_choice}")
    st.write(f"### 컴퓨터의 선택: {computer_choice}")

    # 게임 로직
    if user_choice == computer_choice:
        result = "무승부입니다! 🤝"
    elif (
        (user_choice == "가위" and computer_choice == "보") or
        (user_choice == "바위" and computer_choice == "가위") or
        (user_choice == "보" and computer_choice == "바위")
    ):
        result = "당신이 이겼습니다! 🎉"
    else:
        result = "당신이 졌습니다! 😢"

    st.markdown(f"## 🏆 결과: {result}")

