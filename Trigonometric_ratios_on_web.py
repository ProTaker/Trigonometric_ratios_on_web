import streamlit as st
import random

st.title("三角比クイズ（sin・cos・tan 有名角編）")

# 有名角（度数法）
# 360度範囲外の角も含む
famous_angles = [-360, -330, -315, -300, -270, -240, -225, -210, -180, -150, -135, -120, -90, -60, -45, -30,
                 0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360, 390, 405, 420, 450]

# 出題対象の三角関数
functions = ["sin", "cos", "tan"]

# ✅ 選択肢（LaTeX表記できれいに）- 1/√3 の表記に戻し、「定義なし」に変更
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
    "1/√3": r"$\displaystyle \frac{1}{\sqrt{3}}$", # 1/√3 に戻す
    "-1/√3": r"$\displaystyle -\frac{1}{\sqrt{3}}$", # -1/√3 に戻す
    "定義なし": r"$\text{定義なし}$" # 「定義なし」に変更
}

# -----------------------------------------------
# ✅ 選択肢の分類（sin/cos 用と tan 用）
# -----------------------------------------------

# sin/cos の値（-1 から 1 の範囲）
sin_cos_options = [
    "0", "1/2", "√2/2", "√3/2", "1",
    "-1/2", "-√2/2", "-√3/2", "-1"
]

# tan の値（実数全体と定義なし）
tan_options = [
    "0", "1", "√3", "1/√3",
    "-1", "-√3", "-1/√3",
    "定義なし" # 「定義なし」を使用
]

# 有名角に対する正解辞書（分数表記）- tan の値を 1/√3 に戻し、定義なしに変更
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
        -360: "0", -330: "1/√3", -315: "1", -300: "√3", -270: "定義なし",
        -240: "√3", -225: "1", -210: "1/√3", -180: "0", -150: "-1/√3",
        -135: "-1", -120: "-√3", -90: "定義なし", -60: "-√3", -45: "-1",
        -30: "-1/√3", 0: "0", 30: "1/√3", 45: "1", 60: "√3", 90: "定義なし",
        120: "-√3", 135: "-1", 150: "-1/√3", 180: "0", 210: "1/√3",
        225: "1", 240: "√3", 270: "定義なし", 300: "-√3", 315: "-1",
        330: "-1/√3", 360: "0", 390: "1/√3", 405: "1", 420: "√3", 450: "定義なし"
    }
}

# 新しい問題を作る関数
def new_question():
    # ランダムに関数と角を選択し、セッションステートをリセット
    st.session_state.func = random.choice(functions)
    st.session_state.angle = random.choice(famous_angles)
    st.session_state.selected = None
    st.session_state.result = ""

# session_state 初期化
if 'func' not in st.session_state:
    new_question() # 初回起動時に新しい問題を作成

# -----------------------------------------------
# ✅ 現在の関数に基づいて表示する選択肢を決定
# -----------------------------------------------
current_func = st.session_state.func
if current_func == "sin" or current_func == "cos":
    display_options = sin_cos_options
else: # "tan" の場合
    display_options = tan_options

# 問題文
# LaTeXで表示
st.subheader(f"${current_func}({st.session_state.angle}^\\circ)$ の値は？")

# ✅ ボタンの幅をそろえるため、選択肢をカラム配置で整列
cols = st.columns(4) 

# 選択肢ボタンの表示と処理
for i, key in enumerate(display_options):
    with cols[i % 4]:
        # use_container_width=True で横幅を揃える
        # Streamlitのネイティブ機能では縦横統一は困難ですが、これ以上大きな分数表記がないため、
        # 縦幅の差は最小限に抑えられます。
        if st.button(latex_options[key], use_container_width=True, key=key):
            st.session_state.selected = key
            st.session_state.result = "" # 選択したら結果をリセット

# 答えの確認ボタン
if st.button("解答を確認"):
    if st.session_state.selected is not None:
        correct = answers[current_func][st.session_state.angle]
        correct_latex = latex_options[correct]

        if st.session_state.selected == correct:
            st.session_state.result = f"✅ **正解！**　${current_func}({st.session_state.angle}^\\circ) = {correct_latex}$"
        else:
            st.session_state.result = f"❌ **不正解…**　正しい答えは {correct_latex} です。"
    else:
        st.session_state.result = "選択肢を選んでください。"

# 結果表示
st.markdown(st.session_state.result)

# 次の問題ボタン
if st.button("次の問題"):
    new_question()
    # Streamlitの再実行を促し、画面を更新
    st.experimental_rerun()