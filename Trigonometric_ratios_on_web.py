import streamlit as st
import random

st.title("三角比クイズ（sin・cos・tan 有名角編）")

# 有名角（度数法）
famous_angles = [-360, -330, -315, -300, -270, -240, -225, -210, -180, -150, -135, -120, -90, -60, -45, -30,
                 0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360, 390, 405, 420, 450]

# 出題対象の三角関数
functions = ["sin", "cos", "tan"]

# ✅ 選択肢（LaTeX表記できれいに）
latex_options = {
    "0": r"$\displaystyle 0$",
    "1/2": r"$\displaystyle \frac{1}{2}$",
    "√2/2": r"$\displaystyle \frac{\sqrt{2}}{2}$",
    "√3/2": r"$\displaystyle \frac{\sqrt{3}}{2}$",
    "1": r"$\displaystyle 1$",
    "-1/2": r"$\displaystyle -\frac{1}{2}$",
    "-√2/2": r"$\displaystyle -\frac{\sqrt{2}}{2}$",
    "-√3/2": r"$\displaystyle -\frac{\sqrt{3}}{2}$",
    "-1": r"$\displaystyle -1$",
    "√3": r"$\displaystyle \sqrt{3}$",
    "-√3": r"$\displaystyle -\sqrt{3}$",
    "1/√3": r"$\displaystyle \frac{1}{\sqrt{3}}$",
    "-1/√3": r"$\displaystyle -\frac{1}{\sqrt{3}}$",
    "なし": r"$\text{なし}$"
}

options = list(latex_options.keys())

# 有名角に対する正解辞書（分数表記）
answers = {
    "sin": {
        -360: "0", -330: "1/2", -315: "√2/2", -300: "√3/2", -270: "1",
        -240: "√3/2", -225: "√2/2", -210: "1/2", -180: "0", -150: "-1/2",
        -135: "-√2/2", -120: "-√3/2", -90: "-1", -60: "-√3/2", -45: "-√2/2",
        -30: "-1/2", 0: "0", 30: "1/2", 45: "√2/2", 60: "√3/2", 90: "1",
        120: "√3/2", 135: "√2/2", 150: "1/2", 180: "0", 210: "-1/2",
        225: "-√2/2", 240: "-√3/2", 270: "-1", 300: "-√3/2", 315: "-√2/2",
        330: "-1/2", 360: "0", 390: "1/2", 405: "√2/2", 420: "√3/2", 450: "1"
    },
    "cos": {
        -360: "1", -330: "√3/2", -315: "√2/2", -300: "1/2", -270: "0",
        -240: "-1/2", -225: "-√2/2", -210: "-√3/2", -180: "-1", -150: "-√3/2",
        -135: "-√2/2", -120: "-1/2", -90: "0", -60: "1/2", -45: "√2/2",
        -30: "√3/2", 0: "1", 30: "√3/2", 45: "√2/2", 60: "1/2", 90: "0",
        120: "-1/2", 135: "-√2/2", 150: "-√3/2", 180: "-1", 210: "-√3/2",
        225: "-√2/2", 240: "-1/2", 270: "0", 300: "1/2", 315: "√2/2",
        330: "√3/2", 360: "1", 390: "√3/2", 405: "√2/2", 420: "1/2", 450: "0"
    },
    "tan": {
        -360: "0", -330: "1/√3", -315: "1", -300: "√3", -270: "なし",
        -240: "√3", -225: "1", -210: "1/√3", -180: "0", -150: "-1/√3",
        -135: "-1", -120: "-√3", -90: "なし", -60: "-√3", -45: "-1",
        -30: "-1/√3", 0: "0", 30: "1/√3", 45: "1", 60: "√3", 90: "なし",
        120: "-√3", 135: "-1", 150: "-1/√3", 180: "0", 210: "1/√3",
        225: "1", 240: "√3", 270: "なし", 300: "-√3", 315: "-1",
        330: "-1/√3", 360: "0", 390: "1/√3", 405: "1", 420: "√3", 450: "なし"
    }
}

# session_state 初期化
if 'func' not in st.session_state:
    st.session_state.func = random.choice(functions)
if 'angle' not in st.session_state:
    st.session_state.angle = random.choice(famous_angles)
if 'selected' not in st.session_state:
    st.session_state.selected = None
if 'result' not in st.session_state:
    st.session_state.result = ""

# 新しい問題を作る関数
def new_question():
    st.session_state.func = random.choice(functions)
    st.session_state.angle = random.choice(famous_angles)
    st.session_state.selected = None
    st.session_state.result = ""

# 問題文
st.subheader(f"${st.session_state.func}({st.session_state.angle}^\\circ)$ の値は？")

# ✅ ボタンの幅をそろえるため、選択肢をカラム配置で整列
cols = st.columns(4)
selected_option = None
for i, key in enumerate(options):
    with cols[i % 4]:
        if st.button(latex_options[key], use_container_width=True, key=key):
            st.session_state.selected = key
            st.session_state.result = ""

# 答えの確認ボタン
if st.button("解答を確認"):
    correct = answers[st.session_state.func][st.session_state.angle]
    if st.session_state.selected == correct:
        st.session_state.result = f"✅ 正解！　${st.session_state.func}({st.session_state.angle}^\\circ) = {latex_options[correct]}$"
    else:
        st.session_state.result = f"❌ 不正解…　正しい答えは {latex_options[correct]} です。"

# 結果表示
st.markdown(st.session_state.result)

# 次の問題ボタン
if st.button("次の問題"):
    new_question()
