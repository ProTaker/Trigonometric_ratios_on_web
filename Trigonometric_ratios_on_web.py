import streamlit as st
import math
import random

st.title("三角比クイズ（−360°〜450°の有名角）")

# 有名角リスト（度数法）
famous_angles = [-360, -330, -315, -300, -270, -240, -225, -210, -180, -150, -135, -120, -90, -60, -45, -30, 0,
                 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360, 390, 405, 420, 450]

# session_state 初期化
if 'current_angle' not in st.session_state:
    st.session_state.current_angle = random.choice(famous_angles)
if 'selected_answer' not in st.session_state:
    st.session_state.selected_answer = None
if 'result' not in st.session_state:
    st.session_state.result = ""

# ランダム問題生成関数
def new_question():
    st.session_state.current_angle = random.choice(famous_angles)
    st.session_state.selected_answer = None
    st.session_state.result = ""

# 問題表示
st.write(f"次の角度の **sin** の値はいくつでしょう？")
st.write(f"角度: {st.session_state.current_angle}°")

# 正解計算
rad = math.radians(st.session_state.current_angle)
correct_value = round(math.sin(rad), 4)

# 選択肢生成（正解 + ランダム値）
options = [correct_value]
while len(options) < 4:
    val = round(random.uniform(-1, 1), 4)
    if val not in options:
        options.append(val)
random.shuffle(options)

# 選択肢ラジオボタン
st.session_state.selected_answer = st.radio("答えを選んでください:", options, index=0 if st.session_state.selected_answer is None else options.index(st.session_state.selected_answer))

# 解答確認ボタン
if st.button("解答を確認"):
    if st.session_state.selected_answer == correct_value:
        st.session_state.result = "正解！🎉"
    else:
        st.session_state.result = f"不正解… 正しい答えは {correct_value} です。"

st.write(st.session_state.result)

# 次の問題ボタン
if st.button("次の問題"):
    new_question()
