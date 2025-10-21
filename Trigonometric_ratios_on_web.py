import streamlit as st
import random
import time
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd # 👈 追加: 結果表示にPandasを使用

st.title("三角比クイズ（sin・cos・tan 有名角編）")

# -----------------------------
# CSS（ボタンサイズ調整）
# -----------------------------
st.markdown("""
<style>
/* 選択肢ボタンのサイズとフォントを統一 */
div.stButton > button {
    width: 160px !important;
    height: 70px !important;
    font-size: 22px;
}
/* st.table/st.dataframe のセル内の数式表示を調整 */
.stTable, .stDataFrame {
    font-size: 18px; /* 全体フォントサイズ調整 */
}
</style>
""", unsafe_allow_html=True)

# 有名角、関数、選択肢などの定義（中略）
# ...
famous_angles = [-360, -330, -315, -300, -270, -240, -225, -210, -180, -150, -135, -120, -90, -60, -45, -30,
                 0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360, 390, 405, 420, 450]
functions = ["sin", "cos", "tan"]

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

sin_cos_options = [
    "0", "1/2", "√2/2", "√3/2", "1",
    "-1/2", "-√2/2", "-√3/2", "-1"
]
tan_options = [
    "0", "1", "√3", "1/√3",
    "-1", "-√3", "-1/√3",
    "なし"
]

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
MAX_QUESTIONS = 10 

# 関数定義（中略）
def new_question():
    st.session_state.func = random.choice(functions)
    st.session_state.angle = random.choice(famous_angles)
    st.session_state.selected = None
    st.session_state.result = ""
    st.session_state.show_result = False

def initialize_session_state():
    if 'func' not in st.session_state:
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

if st.session_state.show_result:
    end_time = time.time()
    elapsed = Decimal(str(end_time - st.session_state.start_time)).quantize(Decimal('0.01'), ROUND_HALF_UP)
    
    st.header("✨ クイズ終了！ 結果発表 ✨")
    st.markdown(f"**あなたのスコア: {st.session_state.score} / {MAX_QUESTIONS} 問正解**")
    st.write(f"**経過時間: {elapsed} 秒**")
    st.divider()
    
    st.subheader("全解答の確認")
    
    # ✅ 修正箇所：Pandas DataFrameとst.table()で安定表示
    table_data = []
    for i, item in enumerate(st.session_state.history, 1):
        # 問題表示の調整（マイナス角にのみ括弧をつける）
        if item['angle'] < 0:
            func_disp = rf"$\text{{}}{item['func']}\left({item['angle']}^\circ\right)$"
        else:
            func_disp = rf"$\text{{}}{item['func']} {item['angle']}^\circ$"
            
        user_disp = latex_options.get(item['user_answer'], item['user_answer'])
        correct_disp = latex_options.get(item['correct_answer'], item['correct_answer'])
        mark = "○" if item['is_correct'] else "×"
        
        table_data.append({
            "番号": i,
            "問題": func_disp,
            "あなたの解答": user_disp,
            "正解": correct_disp,
            "正誤": mark
        })

    df = pd.DataFrame(table_data)

    # st.tableで表示（安定性が高い）
    st.table(df.set_index("番号"))
    

    if st.button("もう一度挑戦する"):
        st.session_state.clear()
        initialize_session_state()
        st.rerun()
    
else:
    # 問題の表示
    st.subheader(f"問題 {st.session_state.question_count + 1} / {MAX_QUESTIONS}")
    
    current_func = st.session_state.func
    current_angle = st.session_state.angle
    
    # ✅ 修正箇所: マイナスの角度のときのみ括弧をつける
    if current_angle < 0:
        question_latex = rf"$$ \{current_func}\left({current_angle}^\circ\right)\ の値は？ $$"
    else:
        question_latex = rf"$$ \{current_func} {current_angle}^\circ\ の値は？ $$"
        
    st.markdown(question_latex)

    if current_func in ["sin", "cos"]:
        display_options = sin_cos_options
    else:
        display_options = tan_options

    cols = st.columns(4) 
    for i, key in enumerate(display_options):
        with cols[i % 4]:
            button_key = f"option_{st.session_state.question_count}_{key}"
            if st.button(latex_options[key], use_container_width=True, key=button_key):
                st.session_state.selected = key
                check_answer_and_advance() 
    
    st.markdown("---")