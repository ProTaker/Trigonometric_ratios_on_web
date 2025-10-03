# trig_quiz_app_on_web_fixed.py
# 実行: python -m streamlit run trig_quiz_app_on_web_fixed.py

import random
import streamlit as st
import time
from decimal import Decimal, ROUND_HALF_UP

# ---------- ヘルパー: α(度) の sin, cos を返す（α は 360 の倍数を含む任意の整数） ----------
def sin_cos_of_angle_deg(angle_deg):
    # 正規化して 0,90,180,270 のいずれかに落とす
    norm = angle_deg % 360
    if norm == 0:
        return 0, 1   # sin, cos
    if norm == 90:
        return 1, 0
    if norm == 180:
        return 0, -1
    if norm == 270:
        return -1, 0
    # 万が一他の値が来たら (使わないはず) 数値計算で返す（ただし本来発生しない）
    import math
    return math.sin(math.radians(angle_deg)), math.cos(math.radians(angle_deg))

# ---------- 恒等式を作る（LaTeX 文字列で返す） ----------
def make_latex_sin_cos(coeff_sin, coeff_cos):
    # coeff_sin * sinθ + coeff_cos * cosθ を単項式に変換（このアプリでは係数は -1/0/1 のはず）
    if coeff_sin == 1 and coeff_cos == 0:
        return r"\sin\theta"
    if coeff_sin == -1 and coeff_cos == 0:
        return r"-\sin\theta"
    if coeff_sin == 0 and coeff_cos == 1:
        return r"\cos\theta"
    if coeff_sin == 0 and coeff_cos == -1:
        return r"-\cos\theta"
    # 万が一両方非ゼロになったら合成表現（現状の出題候補では発生しないはず）
    parts = []
    if coeff_sin != 0:
        parts.append(("" if coeff_sin == 1 else "-" if coeff_sin == -1 else f"{coeff_sin}*") + r"\sin\theta")
    if coeff_cos != 0:
        parts.append(("" if coeff_cos == 1 else "-" if coeff_cos == -1 else f"{coeff_cos}*") + r"\cos\theta")
    return " + ".join(parts)

def simplify(func, angle_deg, op):
    """
    func: "sin","cos","tan"
    angle_deg: integer (can be negative)
    op: '+' or '-'  (意味: alpha ± θ)
    戻り値: LaTeX表記の正解（例 r"\cos\theta" や r"-\sin\theta" や r"\displaystyle\frac{1}{\tan\theta}"）
    """
    sin_a, cos_a = sin_cos_of_angle_deg(angle_deg)
    # sin_a, cos_a の値は -1,0,1 のいずれ（想定）
    sign = 1 if op == '+' else -1

    if func == "sin":
        # sin(alpha ± θ) = sinα cosθ ± cosα sinθ
        # coef for sinθ = ± cosα  (＝ sign * cos_a)
        # coef for cosθ = sinα
        coef_sin = sign * cos_a
        coef_cos = sin_a
        return make_latex_sin_cos(coef_sin, coef_cos)

    if func == "cos":
        # cos(alpha ± θ) = cosα cosθ ∓ sinα sinθ
        # coef for cosθ = cosα
        # coef for sinθ = ∓ sinα  (＝ -sign * sin_a)
        coef_cos = cos_a
        coef_sin = -sign * sin_a
        return make_latex_sin_cos(coef_sin, coef_cos)

    if func == "tan":
        # tan(alpha ± θ) = (sinα cosθ ± cosα sinθ) / (cosα cosθ ∓ sinα sinθ)
        # ここで分子・分母は（係数）*sinθ または *cosθ の形になる（α が 90° 等のため）
        # 分子: num = num_sin * sinθ + num_cos * cosθ
        # 分母: den = den_sin * sinθ + den_cos * cosθ
        if op == '+':
            num_sin = cos_a  # coefficient for sinθ in numerator
            num_cos = sin_a
            den_cos = cos_a
            den_sin = -sin_a
        else:
            # op == '-'
            num_sin = -cos_a
            num_cos = sin_a
            den_cos = cos_a
            den_sin = sin_a

        # 可能な簡約パターン（α は 90° 単位なので一つだけが非ゼロになる）
        # ケース 1: numerator = k1 * sinθ, denominator = k2 * cosθ => result = (k1/k2) * tanθ
        if num_cos == 0 and den_sin == 0 and num_sin != 0 and den_cos != 0:
            k = (1 if (num_sin * den_cos) > 0 else -1)
            return r"\tan\theta" if k == 1 else r"-\tan\theta"
        # ケース 2: numerator = k1 * cosθ, denominator = k2 * sinθ => result = (k1/k2) * cotθ = ± 1/tanθ
        if num_sin == 0 and den_cos == 0 and num_cos != 0 and den_sin != 0:
            k = (1 if (num_cos * den_sin) > 0 else -1)
            if k == 1:
                return r"\displaystyle\frac{1}{\tan\theta}"
            else:
                return r"\displaystyle-\frac{1}{\tan\theta}"
        # ケース 3: numerator and denominator both proportional to same function -> ±1 (→ ±1)
        # 例: num = ±sinθ, den = ±sinθ など → ±1 (tan=±1) -> ここでは tanθ や 1/tanθ の形に落ちないが
        #       ただし α が 90° 単位だと発生しにくいので、安全策として文字列で返す
        # 最後に安全フォールバック（未想定ケース）
        return r"\text{定義なし}"

    # デフォルト（起こらない）
    return r"\text{不明}"

