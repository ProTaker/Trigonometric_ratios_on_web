# trig_quiz_app_on_web_fixed2.py
# 実行: python -m streamlit run trig_quiz_app_on_web_fixed2.py

import random
import streamlit as st
import time
from decimal import Decimal, ROUND_HALF_UP

# ---------- ヘルパー ----------
def sin_cos_of_angle_deg(angle_deg):
    """angle_deg を 360 で正規化して 0,90,180,270 の値に対応する sin, cos を返す（整数入力を想定）"""
    norm = angle_deg % 360
    if norm == 0:
        return 0, 1
    if norm == 90:
        return 1, 0
    if norm == 180:
        return 0, -1
    if norm == 270:
        return -1, 0
    # 万が一（ここでは発生しないが）数値で返す
    import math
    return math.sin(math.radians(angle_deg)), math.cos(math.radians(angle_deg))

def make_latex_sin_cos(coef_sin, coef_cos):
    """
    coef_sin * sinθ + coef_cos * cosθ を単純な項に変換して LaTeX 文字列で返す。
    coef は -1,0,1 のはず（このアプリの角度候補ではそのはず）。
    """
    if coef_sin == 1 and coef_cos == 0:
        return r"\sin\theta"
    if coef_sin == -1 and coef_cos == 0:
        return r"-\sin\theta"
    if coef_sin == 0 and coef_cos == 1:
        return r"\cos\theta"
    if coef_sin == 0 and coef_cos == -1:
        return r"-\cos\theta"
    # 万が一混合係数になったら組合せ表現を返す（通常は出ない）
    parts = []
    if coef_sin != 0:
        parts.append(( "-" if coef_sin == -1 else "" ) + r"\sin\theta")
    if coef_cos != 0:
        parts.append(( "-" if coef_cos == -1 else "" ) + r"\cos\theta")
    return " + ".join(parts)

def simplify(func, angle_deg, op):
    """
    func: "sin","cos","tan"
    angle_deg: 整数角度（例 90, -90, 0 等）
    op: '+' または '-'  (alpha ± θ)
    戻り: LaTeX表記の正解（例 r"\cos\theta", r"-\sin\theta", r"\displaystyle\frac{1}{\tan\theta}"）
    """
    sin_a, cos_a = sin_cos_of_angle_deg(angle_deg)
    sign = 1 if op == '+' else -1

    if func == "sin":
        # sin(α ± θ) = sinα cosθ ± cosα sinθ
        coef_sin = sign * cos_a   # sinθ の係数
        coef_cos = sin_a          # cosθ の係数
        return make_latex_sin_cos(coef_sin, coef_cos)

    if func == "cos":
        # cos(α ± θ) = cosα cosθ ∓ sinα sinθ
        coef_cos = cos_a
        coef_sin = -sign * sin_a
        return make_latex_sin_cos(coef_sin, coef_cos)

    if func == "tan":
        # tan(α ± θ) = (sinα cosθ ± cosα sinθ) / (cosα cosθ ∓ sinα sinθ)
        # 角度αは90度単位なので分子・分母は単一項になるケースがメイン
        if op == '+':
            num_sin = sign * cos_a   # actually sign==1 so cos_a
            num_cos = sin_a
            den_cos = cos_a
            den_sin = -sin_a
        else: # op == '-'
            num_sin = sign * cos_a   # sign == -1
            num_cos = sin_a
            den_cos = cos_a
            den_sin = -sign * sin_a  # -(-1)*sin_a = sin_a

        # ケース分岐（α は 90° 単位 → どちらか一方が0）
        # (A) num = k1*sinθ, den = k2*cosθ  -> ±tanθ
        if num_cos == 0 and den_sin == 0 and num_sin != 0 and den_cos != 0:
            k = 1 if (num_sin * den_cos) > 0 else -1
            return r"\tan\theta" if k == 1 else r"-\tan\theta"

        # (B) num = k1*cosθ, den = k2*sinθ -> ±1/tanθ
        if num_sin == 0 and den_cos == 0 and num_cos != 0 and den_sin != 0:
            k = 1 if (num_cos * den_sin) > 0 else -1
            return r"\displaystyle\frac{1}{\tan\theta}" if k == 1 else r"\displaystyle-\frac{1}{\tan\theta}"

        # (C) どちらも同じ関数に比例 -> ±1（稀）: ここでは定義なし扱いにしておく
        return r"\text{定義なし}"

    return r"\text{不明}"

