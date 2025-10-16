import random
import streamlit as st
import time
from decimal import Decimal, ROUND_HALF_UP

# -----------------------------
# 三角比簡単化ルール（ラジアン表記、分数はLaTeXで表示）
# -----------------------------
def simplify(func, expr):
    # expr は内部キー（英数字）で扱い、表示は latex_map を使う
    rules = {
        "sin": {
            "pi/2+θ": r"\cos\theta",
            "pi+θ": r"-\sin\theta",
            "3pi/2+θ": r"-\cos\theta",
            "-pi/2+θ": r"-\cos\theta",
            "-pi+θ": r"-\sin\theta",
            "-3pi/2+θ": r"\cos\theta",
            "-θ": r"-\sin\theta",
            "pi/2-θ": r"\cos\theta",
            "pi-θ": r"\sin\theta",
            "3pi/2-θ": r"-\cos\theta",
            "-pi/2-θ": r"\cos\theta",
            "-pi-θ": r"-\sin\theta",
            "-3pi/2-θ": r"-\cos\theta",
        },
        "cos": {
            "pi/2+θ": r"-\sin\theta",
            "pi+θ": r"-\cos\theta",
            "3pi/2+θ": r"\sin\theta",
            "-pi/2+θ": r"\sin\theta",
            "-pi+θ": r"-\cos\theta",
            "-3pi/2+θ": r"-\sin\theta",
            "-θ": r"\cos\theta",
            "pi/2-θ": r"\sin\theta",
            "pi-θ": r"-\cos\theta",
            "3pi/2-θ": r"-\sin\theta",
            "-pi/2-θ": r"-\sin\theta",
            "-pi-θ": r"-\cos\theta",
            "-3pi/2-θ": r"\sin\theta",
        },
        "tan": {
            "pi/2+θ": r"\displaystyle-\frac{1}{\tan\theta}",
            "pi+θ": r"\tan\theta",
            "3pi/2+θ": r"\displaystyle-\frac{1}{\tan\theta}",
            "-pi/2+θ": r"\displaystyle-\frac{1}{\tan\theta}",
            "-pi+θ": r"\tan\theta",
            "-3pi/2+θ": r"\displaystyle-\frac{1}{\tan\theta}",
            "-θ": r"-\tan\theta",
            "pi/2-θ": r"\displaystyle\frac{1}{\tan\theta}",
            "pi-θ": r"-\tan\theta",
            "3pi/2-θ": r"\displaystyle\frac{1}{\tan\theta}",
            "-pi/2-θ": r"\displaystyle\frac{1}{\tan\theta}",
            "-pi-θ": r"-\tan\theta",
            "-3pi/2-θ": r"\displaystyle\frac{1}{\tan\theta}",
        }
    }
    return rules[func][expr]

