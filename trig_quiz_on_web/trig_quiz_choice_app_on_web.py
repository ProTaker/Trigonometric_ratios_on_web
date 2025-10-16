import random
import streamlit as st
import time
from decimal import Decimal, ROUND_HALF_UP

# -----------------------------
# 三角比簡単化ルール（分数は\displaystyle）
# -----------------------------
def simplify(func, expr):
    rules = {
        "sin": {
            "90°+θ": r"\cos\theta", "180°+θ": r"-\sin\theta", "270°+θ": r"-\cos\theta",
            "-90°+θ": r"-\cos\theta", "-180°+θ": r"-\sin\theta", "-270°+θ": r"\cos\theta",
            "-θ": r"-\sin\theta",
            "90°-θ": r"\cos\theta", "180°-θ": r"\sin\theta", "270°-θ": r"-\cos\theta",
            "-90°-θ": r"\cos\theta", "-180°-θ": r"-\sin\theta", "-270°-θ": r"-\cos\theta"
        },
        "cos": {
            "90°+θ": r"-\sin\theta", "180°+θ": r"-\cos\theta", "270°+θ": r"\sin\theta",
            "-90°+θ": r"\sin\theta", "-180°+θ": r"-\cos\theta", "-270°+θ": r"-\sin\theta",
            "-θ": r"\cos\theta",
            "90°-θ": r"\sin\theta", "180°-θ": r"-\cos\theta", "270°-θ": r"-\sin\theta",
            "-90°-θ": r"-\sin\theta", "-180°-θ": r"-\cos\theta", "-270°-θ": r"\sin\theta"
        },
        "tan": {
            "90°+θ": r"\displaystyle-\frac{1}{\tan\theta}", "180°+θ": r"\tan\theta", "270°+θ": r"\displaystyle-\frac{1}{\tan\theta}",
            "-90°+θ": r"\displaystyle-\frac{1}{\tan\theta}", "-180°+θ": r"\tan\theta", "-270°+θ": r"\displaystyle-\frac{1}{\tan\theta}",
            "-θ": r"-\tan\theta",
            "90°-θ": r"\displaystyle\frac{1}{\tan\theta}", "180°-θ": r"-\tan\theta", "270°-θ": r"\displaystyle\frac{1}{\tan\theta}",
            "-90°-θ": r"\displaystyle\frac{1}{\tan\theta}", "-180°-θ": r"-\tan\theta", "-270°-θ": r"\displaystyle\frac{1}{\tan\theta}"
        }
    }
    return rules[func][expr]

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
st.title("三角比クイズ (補角・余角)")

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
        if st.button("－360°　～　360°", key="range1", use_container_width=True):
            st.session_state.mode = "－360°　～　360°"
            st.session_state.mode_selected = True
            st.session_state.start_time = time.time()
            st.rerun()
    with cols[1]:
        if st.button("0°　～　180°", key="range2", use_container_width=True):
            st.session_state.mode = "0°　～　180°"
            st.session_state.mode_selected = True
            st.session_state.start_time = time.time()
            st.rerun()

# -----------------------------
# 問題生成
# -----------------------------
def generate_question():
    funcs = ["sin", "cos", "tan"]

    if st.session_state.mode == "－360°　～　360°":
        patterns = [
            "90°+θ", "180°+θ", "270°+θ",
            "-90°+θ", "-180°+θ", "-270°+θ",
            "-θ",
            "90°-θ", "180°-θ", "270°-θ",
            "-90°-θ", "-180°-θ", "-270°-θ"
        ]
    else:  # "0°　～　180°"
        patterns = [
            "90°+θ", "180°+θ",
            "90°-θ", "180°-θ",
            "-θ"
        ]

    func = random.choice(funcs)
    expr = random.choice(patterns)

    if expr == "-θ":
        problem = rf"\{func}\ (-\theta)\ を簡単にせよ."
    else:
        problem = rf"\{func}\ ({expr})\ を簡単にせよ."
    
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

        st.subheader(f"問題 {st.session_state.question_number}: （{st.session_state.mode}）")
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