# ---------- ボタン選択肢（LaTeX 表現、順番固定） ----------
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

# ---------- CSS（ボタン大きめ） ----------
st.markdown("""
<style>
div.stButton > button {
    width: 170px !important;
    height: 64px !important;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("三角比クイズ（α±θ と −θ を含む）")

# ---------- 終了時 ----------
if st.session_state.question_number >= 10:
    end_time = time.time()
    elapsed = Decimal(str(end_time - st.session_state.start_time)).quantize(Decimal("0.01"), ROUND_HALF_UP)
    total = st.session_state.score * 10
    st.subheader("結果")
    st.write(f"得点: {total}/100 点")
    st.write(f"経過時間: {elapsed} 秒")

    # 回答表（LaTeXで表現）
    latex_table = r"\def\arraystretch{2}\begin{array}{|c|c|c|c|} \hline 問題 & あなたの解答 & 正解 & 正誤 \\ \hline "
    for a in st.session_state.answers:
        mark = "○" if a["user"] == a["correct"] else "×"
        latex_table += f"${a['problem']}$ & ${a['user']}$ & ${a['correct']}$ & {mark} \\\\ \\hline "
    latex_table += r"\end{array}"
    st.latex(latex_table)

    if st.button("もう一度やる"):
        st.session_state.update({
            "question_number": 0,
            "score": 0,
            "start_time": time.time(),
            "answers": [],
            "current_problem": None,
            "current_answer": None
        })
        st.experimental_rerun()

# ---------- 出題中 ----------
else:
    # 新規問題を生成（current_problem が None のとき）
    if st.session_state.current_problem is None:
        funcs = ["sin", "cos", "tan"]
        base_angles = [0, 90, 180, 270, 360, -90, -180, -270]
        func = random.choice(funcs)
        angle = random.choice(base_angles)
        op = random.choice(['+','-'])   # '+' または '-' をランダムに選ぶ（これで 90°+θ と 90°-θ の両方が出る）
        # 表示ルール：角度が 0 かどうかで括弧の有無を決める
        if angle == 0 and op == '+':
            problem = rf"\{func}\theta を簡単にせよ"
        elif angle == 0 and op == '-':
            problem = rf"\{func}(-\theta) を簡単にせよ"
        else:
            problem = rf"\{func}({angle}^\circ{op}\theta) を簡単にせよ"

        correct = simplify(func, angle, op)
        st.session_state.current_problem = problem
        st.session_state.current_answer = correct

    # 問題表示
    st.subheader(f"問題 {st.session_state.question_number + 1}")
    st.markdown(rf"$$ {st.session_state.current_problem} $$")

    # 選択肢を 2行×4列に固定順で表示（順番は常に BUTTON_OPTIONS の通り）
    clicked = None
    for r in range(2):
        cols = st.columns(4)
        for c in range(4):
            idx = r*4 + c
            with cols[c]:
                if st.button(f"${BUTTON_OPTIONS[idx]}$", key=f"{st.session_state.question_number}_{idx}"):
                    clicked = BUTTON_OPTIONS[idx]

    if clicked:
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
        st.experimental_rerun()
