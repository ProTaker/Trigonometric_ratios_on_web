import streamlit as st
import random
import time
from decimal import Decimal, ROUND_HALF_UP

st.title("三角比クイズ（sin・cos・tan 有名角編）")

# -----------------------------
# ✅ CSS（ボタンサイズ調整）
# -----------------------------
st.markdown("""
<style>
/* 選択肢ボタンのサイズとフォントを統一 */
div.stButton > button {
    width: 160px !important;
    height: 70px !important;
    font-size: 22px;
}
</style>
""", unsafe_allow_html=True)

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

# -----------------------------------------------
# 選択肢の分類（sin/cos 用と tan 用）
# -----------------------------------------------
sin_cos_options = [
    "0", "1/2", "√2/2", "√3/2", "1",
    "-1/2", "-√2/2", "-√3/2", "-1"
]
tan_options = [
    "0", "1", "√3", "1/√3",
    "-1", "-√3", "-1/√3",
    "なし"
]

# 有名角に対する正解辞書
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

# 新しい問題を作る関数
def new_question():
    st.session_state.func = random.choice(functions)
    st.session_state.angle = random.choice(famous_angles)
    st.session_state.selected = None
    st.session_state.result = ""
    st.session_state.show_result = False

# セッションステートの初期化とリセット
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
    
    # 履歴に保存
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
    
    # 問題数制限に達したら結果表示フラグを立てる
    if st.session_state.question_count >= MAX_QUESTIONS:
        st.session_state.show_result = True
    else:
        new_question()
    
    st.rerun()

# 初期化実行
initialize_session_state()

# -----------------------------------------------
# アプリの描画
# -----------------------------------------------

# 問題数が MAX_QUESTIONS に達しているかチェック
if st.session_state.show_result:
    end_time = time.time()
    elapsed = Decimal(str(end_time - st.session_state.start_time)).quantize(Decimal('0.01'), ROUND_HALF_UP)
    
    st.header("✨ クイズ終了！ 結果発表 ✨")
    st.markdown(f"**あなたのスコア: {st.session_state.score} / {MAX_QUESTIONS} 問正解**")
    st.write(f"**経過時間: {elapsed} 秒**")
    st.divider()
    
    st.subheader("全解答の確認")
    
    # ✅ LaTeXのバックスラッシュを修正。LaTeXコマンドは \\、ラインブレイクは \\\\
    # Python文字列: \def は \\def、\begin は \\begin
    latex_table = "\\def\\arraystretch{2.5}\\begin{array}{|c|c|c|c|c|} \\hline 番号 & 問題 & あなたの解答 & 正解 & 正誤 \\hline "
    
    for i, item in enumerate(st.session_state.history, 1):
        # 問題: \sin\left(30^\circ\right) の形式に
        question_text = f"\\{item['func']}\\left({item['angle']}^\\circ\\right)" 
        user_latex = latex_options.get(item['user_answer'], item['user_answer'])
        correct_latex = latex_options.get(item['correct_answer'], item['correct_answer'])
        
        mark = "○" if item['is_correct'] else "×"
        
        # ラインブレイクは \\\\ 、\hline は \hline (Python文字列では \\hline)
        latex_table += f"{i} & ${question_text}$ & {user_latex} & {correct_latex} & {mark} \\\\ \\hline "
    
    latex_table += "\\end{array}"
    
    # st.latexで表を表示
    st.latex(latex_table)

    if st.button("もう一度挑戦する"):
        st.session_state.clear()
        initialize_session_state()
        st.rerun()
    
else:
    # 問題の表示
    st.subheader(f"問題 {st.session_state.question_count + 1} / {MAX_QUESTIONS}")
    
    current_func = st.session_state.func
    st.markdown(rf"$$ \{current_func}\left({st.session_state.angle}^\circ\right)\ の値は？ $$")

    # 選択肢の決定
    if current_func in ["sin", "cos"]:
        display_options = sin_cos_options
    else:
        display_options = tan_options

    # 選択肢ボタンの表示と処理
    cols = st.columns(4) 
    for i, key in enumerate(display_options):
        with cols[i % 4]:
            button_key = f"option_{st.session_state.question_count}_{key}"
            # ボタンが押されたら、選択を確定し、即座に次の問題へ遷移
            if st.button(latex_options[key], use_container_width=True, key=button_key):
                st.session_state.selected = key
                check_answer_and_advance() 
    
    st.markdown("---")