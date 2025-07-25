import streamlit as st
import random

# === 페이지 설정 ===
st.set_page_config(
    page_title="가위바위보 게임",
    page_icon="✊",
    layout="centered"
)

# === 사용자 정의 CSS 테마 ===
st.markdown(
    """
    <style>
    body {
        background-color: #FFF8DC;
    }
    .title {
        text-align: center;
        color: #2E8B57;
        font-size: 40px;
        font-weight: bold;
        margin-top: 20px;
    }
    .scoreboard {
        background-color: #FAF0E6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 20px;
        margin-top: 20px;
    }
    .result {
        font-size: 24px;
        font-weight: bold;
        color: #8B0000;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# === 세션 상태 초기화 ===
if "user_score" not in st.session_state:
    st.session_state.user_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0

# === 타이틀 출력 ===
st.markdown('<div class="title">✊✋✌️ 가위바위보 게임</div>', unsafe_allow_html=True)
st.write("당신은 무엇을 선택하시겠습니까?")

# === 선택 및 대결 버튼 ===
choices = ["가위", "바위", "보"]
user_choice = st.radio("🧑 당신의 선택:", choices, horizontal=True)

if st.button("🎮 대결!"):
    computer_choice = random.choice(choices)

    st.write(f"### 💻 컴퓨터의 선택: {computer_choice}")

    # 게임 로직
    if user_choice == computer_choice:
        result = "무승부입니다! 🤝"
    elif (
        (user_choice == "가위" and computer_choice == "보") or
        (user_choice == "바위" and computer_choice == "가위") or
        (user_choice == "보" and computer_choice == "바위")
    ):
        result = "당신이 이겼습니다! 🎉"
        st.session_state.user_score += 1
    else:
        result = "당신이 졌습니다! 😢"
        st.session_state.computer_score += 1

    st.markdown(f'<div class="result">🏆 결과: {result}</div>', unsafe_allow_html=True)

# === 점수판 표시 ===
st.markdown(
    f"""
    <div class="scoreboard">
        🧑 당신의 점수: <strong>{st.session_state.user_score}</strong> |
        💻 컴퓨터의 점수: <strong>{st.session_state.computer_score}</strong>
    </div>
    """,
    unsafe_allow_html=True
)

# === 점수 초기화 버튼 ===
if st.button("🔄 점수 초기화"):
    st.session_state.user_score = 0
    st.session_state.computer_score = 0
    st.success("점수가 초기화되었습니다!")