# ---------- 選択肢（固定順、LaTeX文字列） ----------
BUTTON_OPTIONS = [
    r"\sin\theta", r"-\sin\theta",
    r"\cos\theta", r"-\cos\theta",
    r"\tan\theta", r"-\tan\theta",
    r"\displaystyle\frac{1}{\tan\theta}", r"\displaystyle-\frac{1}{\tan\theta}"
]

# ---------- セッション初期化 ----------
if "question_number" not in st.session_state:
    st.session_state.question_number = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()
if "answers" not in st.session_state:
    st.session_state.answers = []
if "current_problem" not in st.session_state:
    st.session_state.current_problem = None
if "current_answer" not in st.session_state:
    st.session_state.current_answer = None

# ---------- スタイル ----------
st.markdown("""
<style>
div.stButton > button {
    width: 170px !important;
    height: 64px !important;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

st.title("三角比クイズ（α±θ と −θ を含む） — 修正版")

# ---------- 終了表示 ----------
if st.session_state.question_number >= 10:
    end_time = time.time()
    elapsed = Decimal(str(end_time - st.session_state.start_time)).quantize(Decimal("0.01"), ROUND_HALF_UP)
    total = st.session_state.score * 10
    st.subheader("結果")
    st.write(f"得点: {total}/100 点")
    st.write(f"経過時間: {elapsed} 秒")

    st.markdown("### 各問題の結果")
    # 各行を個別にきれいに表示（LaTeX は $...$ で囲む）
    for i, a in enumerate(st.session_state.answers, start=1):
        mark = "○" if a["user"] == a["correct"] else "×"
        st.markdown(
            rf"**問題 {i}**: $ {a['problem']} $  — あなたの解答: $ {a['user']} $ 、正解: $ {a['correct']} $　**{mark}**"
        )

    # 履歴（簡単なテーブル）
    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append((total, float(elapsed)))
    import pandas as pd
    df = pd.DataFrame(st.session_state.history, columns=["得点", "時間(s)"])
    st.markdown("### 履歴")
    st.dataframe(df)

    if st.button("もう一度やる"):
        st.session_state.update({
            "question_number": 0,
            "score": 0,
            "start_time": time.time(),
            "answers": [],
            "current_problem": None,
            "current_answer": None
        })
        # Streamlit はウィジェット操作で自動的に再実行されるため rerun 呼び出しは不要

# ---------- 出題処理 ----------
else:
    # current_problem が None のときに新規生成
    if st.session_state.current_problem is None:
        funcs = ["sin", "cos", "tan"]
        base_angles = [0, 90, 180, 270, 360, -90, -180, -270]
        func = random.choice(funcs)
        angle = random.choice(base_angles)
        op = random.choice(['+','-'])

        # 問題の「数学部分」を純粋な LaTeX 文字列だけで作る（日本語は別で表示）
        if angle == 0 and op == '+':
            problem_tex = rf"\{func}\theta"
        elif angle == 0 and op == '-':
            problem_tex = rf"\{func}(-\theta)"
        else:
            # 例: \sin(90^\circ+\theta)
            problem_tex = rf"\{func}({angle}^\circ{op}\theta)"

        correct = simplify(func, angle, op)
        st.session_state.current_problem = problem_tex
        st.session_state.current_answer = correct

    # 表示（日本語は数式外）
    st.subheader(f"問題 {st.session_state.question_number + 1}")
    st.markdown(rf"問題: $ {st.session_state.current_problem} $ を簡単にせよ")

    # 選択肢（固定順）を 2行×4列で表示
    clicked = None
    for r in range(2):
        cols = st.columns(4)
        for c in range(4):
            idx = r*4 + c
            with cols[c]:
                if st.button(f"${BUTTON_OPTIONS[idx]}$", key=f"{st.session_state.question_number}_{idx}"):
                    clicked = BUTTON_OPTIONS[idx]

    # 回答処理（ボタン押されたら自動的にページが再実行される）
    if clicked is not None:
        st.session_state.answers.append({
            "problem": st.session_state.current_problem,
            "user": clicked,
            "correct": st.session_state.current_answer
        })
        if clicked == st.session_state.current_answer:
            st.session_state.score += 1

        st.session_state.question_number += 1
        st.session_state.current_problem = None
        st.session_state.current_answer = None