# -----------------------------
# 表示用：内部キー -> LaTeX 表現（分数は \frac{\pi}{2} などで綺麗に）
# -----------------------------
latex_map = {
    "pi/2+θ": r"\frac{\pi}{2} + \theta",
    "pi+θ": r"\pi + \theta",
    "3pi/2+θ": r"\frac{3\pi}{2} + \theta",
    "-pi/2+θ": r"-\frac{\pi}{2} + \theta",
    "-pi+θ": r"-\pi + \theta",
    "-3pi/2+θ": r"-\frac{3\pi}{2} + \theta",
    "-θ": r"-\theta",
    "pi/2-θ": r"\frac{\pi}{2} - \theta",
    "pi-θ": r"\pi - \theta",
    "3pi/2-θ": r"\frac{3\pi}{2} - \theta",
    "-pi/2-θ": r"-\frac{\pi}{2} - \theta",
    "-pi-θ": r"-\pi - \theta",
    "-3pi/2-θ": r"-\frac{3\pi}{2} - \theta",
}

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
for key, val in [("question_number",1), ("score",0), ("start_time",time.time()), 
                 ("answers",[]), ("current_problem",None), ("current_answer",None),
                 ("mode_selected",False), ("mode", None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# -----------------------------
# タイトル
# -----------------------------
st.title("三角比クイズ（ラジアン表記・補角・余角）")

# -----------------------------
# CSS（ボタンサイズ調整）
# -----------------------------
st.markdown("""
<style>
div.stButton > button {
    width: 160px !important;
    height: 70px !important;
    font-size: 22px;
}
.range-button > button {
    width: 240px !important;
    height: 80px !important;
    font-size: 24px !important;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 範囲選択画面（横並びボタン）
# -----------------------------
if not st.session_state.mode_selected:
    st.subheader("テスト範囲を選んでください")
    cols = st.columns(2)
    with cols[0]:
        if st.button("－2\pi　～　2\pi", key="range1", use_container_width=True):
            st.session_state.mode = "-2pi_to_2pi"
            st.session_state.mode_selected = True
            st.session_state.start_time = time.time()
            st.rerun()
    with cols[1]:
        if st.button("0　～　\pi", key="range2", use_container_width=True):
            st.session_state.mode = "0_to_pi"
            st.session_state.mode_selected = True
            st.session_state.start_time = time.time()
            st.rerun()

# -----------------------------
# 問題生成
# -----------------------------
def generate_question():
    funcs = ["sin", "cos", "tan"]

    if st.session_state.mode == "-2pi_to_2pi":
        patterns = [
            "pi/2+θ", "pi+θ", "3pi/2+θ",
            "-pi/2+θ", "-pi+θ", "-3pi/2+θ",
            "-θ",
            "pi/2-θ", "pi-θ", "3pi/2-θ",
            "-pi/2-θ", "-pi-θ", "-3pi/2-θ"
        ]
    else:  # "0_to_pi"
        patterns = [
            "pi/2+θ", "pi+θ",
            "pi/2-θ", "pi-θ",
            "-θ"
        ]

    func = random.choice(funcs)
    expr = random.choice(patterns)

    # 表示用 LaTeX を生成
    display_expr = latex_map.get(expr, expr)
    if expr == "-θ":
        problem = rf"\{func}\left(-\theta\right)\ を簡単にせよ."
    else:
        problem = rf"\{func}\left({display_expr}\right)\ を簡単にせよ."

    correct = simplify(func, expr)
    return problem, correct

# -----------------------------
# メイン部分（出題・結果）
# -----------------------------
if st.session_state.mode_selected:

    # 10問終了後の結果
    if st.session_state.question_number > 10:
        end_time = time.time()
        elapsed = Decimal(str(end_time - st.session_state.start_time)).quantize(Decimal('0.01'), ROUND_HALF_UP)
        total = st.session_state.score * 10
        st.subheader("結果")
        st.write(f"得点: {total}/100 点")
        st.write(f"経過時間: {elapsed} 秒")

        latex_table = r"\def\arraystretch{3}\begin{array}{|c|c|c|c|c|} \hline 番号 & 問題 & あなたの解答 & 正解 & 正誤 \\ \hline "
        for i, a in enumerate(st.session_state.answers, 1):
            mark = "○" if a["user"] == a["correct"] else "×"
            # 問題の先頭に番号を振る（(1)〜(10)）
            latex_table += f"{i} & {a['problem']} & {a['user']} & {a['correct']} & {mark} \\\\ \hline "
        latex_table += r"\end{array}"
        st.latex(latex_table)

        if st.button("もう一度やる"):
            st.session_state.update({
                "question_number": 1,
                "score": 0,
                "start_time": time.time(),
                "answers": [],
                "current_problem": None,
                "current_answer": None,
                "mode_selected": False,
                "mode": None
            })
            st.rerun()

    # 出題中
    else:
        if st.session_state.current_problem is None:
            problem, correct = generate_question()
            st.session_state.current_problem = problem
            st.session_state.current_answer = correct

        st.subheader(f"問題 {st.session_state.question_number}: （{ '－2\pi〜2\pi' if st.session_state.mode=='-2pi_to_2pi' else '0〜\pi' }）")
        st.markdown(rf"$$ {st.session_state.current_problem} $$")

        clicked_option = None
        for row in range(2):
            cols = st.columns(4)
            for col_idx in range(4):
                idx = row*4 + col_idx
                option = BUTTON_OPTIONS[idx]
                with cols[col_idx]:
                    if st.button(f"${option}$", key=f"{st.session_state.question_number}_{idx}"):
                        clicked_option = option

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
            st.rerun()
