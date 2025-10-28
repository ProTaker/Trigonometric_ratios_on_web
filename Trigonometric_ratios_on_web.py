import streamlit as st
import random
import time
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd 

st.title("三角比クイズ（有名角編）")

# -----------------------------
# CSS（ボタンサイズ調整と列幅固定、中央揃えの再適用）
# -----------------------------
st.markdown("""
<style>
div.stButton > button {
    width: 160px !important;
    height: 70px !important;
    font-size: 22px;
}
.stTable, .stDataFrame {
    font-size: 18px;
}
.stTable {
    width: fit-content; 
    margin-left: auto;  
    margin-right: auto; 
}
.stTable table th, .stTable table td {
    white-space: nowrap;
    text-align: center !important; 
    vertical-align: middle !important;
}
.stTable table th:nth-child(1), .stTable table td:nth-child(1) { width: 60px; }
.stTable table th:nth-child(2), .stTable table td:nth-child(2) { min-width: 220px; }
.stTable table th:nth-child(3), .stTable table td:nth-child(3) { min-width: 150px; }
.stTable table th:nth-child(4), .stTable table td:nth-child(4) { min-width: 150px; }
.stTable table th:nth-child(5), .stTable table td:nth-child(5) { width: 60px; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 角度範囲の定義
# -----------------------------
ANGLE_RANGES = {
    "0~90": [0, 30, 45, 60, 90],
    "0~180": [0, 30, 45, 60, 90, 120, 135, 150, 180],
    "0~360": [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360],
    "-180~180": [-180, -150, -135, -120, -90, -60, -45, -30, 0, 30, 45, 60, 90, 120, 135, 150, 180],
    "ALL": [-360, -330, -315, -300, -270, -240, -225, -210, -180, -150, -135, -120, -90, -60, -45, -30,
            0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360, 390, 405, 420, 450]
}
functions = ["sin", "cos", "tan"]

# （中略：選択肢やanswers辞書などは元のまま）
# -------------
# 以下、元コードの構造を維持したまま
# -------------

def new_question():
    st.session_state.func = random.choice(functions)
    st.session_state.angle = random.choice(ANGLE_RANGES[st.session_state.angle_range])
    st.session_state.selected = None
    st.session_state.result = ""
    st.session_state.show_result = False

def initialize_session_state():
    if 'range_selected' not in st.session_state:
        st.session_state.range_selected = False
        st.session_state.angle_range = "ALL"
    if 'func' not in st.session_state and st.session_state.range_selected:
        st.session_state.score = 0
        st.session_state.question_count = 0
        st.session_state.history = []
        st.session_state.show_result = False
        st.session_state.start_time = time.time()
        new_question()

def check_answer_and_advance():
    if st.session_state.selected is None:
        st.session_state.result = "選択肢を選んでください。"
        return
    current_func = st.session_state.func
    current_angle = st.session_state.angle
    correct = answers[current_func][current_angle]
    is_correct = (st.session_state.selected == correct)
    st.session_state.history.append({
        "func": current_func,
        "angle": current_angle,
        "user_answer": st.session_state.selected,
        "correct_answer": correct,
        "is_correct": is_correct
    })
    if is_correct:
        st.session_state.score += 1
    st.session_state.question_count += 1
    if st.session_state.question_count >= MAX_QUESTIONS:
        st.session_state.show_result = True
    else:
        new_question()
    st.rerun()

initialize_session_state()

# -----------------------------------------------
# アプリの描画
# -----------------------------------------------
if not st.session_state.range_selected:
    st.header("出題範囲を選択してください")
    range_cols = st.columns(5)
    if range_cols[0].button(r"$0^\circ \sim 90^\circ$", use_container_width=True):
        st.session_state.angle_range = "0~90"
        st.session_state.range_selected = True
        initialize_session_state()
        st.rerun()
    if range_cols[1].button(r"$0^\circ \sim 180^\circ$", use_container_width=True):
        st.session_state.angle_range = "0~180"
        st.session_state.range_selected = True
        initialize_session_state()
        st.rerun()
    if range_cols[2].button(r"$0^\circ \sim 360^\circ$", use_container_width=True):
        st.session_state.angle_range = "0~360"
        st.session_state.range_selected = True
        initialize_session_state()
        st.rerun()
    if range_cols[3].button(r"$-180^\circ \sim 180^\circ$", use_container_width=True):
        st.session_state.angle_range = "-180~180"
        st.session_state.range_selected = True
        initialize_session_state()
        st.rerun()
    if range_cols[4].button(r"全範囲", use_container_width=True):
        st.session_state.angle_range = "ALL"
        st.session_state.range_selected = True
        initialize_session_state()
        st.rerun()

# （以降は元のクイズ出題・結果表示ロジックそのまま）
