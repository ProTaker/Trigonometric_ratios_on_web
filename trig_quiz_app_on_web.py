import random
import streamlit as st
import time
from decimal import Decimal, ROUND_HALF_UP

# -----------------------------
# sin/cosの簡単化ルール
# -----------------------------
SIN_RULES = {
    "90+θ": r"\cos\theta", "180+θ": r"-\sin\theta", "270+θ": r"-\cos\theta",
    "-90+θ": r"-\cos\theta", "-180+θ": r"-\sin\theta", "-270+θ": r"\cos\theta",
    "0+θ": r"\sin\theta", "-θ": r"-\sin\theta",
    "90-θ": r"\cos\theta", "180-θ": r"\sin\theta", "270-θ": r"-\cos\theta"
}

COS_RULES = {
    "90+θ": r"-\sin\theta", "180+θ": r"-\cos\theta", "270+θ": r"\sin\theta",
    "-90+θ": r"\sin\theta", "-180+θ": r"-\cos\theta", "-270+θ": r"-\sin\theta",
    "0+θ": r"\cos\theta", "-θ": r"\cos\theta",
    "90-θ": r"\sin\theta", "180-θ": r"-\cos\theta", "270-θ": r"-\sin\theta"
}

# -----------------------------
# 三角比簡単化
# -----------------------------
def simplify(func, expr):
    if func == "sin":
        return SIN_RULES[expr]
    elif func == "cos":
        return COS_RULES[expr]
    elif func == "tan":
        # tan = sin/cos
        sin_val = SIN_RULES[expr]
        cos_val = COS_RULES[expr]
        # ±1/tanθ の場合は sin/cos の文字列から判断
        if sin_val.startswith("-") != cos_val.startswith("-") or ("cos" in sin_val and "sin" in cos_val):
            return r"\displaystyle-\frac{1}{\tan\theta}"
        elif sin_val.startswith("-") and cos_val.startswith("-"):
            return r"\displaystyle\frac{1}{\tan\theta}"
        else:
            return r"\tan\theta"
    else:
        return ""

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
                 ("answers",[]), ("current_problem",None), ("current_answer",None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# -----------------------------
# 問題生成
# -----------------------------
def generate_question():
    funcs = ["sin", "cos", "tan"]
    patterns = ["90+θ", "180+θ", "270+θ", "-90+θ", "-180+θ", "-270+θ", "0+θ", "-θ", "90-θ", "180-θ", "270-θ"]
    func = random.choice(funcs)
    expr = random.choice(patterns)

    if expr == "-θ":
        problem = rf"{func}(-\theta) を簡単にせよ"
    else:
        # 角度に°をつける
        degree_expr = expr.replace("θ", "^\circ+\theta") if "+" in expr else expr.replace("θ", "^\circ-\theta")
        problem = rf"{func}({degree_expr}) を簡単にせよ"
    
    correct = simplify(func, expr)
    return problem, correct

# -----------------------------
# CSS: ボタン縦横揃える
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
# タイトル
# -----------------------------
st.title("三角比クイズ (θの簡単化)")

# -----------------------------
# 10問終了チェック
# -----------------------------
if st.session_state.question_number > 10:
    end_time = time.time()
    elapsed = Decimal(str(end_time - st.session_state.start_time)).quantize(Decimal('0.01'), ROUND_HALF_UP)
    total = st.session_state.score * 10
    st.subheader("結果")
    st.write(f"得点: {total}/100 点")
    st.write(f"経過時間: {elapsed} 秒")

    # 表形式で表示
    import pandas as pd
    df = pd.DataFrame([{
        "問題": a["problem"],
        "あなたの解答": a["user"],
        "正解": a["correct"],
        "正誤": "○" if a["user"] == a["correct"] else "×"
    } for a in st.session_state.answers])
    st.dataframe(df, use_container_width=True)

    if st.button("もう一度やる"):
        st.session_state.update({
            "question_number": 1,
            "score": 0,
            "start_time": time.time(),
            "answers": [],
            "current_problem": None,
            "current_answer": None
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
    st.subheader(f"問題 {st.session_state.question_number}: ")
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

    # ボタン押した場合、次の問題へ
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
