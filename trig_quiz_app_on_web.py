#pip install streamlit
#python -m streamlit run trig_quiz_app_on_web.py

import random
import streamlit as st
import time
from decimal import Decimal, ROUND_HALF_UP

# -----------------------------
# 三角比簡単化ルール
# -----------------------------
def simplify(func, base_angle):
    rules = {
        "sin": {
            90: r"\cos\theta", 180: r"-\sin\theta", 270: r"-\cos\theta",
            -90: r"-\cos\theta", -180: r"-\sin\theta", -270: r"\cos\theta",
            0: r"\sin\theta", -0: r"\sin\theta"
        },
        "cos": {
            90: r"-\sin\theta", 180: r"-\cos\theta", 270: r"\sin\theta",
            -90: r"\sin\theta", -180: r"-\cos\theta", -270: r"-\sin\theta",
            0: r"\cos\theta", -0: r"\cos\theta"
        },
        "tan": {
            90: r"\displaystyle\frac{1}{\tan\theta}", 180: r"\tan\theta", 270: r"\displaystyle-\frac{1}{\tan\theta}",
            -90: r"\displaystyle-\frac{1}{\tan\theta}", -180: r"\tan\theta", -270: r"\displaystyle\frac{1}{\tan\theta}",
            0: r"\tan\theta", -0: r"-\tan\theta"
        }
    }
    return rules[func][base_angle]

# -----------------------------
# 選択肢固定（LaTeX形式）
# -----------------------------
BUTTON_OPTIONS = [
    r"\sin\theta", r"-\sin\theta",
    r"\cos\theta", r"-\cos\theta",
    r"\tan\theta", r"-\tan\theta",
    r"\displaystyle\frac{1}{\tan\theta}", r"\displaystyle-\frac{1}{\tan\theta}"
]

# -----------------------------
# セッションステート初期化
# -----------------------------
for key, val in [("question_number",0), ("score",0), ("start_time",time.time()), 
                 ("answers",[]), ("current_problem",None), ("current_answer",None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# -----------------------------
# 問題生成
# -----------------------------
def generate_question():
    funcs = ["sin", "cos", "tan"]
    base_angles = [90, 180, 270, -90, -180, -270, -0]  # 単純な-θも追加
    func = random.choice(funcs)
    angle = random.choice(base_angles)
    
    if angle == -0:
        problem = rf"\{func}(-\theta) を簡単にせよ"
    else:
        problem = rf"\{func}({angle}^\circ+\theta) を簡単にせよ"
    
    correct = simplify(func, angle)
    return problem, correct

# -----------------------------
# CSS: ボタン縦横揃える・固定
# -----------------------------
st.markdown("""
<style>
div.stButton > button {
    width: 160px !important;
    height: 70px !important;
    font-size: 22px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# アプリタイトル
# -----------------------------
st.title("三角比クイズ (θの簡単化)")

# -----------------------------
# 10問終了チェック
# -----------------------------
if st.session_state.question_number >= 10:
    end_time = time.time()
    elapsed = Decimal(str(end_time - st.session_state.start_time)).quantize(Decimal('0.01'), ROUND_HALF_UP)
    total = st.session_state.score * 10
    st.subheader("結果")
    st.write(f"得点: {total}/100 点")
    st.write(f"経過時間: {elapsed} 秒")

    # LaTeX 表で表示

    latex_table = r"\def\arraystretch{2.5}\begin{array}{|c|c|c|c|} \hline 問題 & あなたの解答 & 正解 & 正誤 \\ \hline "
    for a in st.session_state.answers:
        mark = "○" if a["user"] == a["correct"] else "×"
        latex_table += f"{a['problem']} & {a['user']} & {a['correct']} & {mark} \\\\ \hline "
    latex_table += r"\end{array}"
    st.latex(latex_table)

    if st.button("もう一度やる"):
        st.session_state.update({
            "question_number":0,
            "score":0,
            "start_time":time.time(),
            "answers":[],
            "current_problem":None,
            "current_answer":None
        })

# -----------------------------
# 出題中
# -----------------------------
else:
    # 新しい問題を生成
    if st.session_state.current_problem is None:
        problem, correct = generate_question()
        st.session_state.current_problem = problem
        st.session_state.current_answer = correct

    # 問題文表示（LaTeX）
    st.subheader(f"問題 {st.session_state.question_number+1}: ")
    st.markdown(rf"$$ {st.session_state.current_problem} $$")

    # 選択肢ボタン 2行×4列
    clicked_option = None
    for row in range(2):
        cols = st.columns(4)
        for col_idx in range(4):
            idx = row*4 + col_idx
            option = BUTTON_OPTIONS[idx]
            with cols[col_idx]:
                if st.button(f"${option}$", key=f"{st.session_state.question_number}_{idx}"):
                    clicked_option = option

    # ボタン押した場合、即次の問題へ
    if clicked_option:
        st.session_state.answers.append({
            "problem": st.session_state.current_problem,
            "user": clicked_option,
            "correct": st.session_state.current_answer
        })
        if clicked_option == st.session_state.current_answer:
            st.session_state.score += 1

        st.session_state.question_number += 1
        st.session_state.current_problem = None
        st.session_state.current_answer = None
